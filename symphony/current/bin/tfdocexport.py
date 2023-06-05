"""
COPYRIGHT
All Rights Reserved.
The copyright notice above does not evidence any actual or intended
publication of source code.
"""

import cx_Oracle
import os
import sys
import getpass
import re
from optparse import OptionParser
import logging
import tffolder
import tfutil

def init():
    # Parse Parms.
    parser = OptionParser('usage: %prog [options] arg')
    parser.add_option("--project", dest='project', action='store', type='string', default='', help='The Symphony project name to be exported.')
    parser.add_option('--DBUser', dest='dbuser', action='store', type='string', default='', help='The name to use when connecting to the database.')
    parser.add_option('--targetdir', dest='targetdir', action='store', type='string', default='/tmp', help='The base path for the target directory.')
    parser.add_option('--incident', dest='incident', action='store', type='string', default='', help='The PDSM Incident being worked.')
    parser.add_option('--type', dest='type', action='store', type='string', default='zip', help='The type of zip to produce either "zip" or "tgz" - defaults to "zip".')
    parser.add_option('--filestore', dest='filestore', action='store', type='string', default='/var/fedex/teamforge/filestorage', help='The path to the TeamForge filestore directory.  DEFAULTS TO:  /var/fedex/teamforge/filestorage')
    parser.add_option('--DBSchema', dest='dbschema', action='store', type='string', default='SYM_SYMPHONY_SVC_PRD', help='DEFAULTS TO:  SYM_SYMPHONY_SVC_PRD')

    (options, args) = parser.parse_args()

    if (len(options.project) == 0) or (len(options.dbuser) == 0) or (len(options.incident) == 0):
        print("all of these:   --project and --DBUser are required and --incident")
        parser.print_help()
        sys.exit(1)
    if options.type not in {'zip', 'tgz'}:
        print("type can only be one of 'tgz' or 'zip'")
        parser.print_help()
        sys.exit(1)
    if re.match('INC[0-9]+', options.incident) is None:
        print("Incidents start with INC and end with an integer 'INC00000'")
        parser.print_help()
        sys.exit(1)

    lclpass = getpass.getpass(options.dbuser + "'s Password: ")

    try:
        os.makedirs(options.targetdir + '/' + options.project)
    except:
        print('Could not create ' + options.targetdir + '/' + options.project)
        sys.exit(1)

    logging.basicConfig(format='%(asctime)s %(message)s', filename=options.targetdir + '/' + options.project + '/' + options.project + '.log', level=logging.DEBUG)
    logging.info('Beginning tfdocexport')
    logging.debug('Parameters are:')
    logging.debug('  filestore: ' + options.filestore)
    logging.debug('  targetdir: ' + options.targetdir)
    logging.debug('  dbuser:    ' + options.dbuser)
    logging.debug('  project:   ' + options.project)
    logging.debug('  incident:  ' + options.incident)
    logging.debug('  type    :  ' + options.type)
    logging.debug('  schema:    ' + options.dbschema)

    tfutil.initTxt(options.targetdir + '/' + options.project + '/' + options.project + '.txt')

    con = cx_Oracle.connect(options.dbuser + '/' + lclpass + '@' + options.dbschema)

    return {'connection': con, 'options': options}


def getProjectNumber(connection, projectName):
    csr = connection.cursor()

    operator = ''
    if re.search('%', projectName) is None:
        operator = '='
    else:
        operator = 'like'

    csr.execute(
        "select PROJECT_NBR, PROJECT_NM  from sym_symphony_schema.TOOL_PROJECT where TOOL_CD = 'SF' and PROJECT_NM " + operator + " '" + projectName + "'")
    res = csr.fetchall()

    csr.close()

    if len(res) > 1:
        print('Multiple items matched ' + projectName)
        print('Only one match is allowed.  Please be more specific.')
        print('Matches were:')
        for result in res:
            print("    " + str(result[0]) + " " + result[1])
        sys.exit(2)
    else:
        return res[0][0]


condict = init()
projnum = getProjectNumber(condict['connection'], condict['options'].project)

s = tffolder.tffolder(condict['connection'], projnum, condict['options'].filestore, condict['options'].targetdir + '/' + condict['options'].project)

tfutil.zipFile(condict['options'].targetdir, condict['options'].project, condict['options'].incident, condict['options'].type)
