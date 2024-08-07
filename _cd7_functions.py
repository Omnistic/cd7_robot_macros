﻿import os
import xml.etree.ElementTree as ET

# Note: I'm not sure if immersion is applied when activating
# the 50x objective in this manner (to be tested).

OBJECTIVES = {
    '5x0.35NA': 2,
    '20x0.7NA': 1,
    '20x0.95NA': 3,
    '50x1.2NA': 4
    }

OPTOVARS = {
    '0.5x': 3,
    '1x': 2,
    '2x': 1
    }

def set_magnification(Zen, objective, optovar='1x'):
    ###
    #
    # Set CD7 overall magnification, i.e. objective
    # and optovar magnifications.
    #
    # Parameters
    # ==========
    # Zen: Zeiss.Micro.LM.Scripting.Research.ZenBlueScriptingWrapperServiceLM
    #   An object from the main script that probably represents the CD7.
    #
    # objective: string
    #   The objective magnification.
    #
    # optovar: string
    #   The optovar magnification. Default to 1x.
    #
    # Returns
    # =======
    # boolean
    #   True if the magnification could be set. False otherwise.
    #
    ###

    try:
        if Zen.Devices.ObjectiveChanger.TargetPosition != OBJECTIVES[objective]:
            Zen.Devices.ObjectiveChanger.TargetPosition = OBJECTIVES[objective]
            Zen.Devices.ObjectiveChanger.Apply()

        if Zen.Devices.Optovar.TargetPosition != OPTOVARS[optovar]:
            Zen.Devices.Optovar.TargetPosition = OPTOVARS[optovar]
            Zen.Devices.Optovar.Apply()

        return True
    except:
        return False

def get_experiment_folder(Zen):
    active_experiment = Zen.Acquisition.Experiments.ActiveExperiment.FileName
    
    return active_experiment[:active_experiment.rfind('\\')+1]

def set_sample_tab(ZenLiveScan, sample_tab_dict):
    conf = ZenLiveScan.GetConfiguration()

    if 'Sample Carrier' in sample_tab_dict:
        conf.SampleCarrierTypeTemplate = sample_tab_dict['Sample Carrier']

    if 'Measure Bottom Thickness' in sample_tab_dict:
        conf.MeasureBottomThickness = sample_tab_dict['Measure Bottom Thickness']

        if conf.MeasureBottomThickness and 'Determine Bottom Material' in sample_tab_dict:
            conf.DetermineBottonMaterial = sample_tab_dict['Determine Bottom Material']

    if 'Sample Carrier Detection' in sample_tab_dict:
        conf.SampleCarrierDetection = sample_tab_dict['Sample Carrier Detection']

    if 'Sample Carrier Overview' in sample_tab_dict:
        conf.CreateCarrierOverview = sample_tab_dict['Sample Carrier Overview']

    if 'Read Barcodes' in sample_tab_dict:
        conf.ReadBarcodes = True
        if sample_tab_dict['Read Barcodes'] == 'none':
            conf.ReadBarcodes = False
            conf.UseLeftBarcode = False
            conf.UseRightBarcode = False
        if sample_tab_dict['Read Barcodes'] == 'left':
            conf.UseLeftBarcode = True
            conf.UseRightBarcode = False
        elif sample_tab_dict['Read Barcodes'] == 'right':
            conf.UseLeftBarcode = False
            conf.UseRightBarcode = True
        elif sample_tab_dict['Read Barcodes'] == 'both':
            conf.UseLeftBarcode = True
            conf.UseRightBarcode = True

    if 'Automatic Sample Carrier Calibration' in sample_tab_dict:
        conf.AutomaticSampleCarrierCalibration = sample_tab_dict['Automatic Sample Carrier Calibration']

    ZenLiveScan.SetConfiguration(conf)

class TruncatedExperiment:
    def __init__(self, Zen, experiment_template):
        self.Zen = Zen
        self.experiment_template = experiment_template
        self.get_experiment_folder()
        self.truncated_experiment_name = experiment_template+'_truncated'
        self.truncated_experiment_path = os.path.join(self.experiment_folder, self.truncated_experiment_name+'.czexp')
        self.get_experiment_root(experiment_template)
        self.get_tile_region_arrays()
        self.get_tile_regions()
        self.truncate_experiment()

    def get_experiment_folder(self):
        active_experiment = self.Zen.Acquisition.Experiments.ActiveExperiment.FileName
        self.experiment_folder = active_experiment[:active_experiment.rfind('\\')+1]

    def get_experiment_root(self, experiment_template):
        self.experiment_tree = ET.parse(self.experiment_folder + self.experiment_template + '.czexp')
        self.experiment_root = self.experiment_tree.getroot()

    def get_tile_region_arrays(self):
        self.tile_region_arrays = self.experiment_root.find('./ExperimentBlocks/AcquisitionBlock/SubDimensionSetups/RegionsSetup/SampleHolder/SingleTileRegionArrays')

    def get_tile_regions(self):
        self.tile_regions = self.experiment_root.find('./ExperimentBlocks/AcquisitionBlock/SubDimensionSetups/RegionsSetup/SampleHolder/TileRegions')

    def truncate_experiment(self):
        ii = -1
        for tile_region_array in self.tile_region_arrays:
            ii += 1
            if ii < 2:
                tile_region_array.find('./IsUsedForAcquisition').text = 'true'
                continue
            tile_region_array.find('./IsUsedForAcquisition').text = 'false'
        
        ii = -1
        for tile_region in self.tile_regions:
            ii += 1
            if ii < 2:
                tile_region.find('./IsUsedForAcquisition').text = 'true'
                continue
            tile_region.find('./IsUsedForAcquisition').text = 'false'

        self.experiment_tree.write(self.truncated_experiment_path)

    def close(self):
        if os.path.exists(self.truncated_experiment_path):
            os.remove(self.truncated_experiment_path)
