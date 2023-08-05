#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Sat 20 Aug 15:43:10 CEST 2016

"""
  YOUTUBE database implementation of bob.bio.base.database.ZTDatabase interface.
  It is an extension of an SQL-based database interface, which directly talks to YOUTUBE database, for
  verification experiments (good to use in bob.bio.base framework).
"""


from .database import VideoBioFile
from bob.bio.base.database import ZTBioDatabase
from bob.bio.video.utils import FrameContainer
import os
import bob.io.base


class YoutubeBioFile(VideoBioFile):

    def __init__(self, f):
        super(YoutubeBioFile, self).__init__(client_id=f.client_id, path=f.path, file_id=f.id)
        self._f = f

    def load(self, directory=None, extension='.jpg'):
        if extension in (None, '.jpg', '/*.jpg'):
            files = sorted(os.listdir(self.make_path(directory, '')))
            fc = FrameContainer()

            for f in files:
                if extension == os.path.splitext(f)[1]:
                    file_name = os.path.join(self.make_path(directory, ''), f)
                    fc.add(os.path.basename(file_name), bob.io.base.load(file_name))
            return fc
        else:
            return super(YoutubeBioFile, self).load(directory, extension)


class YoutubeBioDatabase(ZTBioDatabase):
    """
    YOUTUBE database implementation of bob.bio.base.database.ZTDatabase interface.
    It is an extension of an SQL-based database interface, which directly talks to YOUTUBE database, for
    verification experiments (good to use in bob.bio.base framework).
    """

    def __init__(
            self,
            original_directory=None,
            original_extension='/*.jpg',
            annotation_extension='.labeled_faces.txt',
            **kwargs
    ):
        # call base class constructors to open a session to the database
        super(YoutubeBioDatabase, self).__init__(
            name='youtube',
            original_directory=original_directory,
            original_extension=original_extension,
            annotation_extension=annotation_extension,
            **kwargs)

        from bob.db.youtube.query import Database as LowLevelDatabase
        self._db = LowLevelDatabase(original_directory,
                                    original_extension,
                                    annotation_extension)

    def model_ids_with_protocol(self, groups=None, protocol=None, **kwargs):
        return self._db.model_ids(groups=groups, protocol=protocol)

    def tmodel_ids_with_protocol(self, protocol=None, groups=None, **kwargs):
        return self._db.tmodel_ids(protocol=protocol, groups=groups, **kwargs)

    def objects(self, groups=None, protocol=None, purposes=None, model_ids=None, **kwargs):
        retval = self._db.objects(groups=groups, protocol=protocol, purposes=purposes, model_ids=model_ids, **kwargs)
        return [YoutubeBioFile(f) for f in retval]

    def tobjects(self, groups=None, protocol=None, model_ids=None, **kwargs):
        retval = self._db.tobjects(groups=groups, protocol=protocol, model_ids=model_ids, **kwargs)
        return [YoutubeBioFile(f) for f in retval]

    def zobjects(self, groups=None, protocol=None, **kwargs):
        retval = self._db.zobjects(groups=groups, protocol=protocol, **kwargs)
        return [YoutubeBioFile(f) for f in retval]

    def annotations(self, myfile):
        return self._db.annotations(myfile._f)
