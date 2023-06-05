"""
COPYRIGHT
All Rights Reserved.
The copyright notice above does not evidence any actual or intended
publication of source code.
"""

import subprocess
import os
import logging
import re
import subprocess
import shutil
import sys

textFileName = ''

def nametr(inString, isFile=True, id='', version=''):
    version = str(version)
    allowed_chars = 'a-zA-Z0-9_&* .\[\]\(\)\{\}-'
    basetr = re.sub('[^'+allowed_chars+']+','~',inString)
    if isFile:
        mobj = re.match('(.*)\.(.*)', basetr)
        if mobj:
            basfn = mobj.group(1)
            if len(version) > 0:
                basfn += '_' + version
            if len(id) > 0:
                basfn += '_' + id
            basetr = basfn + '.' + mobj.group(2)
        else:
            if len(version) > 0:
                basetr += '_' + version
            if len(id) > 0:
                basetr += '_' + id
    else:
        if len(version) > 0:
            basetr = version + '_' + basetr
        if len(id) > 0:
            basetr = id + '_' + basetr
    return basetr


def fullFileSource(filestore, inName):
    return filestore + '/' + inName[0] + '/' + inName[0:2] + '/' + inName[0:3] + '/' + inName[0:4] + '/' + inName


def zipFile(basedir, project, incident, fileType):
    os.chdir(basedir)
    if 'zip' == fileType:
        if os.path.exists(incident + '.zip'):
            os.unlink(incident + '.zip')
        subprocess.call(["/usr/bin/zip", '-r', incident + '.zip', project])
        shutil.move(incident + '.zip', '/EDWExtract')
    elif 'tgz' == fileType:
        if os.path.exists(incident + '.tgz'):
            os.unlink(incident + '.tgz')
        subprocess.call(["/bin/tar", '-czf', incident + '.tgz', project])
        shutil.move(incident + '.tgz', '/EDWExtract')


def initTxt(fname):
    global textFileName
    textFileName = fname
    with open(fname, 'w') as f:
        f.write('folder-id\tparent-folder-id\tdoc-id\ttitle\tfiltered-title\tfile-name\tdisk-file-name\tstatus\r\n')


def appendTxtFolder(folderId, parentFolder, title, filteredTitle):
    global textFileName
    title = re.sub('[\t]', ' ', title)
    with open(textFileName, 'a') as f:
        f.write(folderId + '\t' + parentFolder + '\t' + '\t' + title + '\t' + filteredTitle + '\t' + '\t' + '\t' + '\t\r\n')


def appendTxtFile(docId, title, filteredTitle, filename, diskFile, status):
    global textFileName
    title = re.sub('[\t]', ' ', title)
    with open(textFileName, 'a') as f:
        f.write('\t' + '\t' + docId + '\t' + title + '\t' + filteredTitle + '\t' + filename + '\t' + diskFile + '\t' + status + '\t\r\n')
