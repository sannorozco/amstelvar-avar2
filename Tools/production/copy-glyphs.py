# menuTitle: copy default glyphs to other sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

assert os.path.exists(sourcePath)

glyphNames = 'alpha rho tau'.split()
# glyphNames = "zero one two three four five six seven eight nine".split()
# glyphNames = "dollar cent sterling yen twosuperior threesuperior onesuperior Euro franc lira naira peseta won dong rupeeIndian liraTurkish manat ruble kip peso cedi colonsign guarani florin hryvnia tenge dollar.rvrn cent.rvrn naira.rvrn won.rvrn kip.rvrn peso.rvrn cedi.rvrn colonsign.rvrn dollar.rvrn2 guarani.rvrn zero.lc one.lc two.lc three.lc four.lc five.lc six.lc seven.lc eight.lc nine.lc zero.tab one.tab two.tab three.tab four.tab five.tab six.tab seven.tab eight.tab nine.tab zerosuperior foursuperior fivesuperior sixsuperior sevensuperior eightsuperior ninesuperior".split()
# # glyphNames += 'k t y germandbls'.split()
# glyphNames = 'horizontalbar leftanglebracket rightanglebracket periodcentered.loclCAT diagonalbarO horizontalbarH horizontalbarlc'.split()
# glyphNames += 'ampersand registered notequal currency breveinvertedcomb-stack endash yi-dieresis'.split()

dstFonts = 'XOPQ310 XSHL0 XSHL136 XSHU144 XSHU2 XSVF126 XSVF6 XSVL0 XSVL130 XSVU0 XSVU124 XTRA63 XTRA650 XTTW0 XTTW30 XUCS114 XUCS259'.split()
    
preflight = False

sourceFont = OpenFont(sourcePath, showInterface=False)
ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == sourcePath:
        continue

    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:

        dstFont = OpenFont(ufoPath, showInterface=False)

        print(f'copying glyphs to {os.path.split(ufoPath)[-1]}...')
        for glyphName in glyphNames:
            if glyphName not in sourceFont:
                print(f'\tERROR: {glyphName} not in source font')
                continue
            print(f'\tcopying {glyphName}...')
            if not preflight:
                dstFont.insertGlyph(sourceFont[glyphName], name=glyphName)

        if not preflight:
            print(f'\tsaving font...')
            dstFont.save()

        # dstFont.close()
        print()
