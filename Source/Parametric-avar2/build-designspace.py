import os, glob, shutil
import ufoProcessor
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from variableValues.measurements import FontMeasurements
from defcon import Font
from ufo2ft import compileTTF

def permille(value, unitsPerEm):
    return round(value * 1000 / unitsPerEm)

class AmstelvarDesignSpaceBuilder:

    familyName       = 'AmstelvarA2'
    subFamilyName    = ['Roman', 'Italic'][0]
    baseFolder       = os.path.dirname(os.getcwd())
    sourcesFolder    = os.path.join(baseFolder,    'Parametric-avar2', subFamilyName) # 'TechAlpha'
    measurementsPath = os.path.join(sourcesFolder, 'measurements.json')
    defaultUFO       = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_wght400.ufo')
    designspacePath  = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}.designspace')
    parametricAxes   = 'XOPQ XOUC XOLC XOFI XTRA XTUC XTLC XTFI YOPQ YTUC YTLC YTAS YTDE YTFI XTSP YTOS XTTW YTTL'.split()
    minValue         = -100
    maxValue         = 100

    def __init__(self):
        pass

    @property
    def parametricSources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultLocation(self):
        L = { axis: 0 for axis in self.parametricAxes }
        return L

    def addParametricAxes(self):
        for name in self.parametricAxes:
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = -100
            a.maximum = 100
            a.default = 0
            self.designspace.addAxis(a)

    def addDefaultSource(self):
        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = self.familyName
        src.styleName  = 'wght400'
        src.location   = self.defaultLocation.copy()
        self.designspace.addSource(src)

    def buildParametricSources(self):
        for name in self.parametricAxes:
            for value in [-100, 100]:
                fontName = f'{self.familyName}-{self.subFamilyName}_{name}{value}'
                sourcePath = os.path.join(self.sourcesFolder, f'{fontName}.ufo')
                shutil.copytree(self.defaultUFO, sourcePath)

    def addParametricSources(self):
        for name in self.parametricAxes:
            for ufo in self.parametricSources:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = self.familyName
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    L[name] = value
                    src.styleName  = f'{name}{value}'
                    src.location = L
                    self.designspace.addSource(src)

    def build(self, sources=False):
        if sources:
            self.buildParametricSources()
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()

    def save(self):
        if not self.designspace:
            return
        self.designspace.write(self.designspacePath)


# -----
# build
# -----

if __name__ == '__main__':

    D = AmstelvarDesignSpaceBuilder()
    D.build(sources=False)
    D.save()
