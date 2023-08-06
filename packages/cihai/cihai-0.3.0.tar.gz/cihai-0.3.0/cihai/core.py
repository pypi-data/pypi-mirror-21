#!/usr/bin/env python
# -*- coding: utf8 - *-
"""Cihai client object."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import argparse
import logging
import os

import kaptan
from sqlalchemy import Table, create_engine

from cihai import db, exc
from cihai._compat import string_types
from cihai.util import convert_to_attr_dict, import_string, merge_dict

log = logging.getLogger(__name__)


class CihaiDataset(object):
    """Mixin generic sqlalchemy yum-yums for relational data."""

    def __init__(self, cihai, engine, metadata):
        """Initialize CihaiDatabase back-end.

        :param engine: engine to connect to database with.
        :param type:class:`sqlalchemy.engine.Engine`

        """

        #: :class:`Cihai` application object.
        self.cihai = cihai

        #: :class:`sqlalchemy.engine.Engine` instance.
        self.engine = engine

        #: :class:`sqlalchemy.schema.MetaData` instance.
        self.metadata = metadata

    def get_table(self, table_name):
        """Return :class:`~sqlalchemy.schema.Table`.

        :param table_name: name of sql table
        :type table_name: string
        :rtype: :class:`sqlalchemy.schema.Table`

        """

        return Table(table_name, self.metadata, autoload=True)

    def table_exists(self, table_name):

        """Return True if table exists in db."""

        return True if table_name in self.metadata.tables else False

    def get_datapath(self, filename):
        """Return absolute filepath in relation to :attr:`self.data_path`.

        :param filename: file name relative to ``./data``.
        :type filename: string
        :returns: Absolute path to data file.
        :rtype: string

        """

        data_path = self.cihai.config.get('data_path')

        return os.path.join(data_path, filename)


class Cihai(object):

    """Cihai query client. May use :meth:`~.get()` to grab 中文.

    Cihai object is inspired by `pypa/warehouse`_ Warehouse applicaton object.

    .. _pypa/warehouse: https://github.com/pypa/warehouse

    """

    def __init__(self, config, engine=None):

        #: configuration dictionary. Available as attributes. ``.config.debug``
        self.config = convert_to_attr_dict(config)

        #: absolute path to cihai data files.
        if not self.config.get('data_path'):
            self.config['data_path'] = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 'data/'
            ))

        #: list of current datasets in session
        self.datasets = self.config.get('datasets', [])
        if isinstance(self.datasets, string_types):
            self.datasets = [self.datasets]

        #: list of dataset models in session
        self.models = []

        for ds in self.datasets:
            m = import_string(ds)
            self.models.append(m)

        if engine is None and self.config.get('database', {}).get('url'):
            engine = create_engine(self.config.database.url)
        #: :class:`sqlalchemy.engine.Engine` instance.
        self.engine = engine

        #: :class:`sqlalchemy.schema.MetaData` instance.
        self.metadata = db.metadata
        self.metadata.bind = self.engine

    @classmethod
    def from_file(cls, config_path=None, *args, **kwargs):
        """Create a Cihai instance from a JSON or YAML config.

        :param config_path: path to custom config file
        :type confiig_path: str
        :rtype: :class:`Cihai`

        """

        config = dict()
        configReader = kaptan.Kaptan()

        default_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "config.yml",
        ))
        config = configReader.import_config(default_path).get()

        if config_path:
            if not os.path.exists(config_path):
                raise Exception(
                    '{0} does not exist.'.format(os.path.abspath(config_path)))
            if not any(
                config_path.endswith(ext) for ext in
                ('json', 'yml', 'yaml', 'ini')
            ):
                raise Exception(
                    '{0} does not have a yaml,yml,json,ini extension.'
                    .format(os.path.abspath(config_path))
                )
            else:
                custom_config = configReader.import_config(config_path).get()
                config = merge_dict(config, custom_config)

        return cls(config)

    @classmethod
    def from_cli(cls, argv):
        """Cihai from :py:class:`argparse` / CLI args.

        :param argv: list of arguments, i.e. ``['-c', 'dev/config.yml']``.
        :type argv: list
        :rtype: :class:`Cihai`

        """
        parser = argparse.ArgumentParser(prog="cihai")
        parser.add_argument("-c", "--config", dest="_config")

        args = parser.parse_args(argv)
        config = args._config if args._config is not None else None

        return cls.from_file(config)

    def use(self, Dataset, *args, **kwargs):
        """Add a dataset to cihai instance.

        This is inspired by connect's datasets and pypa/warehouse keeping
        application instances the same ``self`` in the application object.

        ``use`` will pass ``*args`` (positional arguments) and ``**kwargs``
        (keyword arguments) into the dataset.

        :param Dataset: class for dataset object
        :type dataset: :class:`CihaiDataset`
        :returns: instance of dataset paired with ``cihai`` instance.
        :rtype: :class:`CihaiDataset` instance.

        """

        dataset = Dataset(
            self,
            self.engine,
            self.metadata,
            *args, **kwargs
        )

        if dataset not in self.datasets:
            self.datasets.append(dataset)

        return dataset

    def get(self, request, *args, **kwargs):
        """Return results datasets.

        :param request: request / input data
        :type request: string
        :rtype: list

        """

        if not self.datasets:
            raise exc.NoDatasets

        response = {}

        for m in self.datasets:
            if hasattr(m, 'get'):
                response = m.get(request, response, *args, **kwargs)
            if not response:
                break

        return response

    def reverse(self, request, *args, **kwargs):
        """Return results if exists in datasets.

        :param request: request / input data
        :type request: string
        :rtype: list

        """

        if not self.datasets:
            raise exc.NoDatasets

        response = {}

        for m in self.datasets:
            if hasattr(m, 'reverse'):
                response = m.reverse(request, response, *args, **kwargs)
            if not response:
                break

        return response
