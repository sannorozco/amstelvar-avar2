from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, json
from xTools4.modules.measurements import copyFontMeasurements, copyGlyphMeasurements

baseFolder          = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder       = os.path.join(baseFolder, 'Sources')
measurementsPathSrc = os.path.join(sourcesFolder, 'Roman',  'measurements.json')
measurementsPathDst = os.path.join(sourcesFolder, 'Italic', 'measurements.json') 

# copy font-level measurements
measurementNames = [] # 'YTUO YTLO YTFO YTAO YTDO XOAC YOAC XOUA XOLA YOUA YOLA YTUA YTLA YUAT YLAT XTUA XTLA'.split()
copyFontMeasurements(measurementsPathSrc, measurementsPathDst, measurementNames)

# copy glyph-level measurements
glyphNames = ['AE'] # CurrentFont().selectedGlyphNames
copyGlyphMeasurements(measurementsPathSrc, measurementsPathDst, glyphNames)
