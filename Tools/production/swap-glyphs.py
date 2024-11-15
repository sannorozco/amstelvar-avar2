import os, glob
from xTools4.modules.fontutils import swapGlyphs

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)

dstFonts = ['XOUC4']
ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

swapPairs = [
    ('engtail', 'Engtail'),
]

for ufoPath in ufoPaths:
    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]

    if name in dstFonts or not dstFonts:
        dstFont = OpenFont(ufoPath, showInterface=False)
        print(f'swapping glyphs in {os.path.split(ufoPath)[-1]}...')

        for glyphName1, glyphName2 in swapPairs:
            print(f"\tswapping '{glyphName1}' with '{glyphName2}'")
            swapGlyphs(dstFont, glyphName1, glyphName2)
        print('\tsaving font...')
        dstFont.save()
        # dstFont.close()
        print()


