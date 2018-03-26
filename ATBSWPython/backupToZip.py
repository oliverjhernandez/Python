#!/usr/local/bin/python3
# Creates compressed snapshots of a directory
import os, shutil, zipfile


def backupToZip(dir):
    dir = os.path.abspath(dir)
    n = 1
    while True:
        zipFilename = os.path.basename(dir) + '-' + str(n) + '.zip'
        if not os.path.exists(zipFilename):
            break
        n = n + 1
    print("Creating zip file %s..." % (zipFilename))
    backupZip = zipfile.ZipFile(zipFilename, 'w')

    for cwd, subds, files in os.walk(dir):
        print("Adding files in %s..." % (cwd))
        backupZip.write(cwd)
        for file in files:
            newBase = os.path.basename(file) + '_'
            if file.startswith(newBase) and file.endswith('.zip'):
                continue
            backupZip.write(os.path.join(cwd + '/' + file))
    backupZip.close()
    print('Done')



backupToZip("/Users/olhernandez/Desktop/F5_JM-CL")
