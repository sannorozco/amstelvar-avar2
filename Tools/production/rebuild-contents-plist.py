# menuTitle : rebuild contents.plist

import os, glob
import plistlib
from fontTools.ufoLib import LAYERCONTENTS_FILENAME
from fontTools.ufoLib.glifLib import readGlyphFromString, CONTENTS_FILENAME


class SimpleGlyph:
    
    def draw(self, pen):
        pass
    
    def drawPoints(self, pointPen):
        pass

def rebuildContenstPlist(ufoPath):
    layerPlistPath = os.path.join(ufoPath, LAYERCONTENTS_FILENAME)
    with open(layerPlistPath, "rb") as f:
        layerContents = plistlib.load(f)

    for _, layerDirName in layerContents:
        contentsDict = {}
        
        layerPath = os.path.join(ufoPath, layerDirName)
        
        glifPaths = glob.glob(os.path.join(layerPath, "*.glif"))
        for glifPath in glifPaths:
            with open(glifPath, "rb") as f:
                glyph = SimpleGlyph()
                readGlyphFromString(f.read(), glyphObject=glyph)
                contentsDict[glyph.name] = os.path.basename(glifPath)

        contentsPlistPath = os.path.join(layerPath, CONTENTS_FILENAME)
        with open(contentsPlistPath, 'wb') as f:
            plistlib.dump(contentsDict, f)


familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)

assert os.path.exists(sourcesFolder)

sources = glob.glob(f'{sourcesFolder}/*.ufo')

for sourcePath in sources:
    rebuildContenstPlist(sourcePath)
