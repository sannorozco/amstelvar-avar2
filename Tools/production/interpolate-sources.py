import os
from xTools4.modules.measurements import FontMeasurements, permille

baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][1]
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')

src1 = 'wght400'
src2 = 'XUCS126'

f = 1.2

ufoPath1 = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{src1}.ufo')
ufoPath2 = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{src2}.ufo')

f1 = OpenFont(ufoPath1, showInterface=False)
f2 = OpenFont(ufoPath2, showInterface=False)
f3 = NewFont(showInterface=False)

# interpolate glyphs
for glyphName in f1.glyphOrder:
    if glyphName not in f2:
        continue
    g1 = f1[glyphName]
    g2 = f2[glyphName]
    g3 = f3.newGlyph(name=glyphName)
    g3.interpolate(f, g1, g2)
    g3.unicodes = g1.unicodes

# copy font info
fontInfo = f1.info.asDict()
for attr, value in fontInfo.items():
    setattr(f3.info, attr, value)

# get measurements from generated font
measurements = FontMeasurements()
measurements.read(measurementsPath)
measurements.measure(f3)

print('old value:', src2[4:])
print('new value:', permille(measurements.values[src2[:4]], f3.info.unitsPerEm))
print()

f3.openInterface()
