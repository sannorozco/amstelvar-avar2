import os, glob

familyName    = 'Amstelvar2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.getcwd())
sourcesFolder = os.path.join(baseFolder, 'TechAlpha', subFamilyName)
extremaFolder = os.path.join(sourcesFolder, 'extrema')

# set feature in parametric sources

assert os.path.exists(sourcesFolder)

sources = glob.glob(f'{sourcesFolder}/*.ufo')

fea = f'include (features/{familyName}-{subFamilyName}.fea);'
 
for sourcePath in sources:
    f = OpenFont(sourcePath, showInterface=False)
    f.features.text = fea
    f.save()

# set feature in extrema sources

assert os.path.exists(extremaFolder)

sources = glob.glob(f'{extremaFolder}/*.ufo')

fea = f'include (../features/{familyName}-{subFamilyName}.fea);'

for sourcePath in sources:
    f = OpenFont(sourcePath, showInterface=False)
    f.features.text = fea
    f.save()
