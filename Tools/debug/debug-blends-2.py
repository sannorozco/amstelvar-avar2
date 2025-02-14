# menuTitle: compare AmstelvarA2 instances against Amstelvar

import os, glob, datetime

subFamilyName = ['Roman', 'Italic'][0]

familyName1      = 'AmstelvarA2'
baseFolder1      = os.path.dirname(os.path.dirname(os.getcwd()))
instancesFolder1 = os.path.join(baseFolder1, 'Fonts', 'instances')
instances1       = glob.glob(f'{instancesFolder1}/*.ufo')

familyName2      = 'Amstelvar'
baseFolder2      = os.path.join(os.path.dirname(baseFolder1), 'amstelvar')
instancesFolder2 = os.path.join(baseFolder2, subFamilyName)
instances2       = glob.glob(f'{instancesFolder2}/*.ufo')
for i in instances2:
    fileName = os.path.split(i)[-1]
    if 'GRAD' in fileName or 'wght400' in fileName:
        instances2.remove(i)

# instanceNames1 = []
_instances1 = {}
for i in instances1:
    instanceName = ' '.join(os.path.splitext(os.path.split(i)[1])[0].split('_')[2:])
    _instances1[instanceName] = i

# instanceNames2 = []
_instances2 = {}
for i in instances2:
    instanceName = ' '.join(os.path.splitext(os.path.split(i)[1])[0].split('_')[1:])
    _instances2[instanceName] = i

print(len(_instances1), len(_instances2))
print()

print('instances in Amstelvar and NOT in AmstelvarA2:')
missingInstances = set(_instances2.keys()).difference(set(_instances1.keys()))
for i in sorted(missingInstances):
    print(f'\t{i}')
print()
    
proofInstances = [
    'wght100',
    'wght1000',
    'opsz8_wght100',
    'opsz8_wght1000',
    'opsz144_wght100',
    'opsz144_wght1000',
]

controlGlyphs = ['H', 'n', 'zero']

fs = 120              # font size
p  = 25, 10, 10, 10   # padding

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for instanceName in proofInstances:
    instancePath1 = os.path.join(instancesFolder1, f'AmstelvarA2-{subFamilyName}_avar2_{instanceName}.ufo')
    instancePath2 = os.path.join(instancesFolder2, f'Amstelvar-{subFamilyName}_{instanceName}.ufo')
    instance1 = OpenFont(instancePath1, showInterface=False)
    instance2 = OpenFont(instancePath2, showInterface=False)
    print(instance1)
    for glyphName in controlGlyphs:
        newPage('A4Landscape')
        with savedState():
            x1 = p[3]
            x2 = width() / 2
            x3 = width() - p[1]
            y1 = height() - p[0]*0.57
            y2 = p[0]*0.57
            font('Menlo')
            fontSize(7)
            text(f'{instanceName}', (x1, y1), align='left')            
            text(glyphName, (x2, y1), align='center')
            text(f'{now}', (x3, y1), align='right')

            text(f'AmstelvarA2 {subFamilyName}', (width()*0.25, y2), align='center')            
            text(f'Amstelvar {subFamilyName}', (width()*0.75, y2), align='center')            


        g1 = instance1[glyphName]
        g2 = instance2[glyphName]
        print(glyphName, g1, g2)
    print(instance2)
    print()



