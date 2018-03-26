#!/usr/local/bin/python3
# Rename filenames with american style dates MM-DD-YYYY to european style dates DD-MM-YYYY.

import shutil, os, re

datePattern = re.compile(r"""^(.*?)((0|1)?\d)-((0|1|2|3)?\d)-((19|20)?\d\d)(.*?)$""", re.VERBOSE)
#zeroPattern = re.compile(r"""^(.*?)(0?)(.*?)$""", re.VERBOSE)

# TODO: Loop over the files in the working directory.

for amerFile in os.listdir('/somedir'):
    mo = datePattern.search(amerFile)
    if mo == None:
        continue
    before = mo.group[1]
    month  = mo.group[2]
    day    = mo.group[4]
    year   = mo.group[6]
    after  = mo.group[8]

    euroFile = before + day + '-' + month + '-' +  year + after

    absWorkingDir = os.path.abspath('.')
    amerFile = os.path.join(absWorkingDir, amerFile)
    euroFile = os.path.join(absWorkingDir, euroFile)

    print('Renaming "%s" to "%s" ...' % (amerFile, euroFile))
    shutil.move(amerFile, euroFile)





# TODO: Skip files without a date.
# TODO: Get the different parts of the filename.
# TODO: Form the European-style filename.
# TODO: Get the full, absolute file paths.
# TODO: Rename the files.
