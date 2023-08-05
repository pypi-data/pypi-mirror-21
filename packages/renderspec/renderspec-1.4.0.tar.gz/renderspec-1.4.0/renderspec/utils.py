#!/usr/bin/python
# Copyright (c) 2017 SUSE Linux GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

from contextlib import contextmanager
from email.parser import HeaderParser
import os
import shutil
import tarfile
import tempfile
import zipfile

import six


@contextmanager
def _extract_archive_to_tempdir(archive_filename):
    """extract the given tarball or zipfile to a tempdir.
    Delete the tempdir at the end"""
    if not os.path.exists(archive_filename):
        raise Exception("Archive '%s' does not exist" % (archive_filename))

    tempdir = tempfile.mkdtemp(prefix="renderspec_")
    try:
        if tarfile.is_tarfile(archive_filename):
            with tarfile.open(archive_filename) as f:
                f.extractall(tempdir)
        elif zipfile.is_zipfile(archive_filename):
            with zipfile.ZipFile(archive_filename) as f:
                f.extractall(tempdir)
        else:
            raise Exception("Can not extract '%s'. "
                            "Not a tar or zip file" % archive_filename)
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


def _find_archives(directories, basename):
    """return a list of archives in the given directories
    or an empty list if no archive(s) can be found"""
    if isinstance(directories, six.string_types):
        directories = [directories]

    return [f for d in directories for f in os.listdir(d)
            if f.startswith(basename) and
            f.endswith(('tar.gz', 'zip', 'tar.bz2', 'xz'))]


def _find_pkg_info(directory):
    """find and return the full path to a PKG-INFO file or None if not found"""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename == 'PKG-INFO':
                return os.path.join(root, filename)
    # no PKG-INFO file found
    return None


def _get_version_from_pkg_info(pkg_info_filename):
    """get the version from a PKG-INFO (see pep-0314) file"""
    with open(pkg_info_filename, 'r') as f:
        parser = HeaderParser()
        headers = parser.parse(f)
        return headers.get('version')
