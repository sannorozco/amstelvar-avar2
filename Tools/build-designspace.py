from importlib import reload
import xTools4.modules.sys
reload(xTools4.modules.sys)
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, glob, shutil, json, time, datetime
import subprocess
from xml.etree.ElementTree import parse
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from defcon import Font
from ufo2ft import compileVariableTTF
import ufoProcessor # upgrade to UFOOperator?
from extractor import extractUFO
from xTools4.modules.measurements import FontMeasurements, permille
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.sys import timer


### DEPRECATED!
def makeParentAxis(parentName, parametricAxes, defaultName):
    r'''
    Calculate a parent axis to control several parametric axes, 
    with mappings to limit the range of each child axis.

    ::
        parentName  = 'XTRA'
        parametricAxes = {
            'XTUC' : dict(minimum=72, maximum=668, default=400),
            'XTUR' : dict(minimum=60, maximum=902, default=561),
            'XTUD' : dict(minimum=76, maximum=686, default=410),
            'XTLC' : dict(minimum=42, maximum=500, default=243),
            'XTLR' : dict(minimum=46, maximum=625, default=337),
            'XTLD' : dict(minimum=84, maximum=501, default=248),
            'XTFI' : dict(minimum=40, maximum=604, default=329),
        }
        defaultName = 'XTUC'

        parentAxis, mappings = makeParentAxis(parentName, parametricAxes, defaultName)
        
        print('parent parametric axis:')
        print(parentAxis)
        print()
        print('parent mappings to child parameters:')
        for parentValue, mapping in sorted(mappings.items()):
            print(f'\t{ parentValue } { mapping }')

    '''
    # THIS IS THE WRONG PLACE FOR THIS KIND OF DATA!
    # MOVE TO DESIGNSPACE BUILDER? MEASUREMENTS FORMAT?
    matchRangeAxes = {
        'XQUC' : 'XTUR',
        'XQLC' : 'XTLR',
        'XQFI' : 'XTFI',
    }

    defaultValue = parametricAxes[defaultName]['default']
    minValues = []
    maxValues = []
    for axisName, axis in parametricAxes.items():
        # SKIP MATCHED RANGE AXES
        if axisName in matchRangeAxes:
            continue
        axisShift = defaultValue - axis['default'] 
        minValue  = axis['minimum'] + axisShift
        maxValue  = axis['maximum'] + axisShift
        minValues.append(minValue)
        maxValues.append(maxValue)
    
    parentAxis = {
        'name'    : parentName,
        'default' : defaultValue,
        'minimum' : min(minValues),
        'maximum' : max(maxValues),
    }

    mappingValues = set(minValues + maxValues)
    mappings = {}
    for mappingValue in sorted(mappingValues):
        mappings[mappingValue] = {}
        for axisName, axis in parametricAxes.items():
            # SKIP MATCHED RANGE AXES
            if axisName in matchRangeAxes:
                continue
            axisShift = defaultValue - axis['default'] 
            value = mappingValue - axisShift
            mappings[mappingValue][axisName] = value

    # ADD AXES WITH MATCHED RANGES

    for mappingValue, maps in mappings.items():
        for axisName, mapAxisName in matchRangeAxes.items():
            if mapAxisName in maps:
                
                axisDefault = parametricAxes[axisName]['default']
                axisMinimum = parametricAxes[axisName]['minimum']
                axisMaximum = parametricAxes[axisName]['maximum']

                mapAxisDefault = parametricAxes[mapAxisName]['default']
                mapAxisMinimum = parametricAxes[mapAxisName]['minimum']
                mapAxisMaximum = parametricAxes[mapAxisName]['maximum']

                mapAxisValue = maps[mapAxisName]

                if mappingValue < defaultValue:
                    axisRange = axisDefault    - axisMinimum   
                    mapRange  = mapAxisDefault - mapAxisMinimum
                    mapScale  = axisRange / mapRange
                    mapValue  = (mapAxisValue - mapAxisMinimum) * mapScale
                    axisValue = axisMinimum + mapValue

                elif mappingValue > defaultValue:
                    axisRange = axisMaximum    - axisDefault
                    mapRange  = mapAxisMaximum - mapAxisDefault
                    mapScale  = axisRange / mapRange
                    mapValue  = (mapAxisValue - mapAxisDefault) * mapScale
                    axisValue = axisDefault + mapValue

                maps[axisName] = int(axisValue)

    return parentAxis, mappings


class AmstelvarA2DesignSpaceBuilder:
    '''
    Builds the AmstelvarA2 designspace from:

    - UFO sources
    - blends.json
    - measurements.json

    Build steps:

    - build blends file
    - create designspace
    - add blended axes
    - add parametric axes
    - add mappings
    - add default source
    - add parametric sources
    - add instances

    see also: recipe.md

    '''
    familyName  = 'AmstelvarA2'
    defaultName = 'wght400'

    parentAxesBuild  = False
    parentAxesRoman  = 'XOPQ YOPQ XTRA XSHA YSHA XSVA YSVA XVAA YHAA'.split() # XTEQ YTEQ
    parentAxesItalic = parentAxesRoman

    parentAxesDefaults = {
        'XOPQ' : 'XOUC',
        'YOPQ' : 'YOUC',
        'XTRA' : 'XTUC',
        'XSHA' : 'XSHU',
        'YSHA' : 'YSHU',
        'XSVA' : 'XSVU',
        'YSVA' : 'YSVU',
        'XVAA' : 'XVAU',
        'YHAA' : 'YHAU',
        'XTEQ' : 'XQUC',
        'YTEQ' : 'YQUC',
    }
                                      # UPPERCASE                                                                               # LOWERCASE                                                                                         # FIGURES                                                        # VARIETY
    parametricAxesRoman  = 'WDSP GRAD XOUC YOUC XTUC XTUR XTUD XTUA YTUC XSHU YSHU XSVU YSVU XVAU YHAU XQUC YQUC XUCS XUCR XUCD XOLC YOLC XTLC XTLR XTLD XTLA YTLC YTAS YTDE XSHL YSHL XSVL YSVL XVAL YHAL XLCS XLCR XLCD XQLC YQLC XOFI YOFI XTFI YTFI XSHF YSHF XSVF YSVF XVAF YHAF XQFI YQFI XFIR XDOT YTOS XTTW YTTL BARS'.split()
    parametricAxesItalic = parametricAxesRoman

    spacingAxes = [
        'XUCS', 'XUCR', 'XUCD',
        'XLCS', 'XLCR', 'XLCD',
        'XFIR', # 'XFIS', 
    ]

    def __init__(self, subFamilyName='Roman'):
        self.subFamilyName = subFamilyName
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def designspaceName(self):
        return f'{self.familyName}-{self.subFamilyName}_avar2.designspace'

    @property
    def baseFolder(self):
        return os.path.dirname(os.getcwd())

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, 'Sources', self.subFamilyName)

    @property
    def instancesFolder(self):
        return os.path.join(self.sourcesFolder, 'instances')

    @property
    def instances(self):
        D = DesignSpaceDocument()
        D.read(self.designspacePath)
        return D.instances

    @property
    def varFontsFolder(self):
        return os.path.join(self.baseFolder, 'Fonts')

    @property
    def varFontPath(self):
        return os.path.join(self.varFontsFolder, self.designspaceName.replace('.designspace', '.ttf'))

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
        L['GRAD'] = 0
        return L

    @property
    def amstelvarFolder(self):
        # path to a local copy of http://github.com/gferreira/amstelvar
        return os.path.join(os.path.dirname(self.baseFolder), 'amstelvar')

    @property
    def amstelvarBlendsPath(self):
        return os.path.join(self.amstelvarFolder, self.subFamilyName, 'blends.json')

    @property
    def blendsPath(self):
        return os.path.join(self.sourcesFolder, 'blends.json')

    @property
    def blendedAxes(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['axes']

    @property
    def blendedSources(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['sources']

    @property
    def parametricAxes(self):
        if self.subFamilyName == 'Italic':
            return self.parametricAxesItalic
        else:
            return self.parametricAxesRoman

    # methods

    def addParametricAxes(self):

        for name in self.parametricAxes:
            # get default value
            if name == 'GRAD':
                defaultValue = 0
            else:
                defaultValue = permille(self.measurementsDefault.values[name], self.unitsPerEm)
            # get min/max values from file names
            values = []
            for ufo in self.parametricSources:
                if name in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            if len(values) == 2:
                values.sort()
                minValue, maxValue = values
            elif len(values) == 1:
                values.append(defaultValue)
                values.sort()
                minValue, maxValue = values
            else:
                print(f'ERROR: {name}: {values}')
                # continue

            # create axis
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = minValue
            a.maximum = maxValue
            a.default = defaultValue
            self.designspace.addAxis(a)

    def addDefaultSource(self):
        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = f'{self.familyName} {self.subFamilyName}'
        src.styleName  = self.defaultName
        src.location   = self.defaultLocation
        self.designspace.addSource(src)

    def addParametricSources(self):
        for name in self.parametricAxes:
            for ufo in self.parametricSources:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = f'{self.familyName} {self.subFamilyName}'
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    src.styleName  = f'{name}{value}'
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def addInstances(self):
        for styleName in self.blendedSources.keys():
            # only add opsz/wght/wdth as instances
            if not ('opsz' in styleName or 'wght' in styleName or 'wdth' in styleName):
                continue
            # if styleName == 'wght400':
            #     continue

            L = self.defaultLocation.copy()
            for axis, value in self.blendedSources[styleName].items():
                L[axis] = value

            I = InstanceDescriptor()
            I.familyName     = f'{self.familyName} {self.subFamilyName}'
            I.styleName      = styleName.replace('_', ' ')
            I.name           = styleName
            I.designLocation = L
            I.filename       = os.path.join('instances', f'{self.familyName}-{self.subFamilyName}_{styleName}.ufo')

            self.designspace.addInstance(I)

    def addBlendedAxes(self):
        for tag in self.blendedAxes.keys():
            a = AxisDescriptor()
            a.name    = self.blendedAxes[tag]['name']
            a.tag     = tag
            a.minimum = self.blendedAxes[tag]['minimum']
            a.maximum = self.blendedAxes[tag]['maximum']
            a.default = self.blendedAxes[tag]['default']
            self.designspace.addAxis(a)

    def buildBlendsFile(self):
        if not os.path.exists(self.amstelvarBlendsPath):
            return

        # import Amstelvar blends
        with open(self.amstelvarBlendsPath, 'r', encoding='utf-8') as f:
            blendsDict = json.load(f)

        # -------------
        # add XTSP axis
        # -------------

        blendsDict['axes']['XTSP'] = {
            "name"    : "XTSP",
            "default" : 0,
            "minimum" : -100,
            "maximum" : 100,
        }
        blendsDict['sources']['XTSP-100'] = self.defaultLocation.copy()
        blendsDict['sources']['XTSP100'] = self.defaultLocation.copy()

        for axisName in self.spacingAxes:
            values = []    
            for ufo in self.parametricSources:
                value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                if axisName in ufo:
                    values.append(value)
            assert len(values)
            values.sort()
            blendsDict['sources']['XTSP-100'][axisName] = values[0]
            blendsDict['sources']['XTSP100'][axisName] = values[1]

        # -----------------------
        # add blended PARENT axes
        # -----------------------

        if self.parentAxesBuild:

            measurements = readMeasurements(self.measurementsPath)
            fontMeasurements = measurements['font']
            parentAxes = self.parentAxesRoman if self.subFamilyName == 'Roman' else self.parentAxesItalic

            for parentAxisName in parentAxes:
                parentMeasurement = fontMeasurements[parentAxisName]

                # get parametric axes for parent
                parametricAxes = {}
                childNames = [a[0] for a in fontMeasurements.items() if a[1]['parent'] == parentAxisName]
                for childName in childNames:
                    # get min/max values from file names
                    values = []
                    for ufo in self.parametricSources:
                        if childName in ufo:
                            value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                            values.append(value)
                    if not len(values) == 2:
                        print(parentAxisName, childName, values)
                        continue
                    values.sort()

                    parametricAxes[childName] = {
                        'minimum' : values[0],
                        'maximum' : values[1],
                        'default' : self.defaultLocation[childName],
                    }

                parentDefault = self.parentAxesDefaults[parentAxisName]
                parentAxis, mappings = makeParentAxis(parentAxisName, parametricAxes, parentDefault)

                # add parent axis
                blendsDict['axes'][parentAxisName] = parentAxis

                # add parametric mappings
                for mappingValue in mappings:
                    blendsDict['sources'][f'{parentAxisName}{mappingValue}'] = {}
                    for parametricAxisName, parametricValue in mappings[mappingValue].items():
                        blendsDict['sources'][f'{parentAxisName}{mappingValue}'][parametricAxisName] = parametricValue

        # -----------------------
        # save AmstelvarA2 blends
        # -----------------------

        with open(self.blendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

    def patchBlendsFile(self):

        # import blends data
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsDict = json.load(f)

        # import & apply patch data
        patchPath = self.blendsPath.replace('.json', '_patch.json')
        with open(patchPath, 'r', encoding='utf-8') as f:
            patchDict = json.load(f)

        for key1, value1 in patchDict.items():
            if key1 not in blendsDict:
                print(f'{key1} not in blends dict')
                continue
            for key2, value2 in value1.items():
                blendsDict[key1][key2] = value2

        # # save patched blends data
        # with open(self.blendsPath, 'w', encoding='utf-8') as f:
        #     json.dump(blendsDict, f, indent=2)

    def addMappings(self):

        blendedAxes    = self.blendedAxes
        blendedSources = self.blendedSources

        for styleName in blendedSources.keys():
            m = AxisMappingDescriptor()

            # get input value from style name
            inputLocation = {}
            for param in styleName.split('_'):
                tag   = param[:4]
                value = int(param[4:])
                axisName  = blendedAxes[tag]['name']
                inputLocation[axisName] = value

            # if 'XTSP' not in styleName:
            #     inputLocation['XTRA'] = int(blendedSources[styleName]['XTUC'])

            # get output value from blends.json file
            outputLocation = {}
            for axisName in blendedSources[styleName]:
                outputLocation[axisName] = int(blendedSources[styleName][axisName])

            m.inputLocation  = inputLocation
            m.outputLocation = outputLocation
            m.description    = styleName

            self.designspace.addAxisMapping(m)

    def save(self):
        if not self.designspace:
            return
        print(f'saving...', end=' ')
        self.designspace.write(self.designspacePath)
        print(os.path.exists(self.designspacePath))

    def build(self):
        print(f'building {os.path.split(self.designspacePath)[-1]}...')
        self.buildBlendsFile()
        # self.patchBlendsFile()
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addMappings()
        self.addDefaultSource()
        self.addParametricSources()
        self.addInstances()

    def buildInstances(self, clear=True):

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

    def buildVariableFont(self, subset=None, setVersionInfo=True, debug=False):

        print(f'generating variable font for {self.designspaceName}...')

        D = DesignSpaceDocument()
        D.read(self.designspacePath)
        print(f'\tloading sources...')
        for src in D.sources:
            if debug:
                print(f'\t\tloading {src.familyName} {src.styleName}...')
            src.font = Font(src.path)

        ###
        ### REWRITE VARIABLE FONT GENERATION HERE
        ###

        # subset ascii variable font with pyftsubset
        if subset:
            print('\tsubsetting variable font...')
            asciiGlyphs = subset.split()
            font = TTFont(self.varFontPath)
            subsetter = Subsetter()
            subsetter.populate(glyphs=asciiGlyphs)
            subsetter.subset(font)
            font.save(self.varFontPath)

        # set version info in the font's unique name
        if setVersionInfo:
            print('\tsetting version info...')
            # convert ttf to ttx
            ttxPath = self.varFontPath.replace('.ttf', '.ttx')
            tt = TTFont(self.varFontPath)
            tt.verbose = False
            tt.saveXML(ttxPath)
            tt.close()
            # make unique name with timestamp
            timestamp = time.strftime("%Y%m%d%H%M", time.localtime())
            uniqueName = f'{self.familyName} {self.subFamilyName} {timestamp}'
            # add version info to unique name -- nameID 3
            tree = parse(ttxPath)
            root = tree.getroot()
            for child in root.find('name'):
                if child.attrib['nameID'] == '3':
                    child.text = uniqueName
            tree.write(ttxPath)
            # convert ttx back to ttf
            tt = TTFont()
            tt.verbose = False
            tt.importXML(ttxPath)
            tt.save(self.varFontPath)
            tt.close()
            # clear ttx file
            os.remove(ttxPath)

        print('...done.\n')

    def buildInstancesVariableFont(self, clear=True, ufo=False):

        varInstancesFolder = os.path.join(self.varFontsFolder, 'instances', self.subFamilyName)

        if clear:
            varInstances = glob.glob(f'{varInstancesFolder}/*.ttf')
            for instance in varInstances:
                os.remove(instance)
            if ufo:
                ufos = glob.glob(f'{varInstancesFolder}/*.ufo')
                for ufo in ufos:
                    shutil.rmtree(ufo)

        # http://stackoverflow.com/questions/65184937/fatal-python-error-init-fs-encoding-failed-to-get-the-python-codec-of-the-file
        if 'PYTHONHOME' in os.environ:
           del os.environ['PYTHONHOME']

        print(f"building AmstelvarA2 {self.subFamilyName} instances...")

        for instance in self.instances:
            ttfPath = os.path.join(varInstancesFolder, f'AmstelvarA2-{self.subFamilyName}_avar2_{instance.name}.ttf')
            print(f"\tbuilding {instance.name}...", end=' ')
            cmd  = ['/opt/homebrew/bin/fontmake']
            cmd += ['-m', self.designspacePath]
            cmd += ['-o', 'ttf']
            cmd += ['-i', instance.name, '--expand-features-to-instances']
            cmd += ['--feature-writer', 'None']
            cmd += ['--output-path', ttfPath]
            cmd += ['--keep-direction', '--keep-overlaps']
            cmd += ['--verbose ERROR']
            cmd  = ' '.join(cmd)

            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
                for line in p.stdout.readlines():
                    print(line,)
                retval = p.wait()

            print(f'({os.path.exists(ttfPath)})')

        if ufo:
            print(f"Converting instances to UFO format...")
            ttfPaths = glob.glob(f'{varInstancesFolder}/*.ttf')
            for ttfPath in ttfPaths:
                ufo = Font()
                extractUFO(ttfPath, ufo)
                ufoPath = ttfPath.replace('.ttf', '.ufo')
                print(f"\tSaving {os.path.split(ufoPath)[-1]}...")
                ufo.save(ufoPath)

            # set slant offset in Italic fonts
            ufoPaths = glob.glob(f'{varInstancesFolder}/*.ufo')
            defaultFont = OpenFont(self.defaultUFO, showInterface=False)
            slantOffset = defaultFont.lib.get('com.typemytype.robofont.italicSlantOffset')
            if slantOffset:
                for ufoPath in ufoPaths:
                    f = OpenFont(ufoPath, showInterface=False)
                    f.features.text = '' # clear OpenType features
                    f.lib['com.typemytype.robofont.italicSlantOffset'] = slantOffset
                    f.save()
                    f.close()

        print("done!")

    def printAxes(self):

        measurements = {}
        for d in self.measurementsDefault.definitions:
            measurements[d[0]] = d[7]

        print('### Parent parametric axes\n')
        for n, axis in enumerate(self.parentAxesRoman):
            print(f'{n+1}. `{axis}` {measurements[axis]}')

        print('\n### Parametric axes\n')
        for n, axis in enumerate(self.parametricAxesRoman):
            print(f'{n+1}. `{axis}` {measurements[axis]}')

# -----
# build
# -----

if __name__ == '__main__':

    subFamilyName = ['Roman', 'Italic'][0]

    start = time.time()

    D2 = AmstelvarA2DesignSpaceBuilder(subFamilyName)
    D2.build()
    D2.save()
    # D2.buildVariableFont(subset=None, setVersionInfo=True, debug=False)
    # D2.buildInstancesVariableFont(clear=True, ufo=True)
    # D2.printAxes()

    end = time.time()

    timer(start, end)
