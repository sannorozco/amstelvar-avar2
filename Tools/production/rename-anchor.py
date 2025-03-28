# menuTitle: rename anchor in all sources

import os, glob, shutil

familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)

glyphName     = 'z'
oldAnchorName = 'liga'
newAnchorName = '_liga'

sources = glob.glob(f'{sourcesFolder}/*.ufo')

print(f'renaming anchors in all {familyName} {subFamilyName} sources:')
for sourcePath in sources:
    f = OpenFont(sourcePath, showInterface=False)
    g = f[glyphName]
    for a in g.anchors:
        if a.name == 'liga':
            print(f'\trenaming anchor in {f.info.styleName}...')
            a.name = '_liga'
    f.save()

print('...done!\n')
