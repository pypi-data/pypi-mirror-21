###############################################################################
# Caleydo - Visualization for Molecular Biology - http://caleydo.org
# Copyright (c) The Caleydo Team. All rights reserved.
# Licensed under the new BSD license, available at http://caleydo.org/license
###############################################################################


from past.builtins import basestring
import phovea_server.plugin
import phovea_server.range
import phovea_server.util
import itertools

_providers_r = None


def _providers():
  global _providers_r
  if _providers_r is None:
    _providers_r = [p.load().factory() for p in phovea_server.plugin.list('dataset-provider')]
  return _providers_r


def iter():
  """
  an iterator of all known datasets
  :return:
  """
  return itertools.chain(*_providers())


def list_datasets():
  """
  list all known datasets
  :return:
  """
  return list(iter())


def get(dataset_id):
  """
  :param dataset_id:
  :return: returns the selected dataset identified by id
  """
  for p in _providers():
    r = p[dataset_id]
    if r is not None:
      return r
  return None


def add(desc, files=[], id=None):
  """
  adds a new dataset to this storage
  :param desc: the dict description information
  :param files: a list of FileStorage
  :param id: optional the unique id to use
  :return: the newly created dataset or None if an error occurred
  """
  for p in _providers():
    r = p.upload(desc, files, id)
    if r:
      return r
  return None


def update(dataset, desc, files=[]):
  """
  updates the given dataset
  :param dataset: a dataset or a dataset id
  :param desc: the dict description information
  :param files: a list of FileStorage
  :return:
  """
  old = get(dataset) if isinstance(dataset, basestring) else dataset
  if old is None:
    return add(desc, files)
  r = old.update(desc, files)
  return r


def remove(dataset):
  """
  removes the given dataset
  :param dataset: a dataset or a dataset id
  :return: boolean whether the operation was successful
  """
  old = get(dataset) if isinstance(dataset, basestring) else dataset
  if old is None:
    return False
  for p in _providers():
    if p.remove(old):
      return True
  return False


def list_idtypes():
  tmp = dict()
  for d in list_datasets():
    for idtype in d.to_idtype_descriptions():
      tmp[idtype['id']] = idtype
  return list(tmp.values())


def get_idmanager():
  return phovea_server.plugin.lookup('idmanager')


def get_mappingmanager():
  return phovea_server.plugin.lookup('mappingmanager')
