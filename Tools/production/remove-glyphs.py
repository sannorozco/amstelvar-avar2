# menuTitle: remove glyphs from all sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
ufoPaths      = glob.glob(f'{sourcesFolder}/*.ufo')
glyphNames    = [
    'dieresistonoscomb.case',
    'dieresistonos.case',
]

for ufoPath in ufoPaths:
    f = OpenFont(ufoPath, showInterface=False)
    print(f'removing glyphs in {ufoPath}...')
    for glyphName in glyphNames:
        if glyphName not in f:
            continue
        print(f'\tremoving {glyphName}...')
        del f[glyphName]
    f.save()
    f.close()
    print()
