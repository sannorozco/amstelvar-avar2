# menuTitle: compare measurements of AmstelvarA2 instances against Amstelvar

import os, glob, datetime
from xTools4.modules.measurements import FontMeasurements
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual, colorCheckNone

# --------
# settings
# --------

subFamilyName = ['Roman', 'Italic'][0]

threshold = 2
savePDF   = True

fs = 11              # font size
p  = 30, 20, 20, 20  # padding

# --------
# do stuff
# --------

familyName1       = 'AmstelvarA2'
baseFolder1       = os.path.dirname(os.path.dirname(os.getcwd()))
instancesFolder1  = os.path.join(baseFolder1, 'Fonts', 'instances', subFamilyName)
instances1        = glob.glob(f'{instancesFolder1}/*.ufo')
measurementsPath1 = os.path.join(baseFolder1, 'Sources', subFamilyName, 'measurements.json')

familyName2       = 'Amstelvar'
baseFolder2       = os.path.join(os.path.dirname(baseFolder1), 'amstelvar')
instancesFolder2  = os.path.join(baseFolder2, subFamilyName)
instances2        = glob.glob(f'{instancesFolder2}/*.ufo')
measurementsPath2 = os.path.join(baseFolder2, subFamilyName, 'measurements.json')
for i in instances2:
    fileName = os.path.split(i)[-1]
    if 'GRAD' in fileName or 'wght400' in fileName:
        instances2.remove(i)

_instances1 = {}
for i in instances1:
    instanceName = '_'.join(os.path.splitext(os.path.split(i)[1])[0].split('_')[2:])
    _instances1[instanceName] = i

_instances2 = {}
for i in instances2:
    instanceName = '_'.join(os.path.splitext(os.path.split(i)[1])[0].split('_')[1:])
    _instances2[instanceName] = i

# print(f'instances in Amstelvar {subFamilyName} and NOT in AmstelvarA2 {subFamilyName}:')
# missingInstances = set(_instances2.keys()).difference(set(_instances1.keys()))
# for i in sorted(missingInstances):
#     print(f'\t{i}')
# print()
    
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

tabs = [
    (100, "right"),
    (190, "right"),
    (270, "right"),
    (320, "right"),
]

# for instanceName in sorted(_instances1.keys()):
#     print(instanceName)

for opsz in [14, 8, 144]:
    for wght in [400, 100, 1000]:
        for wdth in [100, 50, 125]:
            instanceName = []
            if opsz == 14 and wght == 400 and wdth == 100:
                continue
            if opsz != 14:
                instanceName.append(f'opsz{opsz}')
            if wght != 400:
                instanceName.append(f'wght{wght}')
            if wdth != 100:
                instanceName.append(f'wdth{wdth}')
            instanceName = '_'.join(instanceName)

            assert instanceName in _instances1

            instancePath1 = os.path.join(instancesFolder1, f'AmstelvarA2-{subFamilyName}_avar2_{instanceName}.ufo')
            instancePath2 = os.path.join(instancesFolder2, f'Amstelvar-{subFamilyName}_{instanceName}.ufo')
            instance1 = OpenFont(instancePath1, showInterface=False)
            instance2 = OpenFont(instancePath2, showInterface=False)

            M1 = FontMeasurements()
            M1.read(measurementsPath1)
            M1.measure(instance1)

            M2 = FontMeasurements()
            M2.read(measurementsPath2)
            M2.measure(instance2)

            newPage('A4')

            # page header: instance name & date
            with savedState():
                x1 = p[3]
                x2 = width() / 2
                x3 = width() - p[1]
                y1 = height() - p[0]*0.57
                font('Menlo')
                fontSize(fs)
                text(f'{subFamilyName} opsz{opsz} wght{wght} wdth{wdth}', (x1, y1), align='left')
                text(f'threshold={threshold}', (width()/2, y1), align='center')
                text(f'{now}', (x3, y1), align='right')

            # measurements table
            T = FormattedString()
            T.font('Menlo')
            T.fontSize(fs)
            T.lineHeight(fs*1.25)

            T.tabs(*tabs)
            T.append('\tglyph\tAmstelvarA2\tAmstelvar\tdiff\n')
            for key, value2 in M2.values.items():
                value1 = M1.values.get(key)

                def1 = [d for d in M1.definitions if d[0] == key]
                def2 = [d for d in M2.definitions if d[0] == key]

                if def1:        
                    glyph11, pt11, glyph12, pt12 = [(d[2], d[3], d[4], d[5]) for d in M1.definitions if d[0] == key][0]
                else:
                    glyph11 = pt11 = glyph12 = pt12 = '—'

                if def2:
                    glyph21, pt21, glyph22, pt22 = [(d[2], d[3], d[4], d[5]) for d in M2.definitions if d[0] == key][0]
                else:
                    glyph21 = pt21 = glyph22 = pt22 = '—'

                if value1 is None or value2 is None:            
                    value1 = difference = '—'
                    c = colorCheckNone
                else:
                    difference = abs(value1 - value2)
                    if value1 == value2:
                        c = colorCheckEqual
                    elif difference <= threshold:
                        c = colorCheckTrue
                    else:
                        c = colorCheckFalse

                if c == colorCheckFalse:
                    T.fill(*c)
                else:
                    T.fill(0)
                T.append(f'{key}\t')
                T.fill(0)
                T.append(f'{glyph11}\t')
                T.fill(*c)
                T.append(f'{value2}\t{value1}\t')
                if c == colorCheckFalse:
                    T.fill(*c)
                else:
                    T.fill(0)
                T.append(f'{difference}\n')

            text(T, (p[3], height()-50))

if savePDF:
    pdfPath = os.path.join(instancesFolder1, f'AmstelvarA2-{subFamilyName}_blending-check.pdf')
    saveImage(pdfPath)
