import os, glob, shutil

subFamily     = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamily)

parentAxes = {
    # 'XOPQ' : ('XOUC', 'XOLC', 'XOFI'), 
    'YOPQ' : ('YOUC', 'YOLC', 'YOFI'), 
    # 'XTRA' : ('XTUC', 'XTLC', 'XTFI'), 
}

deleteParent = True

for parentAxis, childAxes in parentAxes.items():
    parentPaths = [f for f in glob.glob(f'{sourcesFolder}/*.ufo') if parentAxis in os.path.split(f)[-1]]
    # create child sources as duplicates of parent source
    for parentPath in parentPaths:
        for childAxis in childAxes:
            childPath = parentPath.replace(parentAxis, childAxis)
            shutil.copytree(parentPath, childPath)
    # remove parent source
    if deleteParent:
        shutil.rmtree(parentPath)
