# menuTitle: copy glyph order from Roman default to Italic default

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
defaultName   = 'wght400'
defaultPath   = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{defaultName}.ufo')

assert os.path.exists(defaultPath)

defaultFont = OpenFont(defaultPath, showInterface=False)
ufoPaths    = glob.glob(f'{sourcesFolder}/*.ufo')

print('copying default groups to all other sources...')

for ufoPath in ufoPaths:
    if ufoPath == defaultPath:
        continue

    f = OpenFont(ufoPath, showInterface=False)
    fontName = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    print(f'\tcopying groups to {fontName}...')
    f.groups.clear()
    f.groups.update(defaultFont.groups)
    f.save()

print('...done.\n')
