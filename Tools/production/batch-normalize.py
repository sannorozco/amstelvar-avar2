# menuTitle: batch normalize all sources

import os, glob
from ufonormalizer import normalizeUFO

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

print('batch normalizing UFOs...\n')

for ufoPath in ufoPaths:
    print(f'\tnormalizing {os.path.split(ufoPath)[-1]}...')
    normalizeUFO(ufoPath, onlyModified=False, writeModTimes=False)
    
print()
print('...done.\n')

