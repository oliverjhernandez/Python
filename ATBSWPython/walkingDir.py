#!/usr/local/bin/python3
# Simple file/dirs organizer


import zipfile, shutil, os

for folderName, subFolders, filenames in os.walk("/Users/olhernandez/MEGAsync"):
    print("The current folder is " + folderName)
    for subFolder in subFolders:
        print("    Subfolder of " + folderName + ": " + subFolder)
    for filename in filenames:
        print("        File inside " + folderName + ': ' + filename)

newZip = zipfile.ZipFile('/Users/olhernandez/Desktop/F5_JM-CL.zip', 'w')
newZip.write("/Users/olhernandez/Desktop/F5_JM-CL/",compress_type=zipfile.ZIP_DEFLATED)
namelist = newZip.namelist()
for i in namelist:
    print(i)

newZip.close()
