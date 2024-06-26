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
