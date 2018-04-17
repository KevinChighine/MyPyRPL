import numpy as np
from qtpy import QtCore
from ..attributes import FloatProperty, BoolRegister, FloatRegister, GainRegister
from ..modules import HardwareModule
from . import FilterModule
from ..pyrpl_utils import sorted_dict
from .dsp import all_inputs, dsp_addr_base, InputSelectRegister
from ..attributes import BoolRegister, FloatRegister, SelectRegister, \
    IntRegister, PhaseRegister, FrequencyRegister, FloatProperty, \
    FilterRegister, FilterProperty, GainRegister

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from ..widgets.module_widgets import HazeWidget

#logger = logging.getLogger(name=__name__)

class Haze1(FilterModule, HardwareModule):
    addr_base=0x40330000

    _widget_class = HazeWidget
    _setup_attributes = ["input1",
                         "input2",
                         "p1",
                         "p2",
                         "output_direct"]
                         #"output_signal"]
                         #"setpoint",

                         #"d",
                         #"inputfilter",
                         #"max_voltage",
                         #"min_voltage"]
    _gui_attributes = _setup_attributes

    _output_signals = sorted_dict(
        output_direct=1,
        pfd=2,
        off=3,
        V=4,
        R=0)


    #output_signals = _output_signals.keys()
    #output_signal = SelectRegister(0x10C, options=_output_signals,
    #                               doc="Signal to send back to DSP multiplexer")
    @property
    # the function is here so the metaclass generates a setup(**kwds) function

    def inputs(self):
        return list(all_inputs(self).keys())

    input1 = InputSelectRegister(-addr_base+dsp_addr_base('haze1')+0x0,
                                 options=all_inputs,
                                 default='in1',
                                 doc="selects the input signal 1 of the module")

    input2 = InputSelectRegister(-addr_base+dsp_addr_base('haze1')+0x10000,
                                 options=all_inputs,
                                 default='in2',
                                 doc="selects the input signal 2 of the module")

    _PSR = 12  # Register(0x200)
    _ISR = 12  # Register(0x204)
    _GAINBITS = 24  # Register(0x20C)

    #output_signals = _output_signals.keys()
    #output_signal = SelectRegister(0x10C, options=_output_signals,
    #                doc="Signal to send back to DSP multiplexer")

    p1 = GainRegister(0x108, bits=_GAINBITS, norm= 2 **_PSR,
                      doc="Haze proportional gain [1]")
    p2 = GainRegister(0x10C, bits=_GAINBITS, norm= 2 **_ISR,
                      doc="Haze proportional gain 2 [1]")
