f1 = OpenFont('/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Sources/Roman/AmstelvarA2-Roman_wght400.ufo', showInterface=False) # AllFonts().getFontsByStyleName('wght400')[0]
f2 = OpenFont('/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Sources/Roman/old-sources/AmstelvarA2-Roman_YOPQ311.ufo', showInterface=False) # AllFonts().getFontsByStyleName('YOPQ311')[0]
f3 = NewFont(showInterface=False)

# interpolate glyphs
for glyphName in f1.glyphOrder:
    if glyphName not in f2:
        continue
    g1 = f1[glyphName]
    g2 = f2[glyphName]
    g3 = f3.newGlyph(name=glyphName)
    g3.interpolate(0.57, g1, g2)
    g3.unicodes = g1.unicodes

# copy font info
fontInfo = f1.info.asDict()
for attr, value in fontInfo.items():
    setattr(f3.info, attr, value)

f3.openInterface()
