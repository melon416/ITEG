"""
COPYRIGHT
All Rights Reserved.
The copyright notice above does not evidence any actual or intended
publication of source code.
"""
import cx_Oracle
import os
import sys
import logging
import tfutil
import shutil


class tfdoc:
    _docDict = {}
    _walkVersionTree_iter = {}

    def __init__(self, con, doc, filestore, destpath):
        csr = con.cursor()
        #
        #
        #
        csr = con.cursor()
        csr.execute(
            "select ID, version, status, stored_file_id, stored_file_url from sym_sourceforge_schema.document_version where document_id = '" +
            doc[0] + "' order by id,version")
        logging.info('Document:  ' + doc[0] + ' Title:  ' + doc[1])
        for dv in csr.fetchall():
            isFile = False
            if dv[4] is None:
                #
                #  This is a file
                #
                isFile = True
                csr2 = con.cursor()
                csr2.execute("select raw_file_id, file_name from sym_sourceforge_schema.stored_file where id = '" + dv[
                    3] + "' and is_deleted = 0")
                for rfi in csr2.fetchall():
                    diskTargetName = tfutil.nametr(rfi[1], True, dv[0], dv[1])
                    logging.info('docid:  ' + doc[0] + ' version:  ' + str(dv[1]) + ' stored_file_id :  ' + dv[3] + ' docv_id:  ' + str(dv[0]) + ' raw_file_id:  ' + rfi[1] + ' disk_file_name:  ' + diskTargetName + ' status:  ' + dv[2])
                    shutil.copyfile(tfutil.fullFileSource(filestore, rfi[0]), destpath + '/' + diskTargetName)
                    tfutil.appendTxtFile(doc[0], doc[1], '', rfi[0], diskTargetName, dv[2])
            else:
                diskTargetName = tfutil.nametr(dv[4], False, dv[0], dv[1])
                logging.info('docid:  ' + doc[0] + ' version:  ' + str(dv[1]) + ' docv_id:  ' + 'None' + ' url:  ' + dv[4] + ' munged_file_name:  ' + diskTargetName + ' status:  ' + dv[2])
                tfutil.appendTxtFile(doc[0], doc[1], '', '', diskTargetName, dv[2])
                open(destpath + '/' + diskTargetName, 'w').close()
