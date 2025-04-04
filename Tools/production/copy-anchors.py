# menuTitle: copy anchors from default font to other sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

# settings

glyphNames = [
    'period'
]
anchorNames = [
    '_ellipsis',
    'ellipsis',
]

# batch copy anchors

dstFonts  = []
preflight = False

srcFont  = OpenFont(sourcePath, showInterface=False)
ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == sourcePath:
        continue

    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:
        dstFont = OpenFont(ufoPath, showInterface=False)

        print(f'copying anchors to {os.path.split(ufoPath)[-1]}...')
        for glyphName in glyphNames:
            if glyphName not in srcFont or glyphName not in dstFont:
                continue
            
            srcGlyph = srcFont[glyphName]
            dstGlyph = dstFont[glyphName]

            for anchor in srcGlyph.anchors:
                if anchor.name in anchorNames:
                    print(f"\tcopying anchor '{anchor.name}' to glyph '{glyphName}'...")
                    if not preflight:
                        dstGlyph.appendAnchor(anchor.name, (anchor.x, anchor.y))

        if not preflight:
            print(f'\tsaving font...')
            dstFont.save()

        # dstFont.close()
        print()

print('...done!\n')
