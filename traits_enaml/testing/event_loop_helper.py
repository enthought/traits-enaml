# Copyright (c) 2012-2013 by Enthought Inc.
import contextlib
import threading

from enaml.application import deferred_call
from enaml.qt import QtCore, QtGui
from traits.api import HasStrictTraits, Instance


class ConditionTimeoutError(RuntimeError):
    pass


class EventLoopHelper(HasStrictTraits):

    qt_app = Instance(QtGui.QApplication)

    def event_loop_with_timeout(self, repeat=2, timeout=10.0):
        """Helper function to send all posted events to the event queue and
        wait for them to be processed.  This runs the real event loop and
        does not emulate it with QApplication.processEvents.

        Parameters
        ----------
        repeat : int
            Number of times to process events. Default is 2.
        timeout: float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.

        """
        def repeat_loop(condition, repeat):
            # We sendPostedEvents to ensure that enaml events are processed
            self.qt_app.sendPostedEvents()
            repeat = repeat - 1
            if repeat <= 0:
                deferred_call(condition.set)
            else:
                deferred_call(repeat_loop, condition=condition, repeat=repeat)

        condition = threading.Event()
        deferred_call(repeat_loop, repeat=repeat, condition=condition)
        self.event_loop_until_condition(
            condition=condition.is_set, timeout=timeout)

    def event_loop(self, repeat=1):
        """Emulates an event loop `repeat` times with
        QApplication.processEvents.

        Parameters
        ----------
        repeat : int
            Number of times to process events. Default is 1.

        """
        for i in range(repeat):
            self.qt_app.sendPostedEvents()
            self.qt_app.processEvents()

    def event_loop_until_condition(self, condition, timeout=10.0):
        """Runs the real Qt event loop until the provided condition evaluates
        to True.

        Raises ConditionTimeoutError if the timeout occurs before the condition
        is satisfied.

        Parameters
        ----------
        condition : callable
            A callable to determine if the stop criteria have been met. This
            should accept no arguments.

        timeout : float
            Number of seconds to run the event loop in the case that the trait
            change does not occur.

        """
        def handler():
            if condition():
                self.qt_app.quit()
        condition_timer = QtCore.QTimer()
        condition_timer.setInterval(0.05)
        condition_timer.timeout.connect(handler)
        timeout_timer = QtCore.QTimer()
        timeout_timer.setSingleShot(True)
        timeout_timer.setInterval(timeout * 1000)
        timeout_timer.timeout.connect(self.qt_app.quit)
        timeout_timer.start()
        condition_timer.start()
        try:
            self.qt_app.exec_()
            if not timeout_timer.isActive():
                # We exited the event loop on timeout
                raise ConditionTimeoutError('Timed out waiting for condition')
        finally:
            timeout_timer.stop()
            condition_timer.stop()

    @contextlib.contextmanager
    def delete_widget(self, widget, timeout=1.0):
        """Runs the real Qt event loop until the widget provided has been
        deleted.  Raises ConditionTimeoutError on timeout.

        Parameters
        ----------
        widget : QObject
            The widget whose deletion will stop the event loop.

        timeout : float
            Number of seconds to run the event loop in the case that the
            widget is not deleted.

        """
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.setInterval(timeout * 1000)
        timer.timeout.connect(self.qt_app.quit)
        widget.destroyed.connect(self.qt_app.quit)
        yield
        timer.start()
        self.qt_app.exec_()
        if not timer.isActive():
            # We exited the event loop on timeout
            raise ConditionTimeoutError(
                'Could not destroy widget before timeout: {!r}'.format(widget))