import os, glob, shutil
import ufoProcessor # upgrade to UFOOperator!
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from variableValues.measurements import FontMeasurements
from defcon import Font
from ufo2ft import compileTTF

def permille(value, unitsPerEm):
    return round(value * 1000 / unitsPerEm)

'''
targeted alpha build by Dec 31:
- ascii only
- default size only (opsz14)
- wght 200-800
- wdth 85-125

two versions:
- one instantiates the extreme to build an avar1
- one that is the same design space but using avar2

'''


class AmstelvarDesignSpaceBuilder:

    familyName      = 'AmstelvarA2'
    subFamilyName   = ['Roman', 'Italic'][0]
    defaultName     = 'wght400'
    parametricAxes  = 'XOPQ XOUC XOLC XOFI XTRA XTUC XTLC XTFI YOPQ YTUC YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL XSHF YSHF XSVF YSVF XTTW YTTL YTOS'.split()
    designspaceName = f'{familyName}-{subFamilyName}.designspace'

    def __init__(self):
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def baseFolder(self):
        return os.path.dirname(os.getcwd())

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, 'Parametric-avar2', self.subFamilyName)

    @property
    def measurementsPath(self):
        return os.path.join(self.sourcesFolder, 'measurements.json')

    @property
    def defaultUFO(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{self.defaultName}.ufo')

    @property
    def designspacePath(self):
        return os.path.join(self.sourcesFolder, self.designspaceName)

    @property
    def parametricSources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultLocation(self):
        L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        L['XTSP'] = 0
        return L

    def addParametricAxes(self):
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
            for ufo in self.parametricSources:
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
            self.designspace.addAxis(a)

    def addDefaultSource(self):
        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = self.familyName
        src.styleName  = self.defaultName
        src.location   = self.defaultLocation.copy()
        self.designspace.addSource(src)

    def addParametricSources(self):
        # add XTSP sources
        for spacingValue in [-100, 100]:
            L = self.defaultLocation.copy()
            L['XTSP'] = spacingValue
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_XTSP{spacingValue}.ufo')
            src.familyName = self.familyName
            src.styleName  = f'XTSP{spacingValue}'
            src.location   = L
            self.designspace.addSource(src)
        # add parametric sources
        for name in self.parametricAxes:
            for ufo in self.parametricSources:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = self.familyName
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    src.styleName  = f'{name}{value}'
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()

    def save(self):
        if not self.designspace:
            return
        self.designspace.write(self.designspacePath)


class AmstelvarDesignSpaceBuilder0(AmstelvarDesignSpaceBuilder):
    '''
    - parametric axes
    - XTSP
    - 4 instances for 2 axes extrema
    - avar 1

    '''
    blendedAxes    = {
        # 'opsz' : {
        #     'name'    : 'Optical size',
        #     'default' : 14,
        # },
        'wght' : {
            'name'    : 'Weight',
            'default' : 400,
        },
        'wdth' : {
            'name'    : 'Width',
            'default' : 100,
        },
    }

    parametricAxesParent = 'XOPQ XTRA YOPQ YTUC YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL XSHF YSHF XSVF YSVF XTTW YTTL YTOS'.split()

    designspaceName = AmstelvarDesignSpaceBuilder.designspaceName.replace('.designspace', '_0.designspace')

    @property
    def extremaFolder(self):
        return os.path.join(self.baseFolder, 'TechAlpha', self.subFamilyName, 'extrema')

    @property
    def extremaMeasurementsPath(self):
        return os.path.join(self.baseFolder, 'TechAlpha', self.subFamilyName, 'measurements.json')

    @property
    def extremaSources(self):
        return glob.glob(f'{self.extremaFolder}/*.ufo')

    @property
    def instancesFolder(self):
        return os.path.join(self.sourcesFolder, 'instances')

    # @property
    # def defaultLocation(self):
    #     L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
    #     L['XTSP'] = 0
    #     for tag in self.blendedAxes.keys():
    #         name    = self.blendedAxes[tag]['name']
    #         default = self.blendedAxes[tag]['default']
    #         L[name] = default
    #     return L

    # def addBlendedAxes(self):
    #     # load measurement definitions
    #     M = FontMeasurements()
    #     M.read(self.measurementsPath)

    #     for tag in self.blendedAxes.keys():
    #         # get min/max values from file names
    #         values = []
    #         for ufo in self.extremaSources:
    #             if tag in ufo:
    #                 value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
    #                 values.append(value)
    #         assert len(values)
    #         values.sort()
    #         # create axis
    #         a = AxisDescriptor()
    #         a.name    = self.blendedAxes[tag]['name']
    #         a.tag     = tag
    #         a.minimum = values[0]
    #         a.maximum = values[1]
    #         a.default = self.blendedAxes[tag]['default']
    #         self.designspace.addAxis(a)

    def addInstances(self):
        # prepare to measure extrema sources
        M = FontMeasurements()
        M.read(self.extremaMeasurementsPath)

        for tag in self.blendedAxes.keys():
            for ufoPath in self.extremaSources:
                if tag in ufoPath:
                    # get extrema source measurements
                    f = OpenFont(ufoPath, showInterface=False)
                    M.measure(f)

                    # create instance location from default + measurements
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1][4:])
                    valuePermill = permille(value, f.info.unitsPerEm)
                    L[tag] = valuePermill
                    for measurementName in self.parametricAxes:
                        if measurementName not in M.values:
                            continue
                        if measurementName not in self.parametricAxesParent:
                            continue

                        valueUnits = int(M.values[measurementName])
                        valuePermill = permille(valueUnits, f.info.unitsPerEm)
                        L[measurementName] = valuePermill

                    # add instance to designspace
                    I = InstanceDescriptor()
                    I.familyName     = self.familyName
                    I.styleName      = f.info.styleName.replace(' ', '')
                    I.name           = f.info.styleName.replace(' ', '')
                    I.designLocation = L
                    I.filename       = os.path.join('instances', f"{self.familyName}-{self.subFamilyName}_{os.path.split(ufoPath)[-1].split('_')[-1]}")
                    self.designspace.addInstance(I)

    def buildInstances(self, clear=True, ttf=False):
        if clear:
            instances = glob.glob(f'{self.instancesFolder}/*.ufo')
            for instance in instances:
                shutil.rmtree(instance)
        ufoProcessor.build(self.designspacePath)
        ufos = glob.glob(f'{self.instancesFolder}/*.ufo')

        # copy glyph order from default
        f = OpenFont(self.defaultUFO, showInterface=False)
        glyphOrder = f.glyphOrder
        f.close()

        for ufo in ufos:
            f = OpenFont(ufo, showInterface=False)
            f.glyphOrder = glyphOrder
            f.save()
            f.close()

        # convert all instances to ttf
        if ttf:
            for ufoPath in ufos:
                ufo = Font(ufoPath)
                ttf = compileTTF(ufo)
                ttfPath = ufoPath.replace('.ufo', '.ttf')
                ttf.save(ttfPath)

    # def addLibs(self):
    #     asciiGlyphs = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()
    #     f = OpenFont(self.defaultUFO, showInterface=False)
    #     allGlyphs = f.glyphOrder
    #     skipExportGlyphs = [g for g in allGlyphs if g not in asciiGlyphs]
    #     self.designspace.lib['public.skipExportGlyphs'] = skipExportGlyphs

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        self.addInstances()


class AmstelvarDesignSpaceBuilder1:
    '''
    - parametric axes
    - XTSP
    - blended axes
    - avar 2

    '''
    pass


class AmstelvarDesignSpaceBuilder2:
    '''
    3. default
    6 sources for 3 axes extrema

    '''
    pass



# -----
# build
# -----

if __name__ == '__main__':

    D = AmstelvarDesignSpaceBuilder()
    D.build()
    D.save()

    D = AmstelvarDesignSpaceBuilder0()
    D.build()
    D.save()
    D.buildInstances()
