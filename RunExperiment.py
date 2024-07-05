﻿# ==================== Imports ==================== #
# Modules that have been imported once in Zen are not
# imported again even if their content has changed.
# To workaround this issue, we use the reload function.

import _cd7_functions, _logging, _sample_functions, _automatic_data_transfer

reload(_cd7_functions)
reload(_logging)
reload(_sample_functions)
reload(_automatic_data_transfer)

from _cd7_functions import set_magnification, TruncatedExperiment
from _logging import log_message
from _sample_functions import get_barcode, get_timestamp
from _automatic_data_transfer import start_transfer

clr.AddReferenceByPartialName('Zeiss.Micro.AMP')
from Zeiss.Micro.AMP.Scripting import LiveScanScriptingPlugin

# ==================== Settings ==================== #

verbose = True
log_path = 'D:\UserData\david\log.txt'
log_message(log_path, verbose, '==================== Running macro ====================')

experimentName = 'SpiroC_Robot'
plateType = 'Aceto96.czsht'
additionalParameter = ''

dataPath = 'D:/UserData/Transfer/'

screening_experiments = ['SpiroC_Robot', 'SpiroC_Robot_Testing']
testing_index = 1
actual_experiments = ['SpiroC_V010_Robot-4Channels', 'MS-PlateOverview-003']

skip_experiment = False
skip_overview = False

# ==================== Data transfer ==================== #
transfer_status = start_transfer()

if transfer_status == -1:
    log_message(log_path, verbose, 'Warning: automatic data tranfser could not be started. Please copy the data manually.')
elif transfer_status == 0:
    log_message(log_path, verbose, 'Automatic data tranfser: started.')
else:
    log_message(log_path, verbose, 'Warning: automatic data tranfser already active.')

# ==================== Main ==================== #

ZenLiveScan = LiveScanScriptingPlugin.Instance

# Is the macro executed by the robot?
try:
    experimentName = sys.argv[1]
    plateType = sys.argv[2]
    additionalParameter = sys.argv[3]

    robot_execution = True
except:
    # In manual execution, load the sample.
    ZenLiveScan.LoadTrayAndPrescan()

    robot_execution = False

log_message(log_path, verbose, 'Robot execution: {}'.format(robot_execution))

# From Zeiss boilerplate template (?).
if experimentName == '':
    print('Experiment name cannot be empty.')
# Screening experiment.
elif experimentName in screening_experiments:
    testing = False
    if experimentName == screening_experiments[testing_index]:
        testing = True

    log_message(log_path, verbose, 'Testing: {}'.format(testing))

    # A timestamp is also found in the metadata. However, a single
    # timestamp is wanted for both experiments in a run as they
    # should be identified as belonging to the same run.
    timestamp = get_timestamp()

    # =============== Main experiment =============== #
    
    objective_position = '5x0.35NA'
    optovar_position = '2x'
    if not set_magnification(Zen, objective_position, optovar=optovar_position):
        log_message(log_path, verbose, 'Warning: Unable to set magnification.')
    else:
        log_message(log_path, verbose, 'Magnification set: {0} | {1}'.format(objective_position, optovar_position))

    experimentName = actual_experiments[0]
    if testing:
        truncated_experiment = TruncatedExperiment(Zen, experimentName)
        experimentName = truncated_experiment.truncated_experiment_name

    exp = Zen.Acquisition.Experiments.GetByName(experimentName)
    exp.SetActive()
    
    if skip_experiment:
        log_message(log_path, verbose, 'Skip experiment.')
    else:
        log_message(log_path, verbose, 'Running experiment: {}'.format(experimentName))
    
        PlateScan = Zen.Acquisition.Execute(exp)
    
        log_message(log_path, verbose, 'Experiment completed.')
    
        barcode = get_barcode(PlateScan)
    
        log_message(log_path, verbose, 'Barcode: {}'.format(barcode))
    
        filename = dataPath + barcode + '-unprocessed-' + timestamp + '.czi'
        log_message(log_path, verbose, 'Saving experiment data to file: {} ...'.format(filename))
        PlateScan.Save(filename)
        log_message(log_path, verbose, 'Save completed.')
    
        PlateScan.Close()
    
    if testing:
        truncated_experiment.close()

    # =============== Plate overview =============== #
    
    objective_position = '5x0.35NA'
    optovar_position = '1x'
    if not set_magnification(Zen, objective_position, optovar=optovar_position):
        log_message(log_path, verbose, 'Warning: Unable to set magnification.')
    else:
        log_message(log_path, verbose, 'Magnification set: {0} | {1}'.format(objective_position, optovar_position))

    experimentName = actual_experiments[1]
    if testing:
        truncated_experiment = TruncatedExperiment(Zen, experimentName)
        experimentName = truncated_experiment.truncated_experiment_name

    exp = Zen.Acquisition.Experiments.GetByName(experimentName)
    exp.SetActive()
    
    if skip_overview:
        log_message(log_path, verbose, 'Skip overview.')
    else:
        log_message(log_path, verbose, 'Running experiment: {}'.format(experimentName))
    
        PlateOverview = Zen.Acquisition.Execute(exp)
    
        log_message(log_path, verbose, 'Experiment completed.')
    
        barcode_overview = get_barcode(PlateOverview)
    
        try:
            if barcode != barcode_overview:
                log_message(log_path, verbose, 'Warning: barcodes for experiment and overview are not identical')
        except:
            pass
    
        filename = dataPath + barcode_overview + '-PO-unprocessed-' + timestamp + '.czi'
        log_message(log_path, verbose, 'Saving experiment data to file: {} ...'.format(filename))
        PlateOverview.Save(filename)
        log_message(log_path, verbose, 'Save completed.')
        
        PlateOverview.Close()

    if testing:
        truncated_experiment.close()
        
    # From PAA: Whatever is printed gets picked up by the robot.
    retstring = ZenLiveScan.GetCurrentError()
    if retstring=='Successful':
        print('Experiment Completed: {}'.format(experimentName))
        log_message(log_path, verbose, 'Macro completed successfully')
        log_message(log_path, verbose, '=======================================================')
    else:
        log_message(log_path, verbose, 'Macro completed with errors')
        log_message(log_path, verbose, '=======================================================')    

    # In manual exection, eject the sample.
    if not robot_execution:
        ZenLiveScan.EjectTray()
# From Zeiss boilerplate template (?).
else:
    experiment = ZenExperiment()
    experiment.Load(experimentName, ZenSettingDirectory.User)
    experiment.SetActive()
    outputexperiment1 = Zen.Acquisition.Execute(experiment)
    retstring = ZenLiveScan.GetCurrentError()
    if retstring == 'Successful':
        print('Experiment Completed: {}'.format(experiment.Name()))
