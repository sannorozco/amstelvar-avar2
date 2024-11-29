# menuTitle: fix XOFI XTFI YOFI etc glyph coverage

import os, glob
from collections import Counter
from mojo.smartSet import readSmartSets

'''
1. copy glyphs from lowercase to figures
2. copy glyphs from default to lowercase

- all figure styles (lining, oldstyle, tabular, etc)
- all math operators
- all currency symbols
- superior figures
- fractions
- perthousand

'''

subfamilyName = ['Roman', 'Italic'][1]
defaultName   = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources')
smartSetsPath = os.path.join(sourcesFolder, 'AmstelvarA2.roboFontSets')
defaultPath   = os.path.join(sourcesFolder, subfamilyName, f'AmstelvarA2-{subfamilyName}_{defaultName}.ufo')
ufoPaths      = glob.glob(f'{sourcesFolder}/{subfamilyName}/*.ufo')

assert os.path.exists(smartSetsPath)
assert os.path.exists(defaultPath)

preflight = True

sourcesFigures = {
    'XOFI' : 'XOLC',   # figures : lowercase
    'YOFI' : 'YOLC',
    'XTFI' : 'XTLC',
}

smartSets = readSmartSets(smartSetsPath, useAsDefault=False, font=None)

copyGroups = [
    'fractions',
    'currency',
    'math operators',
    'figures superior',
]

glyphNames = []
for smartSet in smartSets:
    for group in smartSet.groups:
        if group.name in copyGroups:
            glyphNames += group.glyphNames

glyphNames += [
    'perthousand'
    'fraction',
]

defaultSrc = OpenFont(defaultPath, showInterface=False)

for figuresName, lowercaseName in sourcesFigures.items():

    figuresSources = [f for f in ufoPaths if figuresName   in os.path.split(f)[-1]]
    figuresValues  = {int(os.path.splitext(os.path.split(f)[-1])[0].split('_')[-1][4:]) : f for f in figuresSources }

    lowercaseSources = [f for f in ufoPaths if lowercaseName in os.path.split(f)[-1]]
    lowercaseValues = {int(os.path.splitext(os.path.split(f)[-1])[0].split('_')[-1][4:]) : f for f in lowercaseSources }

    print(f'fixing {figuresName} and {lowercaseName} sources...')
    for i, figuresSrcValue in enumerate(sorted(figuresValues.keys())):
        figuresSrcPath = figuresValues[figuresSrcValue]
        figuresSrc = OpenFont(figuresSrcPath, showInterface=False)

        lowercaseSrcValue = sorted(lowercaseValues.keys())[i]
        lowercaseSrcPath = lowercaseValues[lowercaseSrcValue]
        lowercaseSrc = OpenFont(lowercaseSrcPath, showInterface=False)

        # copy lowercase glyphs to figures source
        print(f'\tcopying glyphs from {lowercaseName}{lowercaseSrcValue} to {figuresName}{figuresSrcValue}...')
        if not preflight:
            for glyphName in glyphNames:
                if glyphName not in figuresSrc:
                    print(f'ERROR: {glyphName} not in lowercase font {lowercaseSrcValue}')
                    continue
                figuresSrc.insertGlyph(lowercaseSrc[glyphName], name=glyphName)
            figuresSrc.save()
            figuresSrc.close()

        # copy default glyphs to lowercase source
        print(f'\tcopying glyphs from {defaultName} to {lowercaseName}{lowercaseSrcValue}...')
        if not preflight:
            for glyphName in glyphNames:
                if glyphName not in defaultSrc:
                    print(f'ERROR: {glyphName} not in default font {defaultName}')
                    continue
                lowercaseSrc.insertGlyph(defaultSrc[glyphName], name=glyphName)
            lowercaseSrc.save()
            lowercaseSrc.close()

        print()

