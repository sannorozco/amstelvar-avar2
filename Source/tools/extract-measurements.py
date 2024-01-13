# menuTitle: extract measurements

import os, glob, json
from variableValues.measurements import FontMeasurements

familyName       = 'Amstelvar2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.getcwd())
sourcesFolder    = os.path.join(baseFolder, 'TechAlpha', subFamilyName)
extremaFolder    = os.path.join(sourcesFolder, 'extrema')
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')

assert os.path.exists(measurementsPath)

ufos = [
    'Amstelvar-Roman_opsz8.ufo', 
    'Amstelvar-Roman_opsz144.ufo',
]

measurements = {}

for ufo in ufos:
    ufoPath = os.path.join(extremaFolder, ufo)
    assert os.path.exists(ufoPath)

    fontName = os.path.splitext(os.path.split(ufoPath)[-1])[0]
    styleName = fontName.split('_')[-1]

    f = OpenFont(ufoPath, showInterface=False)

    M = FontMeasurements()
    M.read(measurementsPath)
    M.measure(f)

    measurements[styleName] = M.values


print(measurements)


# # save blends in JSON format

# jsonPath = os.path.join(ufosFolder, 'blends.json')

# with open(jsonPath, 'w', encoding='utf-8') as f:
#     json.dump(measurements, f, indent=2)
