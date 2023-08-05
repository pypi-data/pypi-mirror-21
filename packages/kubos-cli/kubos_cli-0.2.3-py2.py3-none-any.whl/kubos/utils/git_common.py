# Kubos SDK
# Copyright (C) 2016 Kubos Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import git
import os

KUBOS_SRC_URL = 'https://github.com/kubostech/kubos'
KUBOS_EXAMPLE_URL = 'https://github.com/kubostech/kubos-rt-example'
HOME_DIR = os.path.expanduser('~')
KUBOS_DIR = os.path.join(HOME_DIR, '.kubos')
KUBOS_SRC_DIR = os.path.join(KUBOS_DIR, 'kubos')
KUBOS_EXAMPLE_DIR = os.path.join(KUBOS_DIR, 'example')

KUBOS_GIT_DIR = os.path.join(KUBOS_SRC_DIR, '.git')
KUBOS_VERSION_FILE = os.path.join(KUBOS_DIR, 'version.txt')

def get_repo(path):
    repo = git.Repo(path)
    origin = repo.remotes.origin
    return repo, origin


def get_active_kubos_version():
    if os.path.isfile(KUBOS_VERSION_FILE):
        return open(KUBOS_VERSION_FILE).read()
    else:
        return None


def checkout(tag, repo):
    try:
        repo.git.checkout(tag.name)
        if repo.git_dir == os.path.join(KUBOS_SRC_DIR, '.git'): #only set the version file for kubos source checkouts, not for example checkouts
            with open(KUBOS_VERSION_FILE, 'w') as version_file:
                version_file.write(tag.name)
    except:
        print 'There was an error checking out the tag "%s"' % tag.name
        print 'The error details are: \n\n%s' %  sys.exc_info()[0]

def fetch_tags(repo):
    origin = repo.remotes.origin
    tag_list = []
    latest_tag = ""
    print 'Checking for newer releases...' #Tags mark new KubOS releases
    origin.fetch(tags=True)

