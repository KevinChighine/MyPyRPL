import numpy as np
from qtpy import QtCore
from ..attributes import FloatProperty, BoolRegister, FloatRegister, GainRegister
from ..modules import HardwareModule, SignalModule
from . import FilterModule, DspModule
from ..pyrpl_utils import sorted_dict
from .dsp import all_inputs, dsp_addr_base, InputSelectRegister, all_output_directs
from ..attributes import BoolRegister, FloatRegister, SelectRegister, \
    IntRegister, PhaseRegister, FrequencyRegister, FloatProperty, \
    FilterRegister, FilterProperty, GainRegister

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from ..widgets.module_widgets import HazeWidget

#class Haze(DspModule):
#  we do not want all the logic from dsp modules to be applied to haze,
# only selectivel copy-paste some code snippets from dsp.py
class Haze(HardwareModule, SignalModule):  # same as DspModule
    addr_base = dsp_addr_base('haze0') # same as 0x40330000 but more flexible if we change sth
    _widget_class = HazeWidget

    _setup_attributes = ["input1",
                         "input2",
                         "p1",
                         "p2",
                         "output_direct1",
                         "output_direct2",
                         #"output_signal"
                         #"setpoint",
                         #"d",
                         #"inputfilter",
                         #"max_voltage",
                         #"min_voltage"
                         ]
    _gui_attributes = _setup_attributes

    input1 = InputSelectRegister(0x0, # this way of writing ensures that both haze modules get the same
                                 options=all_inputs,
                                 default='in1',
                                 doc="selects the input signal 1 of the module")

    input2 = InputSelectRegister(0x10000,
                                 options=all_inputs,
                                 default='in2',
                                 doc="selects the input signal 2 of the module")

    output_direct1 = SelectRegister(0x4,
                                   options=all_output_directs,
                                   doc="selects to which analog output the "
                                       "module output signal 1 is sent directly")

    output_direct2 = SelectRegister(0x10004,
                                   options=all_output_directs,
                                   doc="selects to which analog output the "
                                       "module output signal 2 is sent directly")

    # multiplexer for internal output signal, yet to be implemented
    #_output_signals = sorted_dict(
    #       output_direct1=0,
    #       output_direct2=1,
    #       off=2,
    #       )

    #output_signals = _output_signals.keys()
    #output_signal = SelectRegister(0x10C, options=_output_signals,
    #                doc="Signal to send back to DSP multiplexer")

    _PSR = 12  # Register(0x200)
    _ISR = 12  # Register(0x204)
    _GAINBITS = 24  # Register(0x20C)

    p1 = GainRegister(0x108, bits=_GAINBITS, norm= 2 **_PSR,
                      doc="Haze proportional gain [1]")
    p2 = GainRegister(0x10C, bits=_GAINBITS, norm= 2 **_ISR,
                      doc="Haze proportional gain 2 [1]")

    ##############################
    # copy-paste from DspModule, not really needed, but here for completeness until we delete it
    ###############################3
    def __init__(self, rp, name):
        super(Haze, self).__init__(rp, name)

    # copy-paste from DspModule, not needed, really
    _delay = 0  # delay of the module from input to output_signal (in cycles)

    @property
    def inputs(self):
        return all_inputs(self).keys()

    @property
    def output_directs(self):
        return all_output_directs(self).keys()

    out1_saturated = BoolRegister(0x8, 0, doc="True if out1 is saturated")

    out2_saturated = BoolRegister(0x8, 1, doc="True if out2 is saturated")

    # the function is here so the metaclass generates a setup(**kwds) function
    @property
    def inputs(self):
        return list(all_inputs(self).keys())
    ##############################
    # end of copy-paste from DspModule
    ###############################3

