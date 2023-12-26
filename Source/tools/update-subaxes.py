# menuTitle: build sub-axes [NOT WORKING YET!]

import os, glob
from mojo.smartSet import readSmartSets
from variableValues.linkPoints import readMeasurements

smartSetsPath    = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/AmstelvarA2.roboFontSets'
measurementsPath = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman/measurements.json'

smartSets = readSmartSets(smartSetsPath, useAsDefault=False, font=None)
measurements = readMeasurements(measurementsPath)
sourcesFolder = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman'

sources = glob.glob(f'{sourcesFolder}/*.ufo')

# for smartSet in smartSets:
#     print(smartSet)
#     for group in smartSet.groups:
#         print(group)
#         # print(group.glyphNames)
#     print()

# for measurementName, measurement in measurements['font'].items():
#     print(measurementName, measurement['parent'])

caseParameters = {
    'uppercase' : [
        'XOUC', 'XTUC', 'YOUC',
        'XSHU', 'YSHU', 'XSVU', 'YSVU'
    ],
    'lowercase' : [
        'XOLC', 'XTLC', 'YOLC',
        'XSHL', 'YSHL', 'XSVL', 'YSVL'
    ],
    'figures' : [
        'XOFI', 'XTFI', 'YOFI',
        'XSHF', 'YSHF', 'XSVF', 'YSVF'
    ],
}

# get max/min sources for each parametric axis

# for src in sources:
    
#             # get min/max values from file names
#             values = []
#             for ufo in self.parametricSources:
#                 if name in ufo:
#                     value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
#                     values.append(value)
#             assert len(values)
#             values.sort()
#             # create axis




for case, parameters in caseParameters.items():
    print(case)
    for param in parameters:
        if param not in measurements['font']:
            continue
        parent = measurements['font'][param]['parent']
        print(f'\t{parent} -> {param}')
        values = []
        for srcPath in sources:
            if param in srcPath:
                print(f'\t\t{srcPath}')
                value = int(os.path.splitext(os.path.split(srcPath)[-1])[0].split('_')[-1][4:])
                values.append(value)
        if not len(values):
            continue
        values.sort()
        print('\t\t', values)
    

            # print(f'\t\t{sourcePath}')
        
    print()

