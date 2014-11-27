Traits-Enaml
============

Traits-Enaml is an extension library to facilitate interoperation of `Enaml
0.8.x` with `Traits` and allow a programmer to drive enaml views using
traits models, enable/chaco components and mayavi 3D scenes.

Usage
-----

To use traits model classes to drive enaml components it is enough to
use the `with traits_enaml.imports():` context manager.

Example python code:

.. literalinclude:: ../examples/traits_view/person.py

And related Enaml definition:

.. literalinclude:: ../examples/traits_view/traits_view.enaml

Widgets
=======

To further simplify the inter-operation with traits-related libraries
additional widgets and factories are provided. These components are available
in the `widgets` module.

AutoView
--------

Using the **auto_window** or the **auto_view** factories we can create Enaml
components for `HasTraits` classes in an automatic way similar to the
default TraitsUI views.

Example python code using the *auto_window* factory:

.. literalinclude:: ../examples/auto_view/auto_view.py

TraitsView
----------

Complete TraitsUI Views can be embedded inside an enaml component using the
:class:`~traits_enaml.widgets.traits_view.TraitsView` widget.

.. autoclass:: traits_enaml.widgets.traits_view.TraitsView

EnableCanvas
------------

Enable and Chaco components can be embedded inside an enaml
component using the :class:`~traits_enaml.widgets.enable_canvas.EnableCanvas`
widget.

.. autoclass:: traits_enaml.widgets.enable_canvas.EnableCanvas

MayaviCanvas
------------

To embed a Mayavi 3D scene inside an Enaml component, one should use the
:class:`~traits_enaml.widgets.mayavi_canvas.MayaviCanvas` widget.

.. autoclass:: traits_enaml.widgets.mayavi_canvas.MayaviCanvas


GLCanvas
--------

To embed an OpenGL 3D scene inside an Enaml component, one should use the
:class:`~traits_enaml.widgets.gl_canvas.GLCanvas` widget.

.. autoclass:: traits_enaml.widgets.gl_canvas.GLCanvas
