import os
from defcon import Font
from fontTools.designspaceLib import DesignSpaceDocument
from ufo2ft import compileVariableTTF
# from ufo2ft.featureWriters.kernFeatureWriter import KernFeatureWriter

familyName      = 'AmstelvarA2'
subFamilyName   = ['Roman', 'Italic'][0]
baseFolder      = os.path.dirname(os.getcwd())
sourcesFolder   = os.path.join(baseFolder, 'Parametric-avar2', subFamilyName)
designspacePath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}.designspace')
fontsFolder     = os.path.join(os.path.dirname(baseFolder), 'fonts', 'Parametric avar2 TTFs')
varFontPath     = designspacePath.replace(sourcesFolder, fontsFolder).replace('.designspace', '.ttf')

assert os.path.exists(designspacePath)
assert os.path.exists(fontsFolder)

print(f'generating variable font for {designspacePath}...')

D = DesignSpaceDocument()
D.read(designspacePath)
print(f'\tloading sources...')
for src in D.sources:
    src.font = Font(src.path)

print('\tbuilding variable font...')

### build variable font with ufo2ft
f = compileVariableTTF(D, featureWriters=[])
f.save(varFontPath)

print('...done.\n')

print(varFontPath, os.path.exists(varFontPath))
