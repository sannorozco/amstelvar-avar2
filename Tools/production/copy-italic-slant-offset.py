# menuTitle: copy italic slant offset from default font to other sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

assert os.path.exists(sourcePath)

dstFonts  = []
preflight = False

sourceFont = OpenFont(sourcePath, showInterface=False)
ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

print('copying italic slant offset from default font to other sources...')

for ufoPath in ufoPaths:
    if ufoPath == sourcePath:
        continue

    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:
        targetFont = OpenFont(ufoPath, showInterface=False)
        
        sourceOffset = sourceFont.lib.get("com.typemytype.robofont.italicSlantOffset")
        targetOffset = targetFont.lib.get("com.typemytype.robofont.italicSlantOffset")

        if sourceOffset != targetOffset:
            print(f'\tcopying italic slant offset to {os.path.split(ufoPath)[-1]}...')
            if not preflight:
                targetFont.lib["com.typemytype.robofont.italicSlantOffset"] = sourceOffset
                print(f'\tsaving font...')
                targetFont.save()

            # targetFont.close()

print('...done!\n')
