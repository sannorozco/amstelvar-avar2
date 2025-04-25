# menuTitle: set features in all parametric sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)

preflight = False

assert os.path.exists(sourcesFolder)

sources = glob.glob(f'{sourcesFolder}/*.ufo')

fea = f'include (features/{familyName}-{subFamilyName}.fea);'
 
for sourcePath in sources:
    f = OpenFont(sourcePath, showInterface=False)
    fontName = os.path.splitext(os.path.split(sourcePath)[-1])[0]
    print(f'setting features in {fontName}...')
    if not preflight:
        f.features.text = fea
        print('saving...\n')
        f.save()
