# WARNING PLEASE READ FIRST
- **Reading of barcodes** seem to happen during loading of samples into the instrument. If the sample is already loaded, there is a possibility that the barcode won't appear in the metadata. It might happen if a sample is present inside the CD7 at the time of the instrument startup. This issue is not fully understood yet, and is to be investigated.
- **Importing user-written modules (*.py)** seem to be possible within an instrument macro. However, once the module is imported once, the module in its state at the time of first importation will remain in memory until ZenBlue is closed. In other words, if you run a macro that imports a user-written module, any subsequent changes to the user-written module aren't considered. I have found the following solution to this problem:
```python
import _cd7_functions
reload(_cd7_functions)
from _cd7_functions import set_magnification
```
reload(_cd7_functions)
- I do not know whether **water immersion** is applied using the `set_magnification` function. When testing this function, changing to the `'50x1.2NA'` lens was suspiciously fast (compared to the time it takes to immerse the lens usually).
# File structure
## CD7 functions
`_cd7_functions.py` contains functions related to the instrument. Currently, there's a single function `set_magnification(Zen, objective, optovar='1x')` used to change the instrument overall magnification: objective and optovar. This function relies on two hardcoded dictionaries consisting of string keys, which correspond to a human-readable magnification (e.g. `objective='5x0.35NA'` and `optovar='0.5x'`), and index values, which correspond to the index required by the Zen command.
## Sample functions
`_sample_functions.py` contains functions related to the sample. Currently, there's a function to extract a barcode from the metadata, and another function to create a timestamp. Although the metadata of each file contains a timestamp, having a common timestamp for the exepriment and its overview (which is considered another experiment) is desirable.
## RunExperiment
The single ZenBlue macro that needs to be executed by the user or the robot. Most of the parameters have been moved at the top of the file.
# What happens next
- The macro checks whether the current experiment is `SpiroC_Robot` or `SpiroC_Robot_Testing`, but never runs this experiment. Instead, it runs `SpiroC_V010_Robot` followed by `MS-PlateOverview-003` (or their truncated version). I think we could get rid of this "empty" experiment. This is mainly required for the robot, and I need to investigate how it can be changed. Alos, all our macros could be *.py but the robot requires a ```RunExperiment.czmac``` currently. It would be good to change everything for *.py in the future.
- The actual experiments have a "normal" version, which scans the whole sample, and a "truncated" version, which scans a small sub-region for debugging purposes. If we can programmatically decide to scan a sub-region from the "normal" experiment, we could get rid of those additional truncated experiments. This has been implemented, I had to do it by parsing the experiments as XML files and toggle a flag ```IsUsedForAcquisition```.
