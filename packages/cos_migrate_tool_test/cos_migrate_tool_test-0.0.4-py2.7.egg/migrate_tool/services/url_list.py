# -*- coding: utf-8 -*-


from migrate_tool import storage_service
from migrate_tool import task
from logging import getLogger
import requests
import urlparse
import hashlib

logger = getLogger(__name__)


class UrlListService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        self._url_list_file = kwargs['url_list_file']
        self._timeout = float(kwargs['timeout'])
        self._chunk_size = 1024
        if kwargs.has_key("validator"):
            if kwargs['validator'] == "sha1":
                self._validator = hashlib.sha1()
            elif kwargs['validator'] == "md5":
                self._validator = hashlib.md5()
            else:
                self._validator = None
        else:
            self._validator = None

    def download(self, task, local_path):

        url_path = task.other
        expected_crc = task.size # size stores the sha1 or md5 of file

        for i in range(5):
            try:
                ret = requests.get(url_path, timeout=self._timeout)
                if ret.status_code == 200:
                    with open(local_path, 'wb') as fd:
                        for chunk in ret.iter_content(self._chunk_size):
                            if self._validator:
                                self._validator.update(chunk)
                            fd.write(chunk)
                        fd.flush()
                    # validate 
                    if self._validator:
                         actual_crc = self._validator.hexdigest()
                         if actual_crc != expected_crc:
                             raise IOError("NOTICE: downloaded file content not valid")
                    break
                else:
                    # print "task: ", task
                    raise IOError("NOTICE: download failed")
            except:
                logger.exception("download failed")
        else:
            raise IOError("NOTICE: download failed with retry 5")

    def upload(self, task, local_path):
        raise NotImplementedError

    def list(self):
        with open(self._url_list_file, 'r') as f:
            for line in f:
                try:
                    field = line.split()
                    if len(field) < 1:
                        logger.warn("{} is invalid".format(line))
                        continue
                    check_value = None
                    url_path = None
                    if len(field) == 1:
                        url_path = field[0]
                    else:
                        check_value = field[0].strip()
                        url_path = field[1]
                    ret = urlparse.urlparse(url_path)
                    if ret.path == '':
                        logger.warn("{} is invalid, No path".format(line))
                    logger.info("yield new object: {}".format(str({'store_path': ret.path.strip(), 'url_path': url_path.strip()})))
                    yield task.Task(ret.path.strip()[1:], check_value, url_path.strip())

                except Exception:
                    logger.warn("{} is invalid".format(line))

    def exists(self, _path):
        raise NotImplementedError
