# Copyright (c) Trainline Limited, 2017. All rights reserved. See LICENSE.txt in the project root for license information.

import json
import os
import errno

from builtins import str
from codecs import open
from hashlib import sha1
from appdirs import user_data_dir
from envmgr.commands.utils.file_utils import safe_create_dir_path

class PatchFile(object):

    @staticmethod
    def get_filepath(cluster, env):
        app_dir = user_data_dir('envmgr', 'trainline')
        filename = 'patch_{0}_{1}'.format(cluster.lower(), env.lower())
        filename = '{0}.json'.format(sha1(filename.encode('utf-8')).hexdigest())
        return os.path.join(app_dir, filename)

    @staticmethod
    def get_contents(cluster, env):
        patch_file = PatchFile.get_filepath(cluster, env)
        if os.path.exists(patch_file):
            with open(patch_file, encoding='utf-8') as file_data:
                return json.load(file_data)
        else:
            return None

    @staticmethod
    def exists(cluster, env):
        return PatchFile.get_contents(cluster, env) is not None

    @staticmethod
    def write_content(cluster, env, content):
        filepath = PatchFile.get_filepath(cluster, env)
        with PatchFile.safe_open_w(filepath) as f:
            f.write(str(json.dumps(content, ensure_ascii=False)))
    
    @staticmethod
    def safe_open_w(filepath):
        safe_create_dir_path(filepath)
        return open(filepath, 'w', encoding='utf-8')

    @staticmethod
    def write_report(cluster, env):
        content = PatchFile.get_contents(cluster, env)
        filepath = os.path.join(os.getcwd(), 'patch_report_{0}_{1}.json'.format(cluster, env))
        with PatchFile.safe_open_w(filepath) as f:
            f.write(str(json.dumps(content, ensure_ascii=False)))
        return filepath

    @staticmethod
    def delete(cluster, env):
        os.remove(PatchFile.get_filepath(cluster, env))

