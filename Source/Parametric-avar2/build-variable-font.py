import os
from defcon import Font
from fontTools.designspaceLib import DesignSpaceDocument
from ufo2ft import compileVariableTTF
# from ufo2ft.featureWriters.kernFeatureWriter import KernFeatureWriter
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont

familyName      = 'AmstelvarA2'
subFamilyName   = ['Roman', 'Italic'][0]
baseFolder      = os.path.dirname(os.getcwd())
sourcesFolder   = os.path.join(baseFolder, 'Parametric-avar2', subFamilyName)
designspacePath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_0.designspace')
fontsFolder     = os.path.join(os.path.dirname(baseFolder), 'fonts', 'Parametric avar2 TTFs')
varFontPath     = designspacePath.replace(sourcesFolder, fontsFolder).replace('.designspace', '.ttf')

assert os.path.exists(designspacePath)
assert os.path.exists(fontsFolder)

print(f'generating variable font for {designspacePath}...')

D = DesignSpaceDocument()
D.read(designspacePath)
print(f'\tloading sources...')
for src in D.sources:
    src.font = Font(src.path)

# build variable font with ufo2ft
print('\tbuilding variable font...')
f = compileVariableTTF(D, featureWriters=[])
f.save(varFontPath)
print('...done.\n')

assert os.path.exists(varFontPath)

# subset ascii variable font with pyftsubset

print('subsetting variable font...')
font = TTFont(varFontPath)
asciiGlyphs = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()
subsetter = Subsetter()
subsetter.populate(glyphs=asciiGlyphs)
subsetter.subset(font)
font.save(varFontPath)
print('...done.\n')
