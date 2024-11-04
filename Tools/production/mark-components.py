# menuTitle: apply validation colors to sources

from importlib import reload
import xTools4.modules.validation
reload(xTools4.modules.validation)

import os, glob
from xTools4.modules.validation import *

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

assert os.path.exists(sourcePath)

colors = {
    'components'      : (1.00, 0.30, 0.00, 0.35),
    'componentsEqual' : (1.00, 0.65, 0.00, 0.35),
    'default'         : (0.00, 0.65, 1.00, 0.35),
    'warning'         : (1.00, 0.00, 0.00, 0.65),
}

dstFonts = [] # 'XOPQ310 XSHL0 XSHL136 XSHU144 XSHU2 XSVF126 XSVF6 XSVL0 XSVL130 XSVU0 XSVU124 XTRA63 XTRA650 XTTW0 XTTW30 XUCS114 XUCS259'.split()
    
preflight = False

sourceFont = OpenFont(sourcePath, showInterface=False)
ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == sourcePath:
        continue

    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:

        dstFont = OpenFont(ufoPath, showInterface=False)

        print(f'applying mark colors to {os.path.split(ufoPath)[-1]}...')
        applyValidationColors(dstFont, sourceFont, colors)

        if not preflight:
            dstFont.save()

        # dstFont.close()
