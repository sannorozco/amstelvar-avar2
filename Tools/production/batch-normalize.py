# menuTitle: batch normalize all sources

import os, glob
from mojo.UI import getDefault, setDefault, preferencesChanged

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
normalizeMode = 1

normalizeModeOld = getDefault("shouldNormalizeOnSave")

if normalizeModeOld != normalizeMode:
    setDefault("shouldNormalizeOnSave", normalizeMode)

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

print('batch normalizing UFOs...\n')

for ufoPath in ufoPaths:
    f = OpenFont(ufoPath, showInterface=False)
    print(f'\tnormalizing {os.path.split(ufoPath)[-1]}...')
    f.save()

if normalizeModeOld != normalizeMode:
    setDefault("shouldNormalizeOnSave", normalizeModeOld)
    
print()
print('...done.\n')

