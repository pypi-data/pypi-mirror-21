#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
smart_reader loads, caches, and invokes reader logic for a supplied file path
based on that files extension. It is provided for convenience, and also forms
the backbone of the command line interface.

"""
from importlib import import_module
from os.path import splitext

from pandas import DataFrame


MODULE_CACHE = {}


def smart_reader(file_path, *, vanilla=False, **read_kwargs):
    """Dispatch a file reader based on file extension.

    Parameters
    ----------
    file_path : str
        Path to the file to be read.
    vanilla : bool, optional
        Return a spruced up subclass of the ``pandas.DataFrame``
        (``ActivityData``) and benefit from some extra data pruning and
        functionality, or be boring and get the raw data untouched.
    **read_kwargs
        Passed down to <file format>.read()

    Returns
    -------
    ActivityData or DataFrame
        The output depends on the `vanilla` argument.

    Raises
    ------
    ImportError
        If the file type (based on the extension) is not supported.
    """
    ext = splitext(file_path)[-1][1:]   # drop period from the extension
    ext = ext.lower()  # important

    module = MODULE_CACHE.get(ext, None)
    if module is None:
        try:
            MODULE_CACHE[ext] = import_module('activityio.' + ext)
        except ImportError:
            raise ImportError('%s is not a supported file type' % ext)
        else:
            module = MODULE_CACHE.get(ext)

    if not vanilla:
        return module.read(file_path, **read_kwargs)
    else:
        return DataFrame.from_records(module.gen_records(file_path))
