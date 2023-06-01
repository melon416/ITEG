"""
COPYRIGHT
All Rights Reserved.
The copyright notice above does not evidence any actual or intended
publication of source code.
"""

import subprocess, os, logging, re, subprocess, shutil
from sys import exit, argv

textFileName = ''

def nametr(inString, isFile=True, id = '', version=''):
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


def fullFileSource(filestore,inName):
  return  filestore + '/' + inName[0] + '/' +  inName[0:2] + '/' + inName[0:3] + '/' + inName[0:4] + '/' + inName

def zipFile(basedir, project, incident, type):
  os.chdir(basedir)
  if 'zip' == type:
    if os.path.exists(incident + '.zip'):
      os.unlink(incident + '.zip')
    subprocess.call(["/usr/bin/zip",'-r', incident + '.zip', project])
    shutil.move(incident + '.zip', '/EDWExtract')
  elif 'tgz' == type:
    if os.path.exists(incident + '.tgz'):
      os.unlink(incident + '.tgz')
    subprocess.call(["/bin/tar",'-czf', incident + '.tgz', project])
    shutil.move(incident + '.tgz', '/EDWExtract')


def initTxt(fname):
  global textFileName
  textFileName = fname
  with open(fname,'w') as f:
    f.write('folder-id\tparent-folder-id\tdoc-id\ttitle\tfiltered-title\tfile-name\tdisk-file-name\tstatus\r\n')

def appendTxtFolder(folderid, parentfolder, title, filteredtitle):
  global textFileName
  title = re.sub('[\t]', ' ',title)
  with open(textFileName,'a') as f:
    f.write(folderid +\
            '\t'     +\
            parentfolder +\
            '\t'     +\
            '\t'     +\
            title    +\
            '\t'     +\
            filteredtitle +\
            '\t'     +\
            '\t'     +\
            '\t'     +\
            '\t\r\n' )

def appendTxtFile(docid, title, filteredtitle, filename, diskfile, status):
  global textFileName
  title = re.sub('[\t]', ' ', title)
  with open(textFileName,'a') as f:
    f.write('\t'     +\
            '\t'     +\
            docid +\
            '\t'     +\
            title    +\
            '\t'     +\
            filteredtitle +\
            '\t'     +\
            filename +\
            '\t'     +\
            diskfile +\
            '\t'     +\
            status   +\
            '\t\r\n' )

