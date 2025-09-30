# menuTitle : rename glyph measurements

from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, json
from xTools4.modules.measurements import renameGlyphMeasurements

subFamilyName    = ['Roman', 'Italic'][0]
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

renameGlyphMeasurements(measurementsPath, glyphNames, renameDict)
