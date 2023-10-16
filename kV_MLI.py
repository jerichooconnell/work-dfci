# A file that specified the kilovoltage multilayer imager
# Detector GUI for fiddling with the parameters of the detector
# Jericho O'Connell 2023

from detector_gui import Detector_GUI as det_gui
from detector_class import Detector as det
import spekpy as sp


materials = ['Al', 'Ti', 'Water', 'Cesium Iodide',
                'Si', 'Cesium Iodide', 'Si']
densities = [None, None, 1, None, None, None, None, None]
thicknesses = [1, 1, 10, 0.6, 0.1, 0.8, 0.1]

spectra = sp.Spek(kvp=140, th=14)

# Create the detector
detector = det()
detector.add_layers(materials, thicknesses, densities=densities)
# Initialize the gui.
gui = det_gui(spectra, detector=detector)