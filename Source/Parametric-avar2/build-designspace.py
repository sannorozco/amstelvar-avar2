import os, glob, shutil
import ufoProcessor
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from variableValues.measurements import FontMeasurements
from defcon import Font
from ufo2ft import compileTTF

def permille(value, unitsPerEm):
    return round(value * 1000 / unitsPerEm)

class AmstelvarDesignSpaceBuilder:

    familyName           = 'AmstelvarA2'
    subFamilyName        = ['Roman', 'Italic'][0]
    baseFolder           = os.path.dirname(os.getcwd())
    sourcesFolder        = os.path.join(baseFolder,    'Parametric-avar2', subFamilyName) # 'TechAlpha'
    measurementsPath     = os.path.join(sourcesFolder, 'measurements.json')
    defaultUFO           = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_wght400.ufo')
    designspacePath      = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}.designspace')
    # blendedAxes          = 'opsz wght wdth'.split()
    parametricAxes       = 'XOPQ XTRA YOPQ YTUC YTLC YTAS YTDE YTFI'.split()
    parametricAxesHidden = False

    def __init__(self):
        # collect parametric sources
        self.sourcesParametric = glob.glob(f'{self.sourcesFolder}/*.ufo')
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def defaultLocation(self):
        L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        L['GRAD'] = 0
        L['XTSP'] = 0
        return L

    def addParametricAxes(self):

        # add grades axis
        a = AxisDescriptor()
        a.name    = 'GRAD'
        a.tag     = 'GRAD'
        a.minimum = -300
        a.maximum = 500
        a.default = 0
        self.designspace.addAxis(a)

        # add spacing axis
        a = AxisDescriptor()
        a.name    = 'XTSP'
        a.tag     = 'XTSP'
        a.minimum = -100
        a.maximum = 100
        a.default = 0
        self.designspace.addAxis(a)

        # add parametric axes
        for name in self.parametricAxes:
            # get min/max values from file names
            values = []
            for ufo in self.sourcesParametric:
                if name in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            assert len(values)
            values.sort()
            # create axis
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = values[0]
            a.maximum = values[1]
            a.default = permille(self.measurementsDefault.values[name], self.unitsPerEm)
            a.hidden  = self.parametricAxesHidden
            self.designspace.addAxis(a)

    def addDefaultSource(self):
        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = self.familyName
        src.location   = self.defaultLocation.copy()
        self.designspace.addSource(src)

    def addParametricSources(self):

        # add GRAD sources
        for gradeValue in [-300, 500]:
            L = self.defaultLocation.copy()
            L['GRAD'] = gradeValue
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_GRAD{gradeValue}.ufo')
            src.familyName = self.familyName
            src.location   = L
            self.designspace.addSource(src)

        # add XTSP sources
        for spacingValue in [-100, 100]:
            L = self.defaultLocation.copy()
            L['XTSP'] = spacingValue
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_XTSP{spacingValue}.ufo')
            src.familyName = self.familyName
            src.location   = L
            self.designspace.addSource(src)

        # add parametric sources
        for name in self.parametricAxes:
            for ufo in self.sourcesParametric:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = self.familyName
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def build(self):
        '''Build the designspace object.'''
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()

    def save(self):
        self.designspace.write(self.designspacePath)


# -----
# build
# -----

if __name__ == '__main__':

    D = AmstelvarDesignSpaceBuilder()
    D.build()
    D.save()
