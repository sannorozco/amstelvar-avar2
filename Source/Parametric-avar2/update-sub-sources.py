# menuTitle: update sub-sources

import os, glob
from mojo.smartSet import readSmartSets
from variableValues.linkPoints import readMeasurements


def copyGlyphs(glyphNames, srcFont, dstFont):
    pass


class AmstelvarSubSourceUpdater:

    baseFolder       = os.getcwd()
    familyName       = 'AmstelvarA2'
    subFamilyName    = ['Roman', 'Italic'][0]
    defaultName      = 'wght400'
    sourcesFolder    = os.path.join(baseFolder, subFamilyName)
    smartSetsPath    = os.path.join(baseFolder, 'AmstelvarA2.roboFontSets')
    measurementsPath = os.path.join(sourcesFolder, 'measurements.json')

    def __init__(self):
        self.smartSets    = readSmartSets(self.smartSetsPath, useAsDefault=False, font=None)
        self.measurements = readMeasurements(self.measurementsPath)

    @property
    def sources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultUFO(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{self.defaultName}.ufo')

    def XOUC(self, parent=True, default=False):

        subAxis    = 'XOUC'
        parentAxis = 'XOPQ'
        parentCopy = ['uppercase latin', 'uppercase greek']

        # get min/max sources
        subValues = []
        for src in self.sources:
            if subAxis in src:
                value = int(os.path.splitext(os.path.split(src)[-1])[0].split('_')[-1][4:])
                subValues.append(value)
        assert len(subValues)
        subValues.sort()

        if parent:
            # get min/max parents
            parentValues = []
            for src in self.sources:
                if parentAxis in src:
                    value = int(os.path.splitext(os.path.split(src)[-1])[0].split('_')[-1][4:])
                    parentValues.append(value)
            assert len(parentValues)
            parentValues.sort()

            for i in range(len(subValues)):

                # get source font (parent)
                srcName = f'{parentAxis}{parentValues[i]}'
                srcPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{srcName}.ufo')
                assert os.path.exists(srcPath)
                srcFont = OpenFont(srcPath, showInterface=False)

                # get target font (sub-source)
                dstName = f'{subAxis}{subValues[i]}'
                dstPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{dstName}.ufo')
                assert os.path.exists(dstPath)
                dstFont = OpenFont(dstPath, showInterface=False)

                # copy glyphs from parent to sub-source
                print(f'copying glyphs from {srcName} to {dstName}...')
                for smartSet in self.smartSets:
                    for group in smartSet.groups:
                        if group.name in parentCopy:
                            print(f'\tcopying {group.name}...')
                            for glyphName in group.glyphNames:
                                dstFont.insertGlyph(srcFont[glyphName])
                srcFont.close()
                # dstFont.save()
                dstFont.close()
                print('...done.\n')

        if default:
            srcFont = OpenFont(self.defaultUFO, showInterface=False)

            parentGlyphs = []
            for smartSet in self.smartSets:
                for group in smartSet.groups:
                    if group.name in parentCopy:
                        parentGlyphs += group.glyphNames

            for subValue in subValues:
                dstName = f'{subAxis}{subValue}'
                dstPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{dstName}.ufo')
                assert os.path.exists(dstPath)
                dstFont = OpenFont(dstPath, showInterface=False)
                print(f'copying glyphs from {self.defaultName} to {dstName}...')
                for glyphName in srcFont.glyphOrder:
                    if glyphName not in parentGlyphs:
                        # print(f'\tcopying {glyphName}...')
                        dstFont.insertGlyph(srcFont[glyphName])
                # dstFont.save()
                dstFont.close()
                print('...done.\n')

            srcFont.close()

    def XOLC(self):
        # XOPQ    : lowercase
        # default : other
        pass

    def XOFI(self):
        pass


if __name__ == '__main__':

    U = AmstelvarSubSourceUpdater()
    U.XOUC(parent=False, default=True)




