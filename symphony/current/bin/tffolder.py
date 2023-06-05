"""
COPYRIGHT
All Rights Reserved.
The copyright notice above does not evidence any actual or intended
publication of source code.
"""

import cx_Oracle
import sys
import tfdoc
import logging
import tfutil
import os

class tffolder:
    _fldrDict = {}

    def __init__(self, con, project, filestore, fpath, id='', parent_id=''):
        csr = con.cursor()

        if '' == id:
            csr.execute("select ID, PARENT_FOLDER_ID, TITLE,PATH from sym_sourceforge_schema.folder where project_id = 'proj" + str(project) + "' and is_deleted = 0 and id like 'docf%' and path='docman.root'")
            res = csr.fetchone()
            id = res[0]
        else:
            csr.execute("select ID, PARENT_FOLDER_ID, TITLE,PATH from sym_sourceforge_schema.folder where project_id = 'proj" + str(project) + "' and is_deleted = 0 and id = '" + id + "'")
            res = csr.fetchone()
        #
        #
        #
        if os.path.exists(fpath + '/' + tfutil.nametr(res[2], False)):
            os.makedirs(fpath + '/' + tfutil.nametr(res[2], False, id))
            logging.info('id:  ' + id + ' parent_folder_id:  ' + parent_id + ' title:  ' + res[2] + ' altered_title:  ' + tfutil.nametr(res[2], False, id) + ' path:  ' + res[3])
            tfutil.appendTxtFolder(id, parent_id, res[2], tfutil.nametr(res[2], False, id))
        else:
            os.makedirs(fpath + '/' + tfutil.nametr(res[2], False))
            logging.info('id:  ' + id + ' parent_folder_id:  ' + parent_id + ' title:  ' + res[2] + ' altered_title:  ' + tfutil.nametr(res[2], False) + ' path:  ' + res[3])
            tfutil.appendTxtFolder(id, parent_id, res[2], tfutil.nametr(res[2], False))
        #
        # Process files first
        #
        csr2 = con.cursor()
        csr2.execute("select ID, Title from sym_sourceforge_schema.item  where folder_id = '" + id + "' and is_deleted=0")
        for doco in csr2.fetchall():
            tfdoc.tfdoc(con, doco, filestore, fpath + '/' + tfutil.nametr(res[2], False))
        #
        #  Process folders second
        #
        csr.execute("select distinct ID, PARENT_FOLDER_ID, TITLE,PATH from sym_sourceforge_schema.folder where project_id = 'proj" + str(project) + "' and is_deleted = 0 and id like 'docf%' and parent_folder_id = '" + id + "'")
        for item in csr.fetchall():
            tffolder(con, project, filestore, fpath + '/' + tfutil.nametr(res[2]), item[0], id)
