# -*- coding: utf-8 -*-

import os
import shlex, subprocess
import hashlib

def filelist(dirname):
    """ 指定したディレクトリ配下のファイルとそのディレクトリを返す

        Args:
            dirname: ディレクトリ
        Returns:
            ファイル名とディレクトリ名を返すイテレータ
    """
    for root, dirs, files in os.walk(dirname):
        for f in files:
            fpathname = os.path.join(root, f)
            if os.path.isfile(fpathname):
                yield f, root


def exec_cmd(cmd, cwd=None):
    """ シェルコマンドを実行する

        Args:
            cmd: シェルコマンド
        Returns:
            (標準出力, 標準エラー出力)のタプル
    """
    args = shlex.split(cmd)
    opts = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'cwd': cwd, }
    p = subprocess.Popen(args, **opts)
    return p.communicate()


def get_sha1(filename):
    """ ファイルのハッシュ値(sha1)を返す

        Args:
            filename: ファイル名
        Returns:
            ハッシュ値(文字列)
    """
    fp = open(filename, 'rb')
    sha1 = hashlib.sha1(fp.read()).hexdigest()
    fp.close()
    return sha1

def get_related_path(base_dir, abs_path):
    """ 引数で渡された相対パスをbase_dirからの相対パスに変換する

        Args:
            base_dir: プロジェクトのベースディレクトリ
            abs_path: 絶対パスで表されたディレクトリ
        Returns
            相対パス化されたディレクトリ abs_path = base_dir + related_path
            abs_pathがbase_dirを含まない場合はabs_pathをそのまま返す
    """
    print abs_path, base_dir
    if abs_path.startswith(base_dir):
        path = abs_path.replace(base_dir, "")
        if path.startswith('/'):
            path = path[1:]
    else:
        path = abs_path
    return path
