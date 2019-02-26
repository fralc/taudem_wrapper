#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python wrapper of Taudem binaries

Example of wrapper around a taudem command:
def pit_remove(dem_input, dem_output, nr_processes=_DEFAULT_NR_PROCESSES):
    mpiexec = os.path.join(_MPIEXEC_PATH, "mpiexec")
    taudem_command = os.path.join(_TAUDEM_PATH, "PitRemove")
    command = 'call "{:s}" -n {:d} "{:s}" -z "{:s}" -fel "{:s}"'.format(mpiexec, nr_processes, taudem_command,
                                                                   dem_input, dem_output)
    os.system(command)

"""

import os, sys
from yaml import load

_settings_path = os.path.join(os.path.dirname(__file__), 'taudem_settings.yaml')
with open(_settings_path, "r") as f:
    _taudem_settings = load(f)

if sys.platform == 'linux':
    _TAUDEM_PATH = _taudem_settings['TAUDEM_PATH_LINUX']
    _IS_LINUX = 1
else:
    _TAUDEM_PATH = _taudem_settings['TAUDEM_PATH_WIN']
    _IS_LINUX = 0

_MPIEXEC_PATH = _taudem_settings['MPIEXEC_PATH_WIN']
_DEFAULT_NR_PROCESSES = _taudem_settings['DEFAULT_NR_PROCESSES']


def taudem_function(taudem_command, input_list, output_list, option_list=None):
    arguments = input_list + output_list

    def function(arguments, nr_processes=_DEFAULT_NR_PROCESSES, **kwargs):
        if _IS_LINUX:
            mpiexec = "mpiexec"
            taudem_command_path = os.path.join(_TAUDEM_PATH, taudem_command.lower())
            command = "{:s} -n {:d} --allow-run-as-root {:s}".format(mpiexec, nr_processes, taudem_command_path)
        else:
            mpiexec = os.path.join(_MPIEXEC_PATH, "mpiexec")
            taudem_command_path = os.path.join(_TAUDEM_PATH, taudem_command)
            command = 'call "{:s}" -n {:d} "{:s}"'.format(mpiexec, nr_processes, taudem_command_path)

        for i in arguments:
            command += ' -{:s} "{:s}"'.format(i, kwargs[i])
        if option_list:
            for i in option_list:
                if isinstance(kwargs[i], str):
                    command += ' -{:s} {:s}'.format(i, kwargs[i])
                else:
                    command += ' -{:s} {}'.format(i, kwargs[i])

        os.system(command)

    return lambda **kwargs: function(arguments=arguments, **kwargs)


pit_remove = taudem_function(taudem_command='PitRemove',
                             input_list=['z'],
                             output_list=['fel'])

d8_flow_dir = taudem_function(taudem_command='D8FlowDir',
                              input_list=['fel'],
                              output_list=['p'])

dinf_flow_dir = taudem_function(taudem_command='DinfFlowDir',
                                input_list=['fel'],
                                output_list=['slp', 'ang'])

area_d8 = taudem_function(taudem_command='AreaD8',
                          input_list=['p'],
                          output_list=['ad8'])

area_dinf = taudem_function(taudem_command='AreaDinf',
                            input_list=['ang'],
                            output_list=['sca'])

dinf_dist_down = taudem_function(taudem_command='DinfDistDown',
                                 input_list=['ang', 'fel', 'slp', 'src'],
                                 output_list=['dd'],
                                 option_list=['m'])

stream_def_by_threshold = taudem_function(taudem_command='Threshold',
                                          input_list=['ssa'],
                                          output_list=['src'],
                                          option_list=['thresh'])

stream_net = taudem_function(taudem_command='StreamNet',
                             input_list=['fel', 'p', 'ad8', 'src'],
                             output_list=['ord', 'tree', 'coord', 'net', 'w'])



