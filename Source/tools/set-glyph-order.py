f1 = OpenFont('/Users/gferreira/hipertipo/fonts/roboto-flex-avar2/Source/Parametric-avar2/RobotoAvar2-wght400.ufo', showInterface=False)
f2 = AllFonts().getFontsByStyleName('XOPQ20')[0]

f2.templateGlyphOrder = f1.templateGlyphOrder

# # import math
# # f = CurrentFont()
# # italicSlantOffset = math.tan(f.info.italicAngle * math.pi / 180) * (f.info.xHeight * 0.5)
# # print(round(italicSlantOffset))
