# -*- coding: utf-8 -*-
"""
指定したディレクトリを走査し、画像ファイル情報をDBへ登録する。

"""

import os

import MySQLdb

import utils

IMAGE_FILE_EXTS = (
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
)

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'blogwatcher'
DB_PASS = 'blogwatcher!'
DB_NAME = 'opencv'
IMAGE_TABLE = 'devel_image'

def main(dirname):
    conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT,
                           user=DB_USER, passwd=DB_PASS,
                           db=DB_NAME, charset='utf8')
    for filename, directory in utils.filelist(dirname):
        root, ext = os.path.splitext(filename)
        if ext.lower() in IMAGE_FILE_EXTS:
            fpathname = os.path.join(directory, filename)
            hash = utils.get_sha1(fpathname)
            if image_exists(conn, hash):
                print "%s exists" % fpathname
                continue
            insert_image(conn, filename, directory, hash)


def image_exists(conn, hash):
    sql = 'SELECT id FROM %s WHERE hash = %%s' % IMAGE_TABLE
    result = exec_sql(conn, sql, hash)
    if result:
        return True
    else:
        return False


def insert_image(conn, filename, dirname, hash):
    sql = """INSERT INTO %s
                (name, directory, hash, status)
             VALUES
                (%%s, %%s, %%s, %%s)""" % IMAGE_TABLE
    vals = (filename, dirname, hash, 1)
    exec_sql(conn, sql, vals)


def exec_sql(conn, sql, vals=None):
    cursor = None
    try:
        if vals:
            if not isinstance(vals, (tuple, list)):
                vals = [vals]
        cursor = conn.cursor()
        cursor.execute(sql, vals)
        rows = []
        for row in cursor:
            rows.append(row)
        return rows
    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
