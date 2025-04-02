import os, glob, datetime
from xTools4.modules.measurements import Measurement

subFamilyName    = ['Roman', 'Italic'][1]
fontsFolder      = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
familyName       = 'Amstelvar'
baseFolder       = os.path.join(fontsFolder, 'amstelvar')
instancesFolder  = os.path.join(baseFolder, subFamilyName)
instances        = glob.glob(f'{instancesFolder}/*.ufo')
measurementsPath = os.path.join(baseFolder, subFamilyName, 'measurements.json')

XUCS_left  = Measurement('XUCS_left',  'x', 'H', -1, 'H', 4)
XUCS_right = Measurement('XUCS_right', 'x', 'H', 31, 'H', 99)

XUCR_left  = Measurement('XUCR_left',  'x', 'O', -1, 'O', 0)
XUCR_right = Measurement('XUCR_right', 'x', 'O',  6, 'O', 99)

XUCD_left  = Measurement('XUCD_left',  'x', 'V', -1, 'V', 19)
XUCD_right = Measurement('XUCD_right', 'x', 'V', 14, 'V', 99)

# M1 = Measurement('XLCS_left',  'x', 'n', -1, 'n', 3)
# M2 = Measurement('XLCS_right', 'x', 'n', 28, 'n', 99)

for ufoPath in instances:
    f = OpenFont(ufoPath, showInterface=False)
    XUCS_left_  = XUCS_left.measure(f)
    XUCS_right_ = XUCS_right.measure(f)
    XUCS_diff   = XUCS_right_ - XUCS_left_

    XUCR_left_  = XUCR_left.measure(f)
    XUCR_right_ = XUCR_right.measure(f)
    XUCR_diff   = XUCR_right_ - XUCR_left_

    XUCD_left_  = XUCD_left.measure(f)
    XUCD_right_ = XUCD_right.measure(f)
    XUCD_diff   = XUCD_right_ - XUCD_left_

    print(f.info.styleName)
    print(f'\tXUCS {XUCS_diff} ({XUCS_left_} {XUCS_right_})')
    print(f'\tXUCR {XUCR_diff} ({XUCR_left_} {XUCR_right_})')
    print(f'\tXUCD {XUCD_diff} ({XUCD_left_} {XUCD_right_})')
    print()    

# # sources[styleName] = { k: permille(v, f.info.unitsPerEm) for k, v in M.values.items() if k in parametricAxes }
