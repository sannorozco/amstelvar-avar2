# menuTitle: find unwanted off-curve points
from importlib import reload
import xTools4.modules.validation
reload(xTools4.modules.validation)

from xTools4.modules.validation import findUnwantedQuadraticOffCurvePoints

font  = CurrentFont()

findUnwantedQuadraticOffCurvePoints(font)
