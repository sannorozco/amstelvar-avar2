import os

baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources')

roman  = os.path.join(sourcesFolder, 'Roman',  'AmstelvarA2-Roman_wght400.ufo')
italic = os.path.join(sourcesFolder, 'Italic', 'AmstelvarA2-Italic_wght400.ufo')

f1 = OpenFont(roman,  showInterface=False)
f2 = OpenFont(italic, showInterface=False)

# check for glyphs which are included in the roman and not in the italic
# for glyphName in f1.glyphOrder:
#     if glyphName not in f2:
#         print(f'{glyphName} not in Italic font')
 
# compare glyph composition in italic with roman
for glyphName in f2.glyphOrder:
    if glyphName not in f1:
        continue
    if f2[glyphName].components:
        c2 = [c.baseGlyph for c in f2[glyphName].components]
        c1 = [c.baseGlyph for c in f1[glyphName].components]
        if c1 != c2:
            print(glyphName)
