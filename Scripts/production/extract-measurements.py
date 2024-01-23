# menuTitle: extract parametric blends from Amstelvar1 extrema

import os, glob, json
from variableValues.measurements import FontMeasurements

subfamilyName    = ['Roman', 'Italic'][0]
baseFolder1      = '/Users/gferreira/hipertipo/fonts/amstelvar' # path to Amstelvar1 sources for measuring - see http://github.com/gferreira/amstelvar
sourcesFolder1   = os.path.join(baseFolder1, subfamilyName)
measurementsPath = os.path.join(sourcesFolder1, 'measurements.json')
baseFolder2      = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder2   = os.path.join(baseFolder2, 'Sources', subfamilyName)
blendsPath       = os.path.join(sourcesFolder2, 'blends_full.json')
parametricAxes   = 'XOPQ XTRA YOPQ YTUC YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL XSHF YSHF XSVF YSVF XTTW YTTL YTOS XUCS'.split()

# define blended axes

blendedAxes = {
    "opsz": {
      "name"    : "Optical size",
      "default" : 14,
      "min"     : 8,
      "max"     : 144,
    },
    "wght": {
      "name"    : "Weight",
      "default" : 400,
      "min"     : 200,
      "max"     : 800,
    },
    "wdth": {
      "name"    : "Width",
      "default" : 100,
      "min"     : 85,
      "max"     : 125,
    }
}

# extract measurements from Amstelvar1

assert os.path.exists(measurementsPath)
ufos = glob.glob(f'{sourcesFolder1}/*.ufo')

blendedSources = {}
for ufoPath in sorted(ufos):
    assert os.path.exists(ufoPath)
    fontName = os.path.splitext(os.path.split(ufoPath)[-1])[0]
    styleName = '_'.join(fontName.split('_')[1:])
    # don't include the default
    if styleName == 'wght400':
        continue
    # ignore GRAD sources
    if 'GRAD' in styleName:
        continue
    f = OpenFont(ufoPath, showInterface=False)
    M = FontMeasurements()
    M.read(measurementsPath)
    M.measure(f)
    blendedSources[styleName] = { k: v for k, v in M.values.items() if k in parametricAxes }

# save measurements to JSON blends file

blendsDict = {
    'axes'    : blendedAxes,
    'sources' : blendedSources,
}

with open(blendsPath, 'w', encoding='utf-8') as f:
    json.dump(blendsDict, f, indent=2)
