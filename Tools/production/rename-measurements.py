# menuTitle : rename glyph measurements

import os, json
from xTools4.modules.measurements import readMeasurements

subFamilyName    = ['Roman', 'Italic'][1]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources')
measurementsPath = os.path.join(sourcesFolder, subFamilyName,  'measurements.json')

assert os.path.exists(measurementsPath)

glyphNames = [
    'dollar',
    'cent',
    'sterling',
]

renameDict = {
    'XOPQ' : 'XOFI',
    'YOPQ' : 'YOFI',
    'XTRA' : 'XTFI',
    'YTOS' : 'YTFO',
}

measurements = readMeasurements(measurementsPath)

print(f"renaming glyph measurements...\n")

for glyphName in glyphNames:
    print(f"\trenaming measurements in /{glyphName}...")
    if glyphName not in measurements['glyphs']:
        continue

    glyphMeasurements = {}
    for ID, m in measurements['glyphs'][glyphName].items():
        if m['name'] in renameDict:
            newName = renameDict[m['name']]
            print(f"\t\trenaming {m['name']} to {newName}...")
            glyphMeasurements[ID] = {
                'name'      : newName,
                'direction' : m['direction'],
            }
        else:
            glyphMeasurements[ID] = m

    measurements['glyphs'][glyphName] = glyphMeasurements
    print()

print('\tsaving measurements...')
with open(measurementsPath, 'w', encoding='utf-8') as f:
    json.dump(measurements, f, indent=2)

print('...done.')

