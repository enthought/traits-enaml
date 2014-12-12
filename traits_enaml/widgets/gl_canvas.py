#----------------------------------------------------------------------------
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in /LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#----------------------------------------------------------------------------
from atom.api import set_default

from enaml.version import version_info as enaml_version
if enaml_version < (0, 9, 6):
    raise ImportError('This widget requires enaml >= 0.9.6')

from enaml.widgets.api import RawWidget
from enaml.core.declarative import d_func

from enaml.qt.QtOpenGL import QGLWidget


class _GLWidget(QGLWidget):
    """ A QGLWidget that calls through to the declarative's methods.
    """
    def __init__(self, parent, declarative):
        super(_GLWidget, self).__init__(parent)
        self.declarative = declarative

    def initializeGL(self):
        self.declarative.init_gl()

    def resizeGL(self, width, height):
        self.declarative.resize_gl(width, height)

    def paintGL(self):
        self.declarative.draw_gl()


class GLCanvas(RawWidget):
    """ A widget that displays OpenGL content.
    Note: This widget requires an enaml version >= 0.9.6 to run!

    :Methods:
        **draw_gl** = *d_func(draw_gl())*
            Draw the OpenGL scene.
        **init_gl** = *d_func(init_gl())*
            Initialize the GL context.
        **resize_gl** = *d_func(resize_gl(width, height))*
            Handle a resize event.

    """

    #: Expand freely in height by default
    hug_height = set_default('ignore')

    #: Expand freely in width by default
    hug_width = set_default('ignore')

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------

    def create_widget(self, parent):
        """ Create the underlying QWidget object.

        """
        return _GLWidget(parent, self)

    #--------------------------------------------------------------------------
    # Declarative methods
    #--------------------------------------------------------------------------

    @d_func
    def draw_gl(self):
        """ A method invoked to draw the contents of the widget.
        """

    @d_func
    def init_gl(self):
        """ A method invoked when a GL context is assigned to the widget.
        """

    @d_func
    def resize_gl(self, width, height):
        """ A method invoked when the size of the GL context changes.

        Parameters
        ----------
        width : int
            The new width of the context, in device pixels.
        height : int
            The new height of the context, in device pixels.

        """

    #--------------------------------------------------------------------------
    # Public interface
    #--------------------------------------------------------------------------

    def update(self):
        """ Force the draw_gl() method to be called.
        """
        self.get_widget().updateGL()
