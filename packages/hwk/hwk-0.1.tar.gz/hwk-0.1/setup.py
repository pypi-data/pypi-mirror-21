#!/usr/bin/env python

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

from distutils.core import setup

VERSION = 0.1
URL = 'https://github.com/jaypipes/hwk'
DOWNLOAD_URL = '%s/archive/%s.tar.gz' % (URL, VERSION)
DESCRIPTION = (
    "The HardWare toolKit - A small Python library containing hardware "
    "discovery and configuration tools"
)

setup(
    name='hwk',
    version=str(VERSION),
    description=DESCRIPTION,
    author='Jay Pipes',
    author_email='jaypipes@gmail.com',
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=['hwk'],
)
