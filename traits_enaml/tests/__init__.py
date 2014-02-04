# load qt from enaml in order to set the setapi before the tests import
# QtCore (see github issue #39).
from enaml import qt
del qt
