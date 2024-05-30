# make sure that the VariableValues module is installed
import sys
modulePath = '/Users/gferreira/hipertipo/tools/variable-values/code/Lib'
if modulePath not in sys.path:
    sys.path.append(modulePath)
from importlib import reload
import variableValues.glyphSetProofer
reload(variableValues.glyphSetProofer)

import os, glob, time
from variableValues.glyphSetProofer import GlyphSetProofer

familyName      = 'AmstelvarA2'
subFamily       = ['Roman', 'Italic'][0]
proofsFolder    = os.path.dirname(os.getcwd())
baseFolder      = os.path.dirname(proofsFolder)
sourcesFolder   = os.path.join(baseFolder, 'Sources', subFamily)
defaultFontPath = os.path.join(sourcesFolder, f'{familyName}-{subFamily}_wght400.ufo')
sourcePaths     = sorted(glob.glob(f'{sourcesFolder}/*.ufo'))
sourcePaths.remove(defaultFontPath)

# sourcePaths = sourcePaths[7:9]

start = time.time()

P = GlyphSetProofer(f'{familyName} {subFamily}', defaultFontPath, sourcePaths)
P.build(savePDF=True)

end = time.time()

print(f'total build time: {end - start:.2f} seconds\n')
