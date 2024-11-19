import os, json
from xTools4.modules.measurements import readMeasurements

baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources')

measurementsPathSrc = os.path.join(sourcesFolder, 'Roman',  'measurements.json')
measurementsPathDst = os.path.join(sourcesFolder, 'Italic', 'measurements.json') 

measurementsSrc = readMeasurements(measurementsPathSrc)
measurementsDst = readMeasurements(measurementsPathDst)

measurementNames = [] # 'YTUO YTLO YTFO YTAO YTDO XOAC YOAC XOUA XOLA YOUA YOLA YTUA YTLA YUAT YLAT XTUA XTLA'.split()
glyphNames       = CurrentFont().selectedGlyphNames

# copy font-level measurements
for measurementName in measurementNames:
    measurementsDst['font'][measurementName] = measurementsSrc['font'][measurementName] 

# copy glyph-level measurements
print('copying glyph-level measurements...')
for glyphName in glyphNames:
    print(f'\tcopying {glyphName}...')
    if glyphName not in measurementsSrc['glyphs']:
        continue
    measurementsDst['glyphs'][glyphName] = measurementsSrc['glyphs'][glyphName] 

print('\tsaving measurements...')
with open(measurementsPathDst, 'w', encoding='utf-8') as f:
    json.dump(measurementsDst, f, indent=2)

print('...done.')
