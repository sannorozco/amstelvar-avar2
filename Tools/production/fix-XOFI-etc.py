# menuTitle: fix XOFI XTFI YOFI etc glyph coverage

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

sourcesFigures = {
    'XOFI' : 'XOLC',   # figures : lowercase
    'YOFI' : 'YOLC',
    'XTFI' : 'XTLC',
}

# get glyph names from smartsets
glyphNames = []

defaultSource = ''

# PSEUDO-CODE
for each figure source axis:
    for each figure source:
        get lowercase source;
        for glyphName in glyphNames:
            copy lowercase glyph to figure glyph;
        save and close figure source;
        for glyphName in glyphNames:
            copy default glyph to lowercase glyph;
        save and close lowercase souce;
