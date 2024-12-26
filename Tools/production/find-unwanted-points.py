# menuTitle: find unwanted off-curve points

'''
scans all glyphs in the current font searching for segments with 1 or 3 or more off-curve points

'''

font  = CurrentFont()

print('searching for unwanted off-curve points...\n')
foundGlyphs = []
for glyph in font:
    for contour in glyph.contours:
        for segment in contour.segments:
            if len(segment) in [1, 3]:
                continue
            if glyph.name not in foundGlyphs:
                print(f'\t{glyph.name}')
                foundGlyphs.append(glyph.name)
            print(f'\t\tsegment #{segment.index} has {len(segment)-1} off-curve point{"s" if len(segment)-1 !=1 else ""}')
    if glyph.name in foundGlyphs:
        print()

if not foundGlyphs:
    print('\tno problems found.\n')

print('...done.\n')
