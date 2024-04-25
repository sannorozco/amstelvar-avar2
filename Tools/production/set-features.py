# menuTitle: include external features in parametric sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)

assert os.path.exists(sourcesFolder)

sources = glob.glob(f'{sourcesFolder}/*.ufo')

fea = f'include (features/{familyName}-{subFamilyName}.fea);'
 
for sourcePath in sources:
    f = OpenFont(sourcePath, showInterface=False)
    f.features.text = fea
    f.save()
