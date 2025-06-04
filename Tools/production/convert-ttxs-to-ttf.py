import os, glob
from fontTools.ttLib import TTFont

baseFolder  = os.path.dirname(os.path.dirname(os.getcwd()))
fontsFolder = os.path.join(baseFolder, 'Fonts')

ttxPaths = glob.glob(f'{fontsFolder}/*.ttx')

print('converting ttxs to ttf...')
for ttxPath in ttxPaths:
    ttfPath = ttxPath.replace('.ttx', '.ttf')
    print(f'\twriting {os.path.split(ttfPath)[-1]}...')
    f = TTFont()
    f.importXML(ttxPath)
    f.save(ttfPath)
    f.close()

print('...done!\n')
