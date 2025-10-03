import os

baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources')

roman  = os.path.join(sourcesFolder, 'Roman',  'AmstelvarA2-Roman_wght400.ufo')
italic = os.path.join(sourcesFolder, 'Italic', 'AmstelvarA2-Italic_wght400.ufo')

romanFont  = OpenFont(roman,  showInterface=False)
italicFont = OpenFont(italic, showInterface=False)

compareGlyphSets  = True
compareComponents = True

if compareGlyphSets:

    print('comparing glyph sets:\n')
    romanGlyphSet  = set(romanFont.glyphOrder)
    italicGlyphSet = set(italicFont.glyphOrder)

    print('\tglyphs not in Italic:')
    for glyphName in romanGlyphSet.difference(italicGlyphSet):
        print(f"\t\t{glyphName}")
    print()

    print('\tglyphs not in Roman:')
    for glyphName in italicGlyphSet.difference(romanGlyphSet):
        print(f"\t\t{glyphName}")

    print()
 
if compareComponents:
 
    print('comparing components:\n')
    for glyphName in italicFont.glyphOrder:
        if glyphName not in romanFont:
            continue
        if italicFont[glyphName].components:
            italicComponents = [c.baseGlyph for c in italicFont[glyphName].components]
            romanComponents  = [c.baseGlyph for c in romanFont[glyphName].components]
            if romanComponents != italicComponents:
                print(f'\t{glyphName}:')
                print(f'\t\titalic : {" ".join(italicComponents)}')
                print(f'\t\t roman : {" ".join(romanComponents)}')
                print()
    