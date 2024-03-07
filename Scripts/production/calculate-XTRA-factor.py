import os
from variableValues.measurements import FontMeasurements, Measurement, permille
from variableValues.linkPoints import readMeasurements

familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')
defaultPath      = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_wght400.ufo')
measurementsDict = readMeasurements(measurementsPath)

def makeMeasurementArgs(glyphName, i=0, measurement='XTUC'):
    args = [[v['name'], v['direction']] + k.split() for k, v in measurementsDict['glyphs'][glyphName].items() if v['name'] == measurement][i]
    args.insert(2, glyphName)
    args.insert(4, glyphName)
    return args

g = CurrentGlyph()

assert g is not None

i = 0

srcFont  = AllFonts().getFontsByStyleName('Roman')[0] # OpenFont(defaultPath, showInterface=False)
dstFont  = CurrentFont()
srcGlyph = 'H'
dstGlyph = g.name

print(dstGlyph)

M1 = Measurement(*makeMeasurementArgs(srcGlyph))
srcReference = M1.measure(srcFont)
dstReference = M1.measure(dstFont)

for m in ['XTUC', 'XTLC', 'XTRA']:
    try:
        M2 = Measurement(*makeMeasurementArgs(dstGlyph, i, measurement=m))
    except:
        pass

srcValue = M2.measure(srcFont)
dstValue = srcValue * dstReference / srcReference

print(f'{srcValue} -> {round(dstValue)}')

dstFont[dstGlyph].rightMargin = srcFont[dstGlyph].rightMargin

