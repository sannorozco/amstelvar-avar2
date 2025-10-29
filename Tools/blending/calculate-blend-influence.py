import os, json
from fontTools.designspaceLib import DesignSpaceDocument

baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
designspacePath  = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}_avar2.designspace')
defaultPath      = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}_wght400.ufo')
blendsPath       = os.path.join(sourcesFolder, 'blends.json')

with open(blendsPath, 'r', encoding='utf-8') as f:
    blendsData = json.load(f)

designspace = DesignSpaceDocument()
designspace.read(designspacePath)

axes = {}
for axis in designspace.axes:
    axes[axis.tag] = {
        'maximum' : axis.maximum,
        'minimum' : axis.minimum,
        'default' : axis.default,
    }

for srcName in blendsData['sources'].keys():
    if 'XTSP' in srcName:
        continue
    print(srcName)
    for axisName, axisValue in blendsData['sources'][srcName].items():
        print(f'\t{axisName} {axisValue}')
    print()
