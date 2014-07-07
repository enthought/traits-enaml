#----------------------------------------------------------------------------
#
#  Copyright (c) 2013-14, Enthought, Inc.
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

from numpy import exp, linspace, meshgrid

import traits_enaml
from enaml.qt.qt_application import QtApplication
from traits.api import HasStrictTraits, Instance
from chaco.api import ArrayPlotData, jet, Plot

class Model(HasStrictTraits):

    plot = Instance(Plot, ())

    def _plot_default(self):
        # Create a scalar field to colormap
        xs = linspace(0, 10, 600)
        ys = linspace(0, 5, 600)
        x, y = meshgrid(xs,ys)
        z = exp(-(x**2+y**2)/100)

        # Create a plot data object and give it this data
        pd = ArrayPlotData()
        pd.set_data("imagedata", z)

        # Create the plot
        plot = Plot(pd)
        plot.img_plot("imagedata", colormap=jet)
        return plot



if __name__ == '__main__':
    with traits_enaml.imports():
        from enable_canvas import Main

    app = QtApplication()
    view = Main(model=Model())
    view.show()

    app.start()
