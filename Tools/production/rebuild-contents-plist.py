# menuTitle : Rebuild contents.plist

import plistlib
import glob
import os

from fontTools.ufoLib import LAYERCONTENTS_FILENAME
from fontTools.ufoLib.glifLib import readGlyphFromString, CONTENTS_FILENAME

from fontParts.ui import GetFile


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


ufoPaths = GetFile(
    "Select ufo to rebuild the contents.plist",
    allowsMultipleSelection=True,
    fileTypes=["ufo"]
)
for ufoPath in ufoPaths:           
    rebuildContenstPlist(ufoPath)
    