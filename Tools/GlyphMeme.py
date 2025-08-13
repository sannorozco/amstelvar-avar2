import os
import ezui
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, NewFont
from mojo.smartSet import readSmartSets
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib.glifLib import GlyphSet
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.dialogs.variable.old.TempEdit import setupNewFont, splitall

familyName        = 'AmstelvarA2'
subFamilyName     = ['Roman', 'Italic'][0]
baseFolder        = os.path.dirname(os.getcwd())
sourcesFolder     = os.path.join(baseFolder, 'Sources', subFamilyName)
measurementsPath  = os.path.join(sourcesFolder, 'measurements.json')
defaultPath       = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_wght400.ufo')
designspacePath   = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_avar2.designspace')
smartSetsPath     = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}.roboFontSets')
glyphSetPathKey   = 'com.hipertipo.tempEdit.glyphSetPath'


class GlyphMeme(ezui.WindowController):

    title   = 'GlyphMeme'
    margins = 10

    content = """
    (groups ...)  @groupSelector
    (glyphs ...)  @glyphSelector

    | | @glyphMeme

    ( open )  @openButton
    ( save )  @saveButton

    """

    descriptionData = dict(
        content=dict(
            sizeStyle="small",
        ),
        groupSelector=dict(
            width='fill',
        ),
        glyphSelector=dict(
            width='fill',
        ),
        openButton=dict(
            width='fill',
        ),
        saveButton=dict(
            width='fill',
        ),
    )

    def build(self):
        self.w = ezui.EZPanel(
            title=self.title,
            content=self.content,
            descriptionData=self.descriptionData,
            controller=self,
            margins=self.margins,
            size=(123, 300),
            minSize=(123, 200),
            maxSize=(123, 400),
        )
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.getItem("glyphMeme").getNSTableView().setRowHeight_(17)
        self.w.open()

    def started(self):
        print(f'loading designspace from {os.path.split(designspacePath)[-1]}...')
        self.designspace = DesignSpaceDocument()
        self.designspace.read(designspacePath)

        print(f'loading measurements from {os.path.split(measurementsPath)[-1]}...')
        measurements = readMeasurements(measurementsPath)
        self.measurements = measurements['glyphs']

        print(f'loading glyph groups from {os.path.split(smartSetsPath)[-1]}...')
        smartSets = readSmartSets(smartSetsPath, useAsDefault=False, font=None)
        self.defaultFont = OpenFont(defaultPath, showInterface=False)
        self.glyphGroups = {}
        for smartGroup in smartSets:
            if not smartGroup.groups:
                continue
            for smartSet in smartGroup.groups:
                # remove component glyphs
                glyphNames = []
                for glyphName in smartSet.glyphNames:
                    if glyphName not in self.defaultFont:
                        continue
                    g = self.defaultFont[glyphName]
                    if not len(g.components):
                        glyphNames.append(glyphName)
                if len(glyphNames):
                    self.glyphGroups[smartSet.name] = glyphNames

        groupSelector = self.w.getItem("groupSelector")
        groupSelector.setItems(self.glyphGroups.keys())
        self.groupSelectorCallback(None)

    def groupSelectorCallback(self, sender):
        groupSelector = self.w.getItem("groupSelector")
        glyphSelector = self.w.getItem("glyphSelector")
        selectedGroup = groupSelector.getItem()
        glyphSelector.setItems(self.glyphGroups[selectedGroup])
        self.glyphSelectorCallback(None)

    def glyphSelectorCallback(self, sender):
        glyphName = self.w.getItem("glyphSelector").getItem()
        measurementsDict = self.measurements.get(glyphName, {})
        measurements = sorted(list(set([m['name'] for m in measurementsDict.values()])))
        memesTable = self.w.getItem("glyphMeme")
        memesTable.set(measurements)
        memesTable.setSelectedIndexes(range(len(measurements)))

    def openButtonCallback(self, sender):

        glyphName = self.w.getItem("glyphSelector").getItem()
        selectedMeasurements = self.w.getItem("glyphMeme").getSelectedItems()

        tmpFont = NewFont(familyName='tempEdit')
        setupNewFont(tmpFont)
        tmpFont.info.familyName = f'{familyName} {subFamilyName}'
        tmpFont.info.styleName  = glyphName

        sources = []
        for src in self.designspace.sources:
            for measurementName in selectedMeasurements:
                if measurementName in src.styleName:
                    sources.append(src.filename)

        print('opening glyphs...')

        for i, sourceFile in enumerate(sources):
            ufoPath = os.path.join(sourcesFolder, sourceFile)
            srcFont = OpenFont(ufoPath, showInterface=False)

            # copy vertical metrics from 1st source
            if i == 0:
                for attr in ['unitsPerEm', 'xHeight', 'capHeight', 'descender', 'ascender']:
                    value = getattr(srcFont.info, attr)
                    setattr(tmpFont.info, attr, value)

            glyphsFolder = os.path.join(ufoPath, 'glyphs')
            ufoName = splitall(glyphsFolder)[-2]
            glyphNameExtension = os.path.splitext(sourceFile)[0].split('_')[-1]

            tmpGlyphName = f'{glyphName}.{glyphNameExtension}'

            srcGlyph = srcFont[glyphName]

            print(f'\timporting {glyphName} from {ufoName}...')

            tmpFont.newGlyph(tmpGlyphName)
            tmpFont[tmpGlyphName].appendGlyph(srcGlyph)
            tmpFont[tmpGlyphName].width = srcGlyph.width
            tmpFont.changed()

            tmpFont[tmpGlyphName].lib[glyphSetPathKey] = glyphsFolder

        print('...done!\n')

    def saveButtonCallback(self, sender):

        f = CurrentFont()

        if f is None:
            return

        print('saving selected glyphs...')

        for glyphName in f.selectedGlyphNames:

            glyph = f[glyphName].getLayer('foreground')

            if glyphSetPathKey not in glyph.lib:
                continue

            glyphsFolder = glyph.lib[glyphSetPathKey]
            srcGlyphName = glyphName[:glyphName.rfind('.')]
            ufoName = splitall(glyphsFolder)[-2]

            print(f'\texporting {srcGlyphName} to {ufoName}...')
            glyphSet = GlyphSet(glyphsFolder, validateWrite=True)
            glyphSet.writeGlyph(srcGlyphName, glyph.naked(), glyph.drawPoints)
            glyphSet.writeContents()

        print('...done!\n')



if __name__ == '__main__':

    OpenWindow(GlyphMeme)

