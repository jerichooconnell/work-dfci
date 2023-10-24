
from detector_gui import Detector_GUI as det_gui
from detector_class import Detector as det
import spekpy_mod as sp

materials = ['Water','Cu','Gadolinium Oxysulfide','Si','Cu','Gadolinium Oxysulfide','Si','Cu','Gadolinium Oxysulfide','Si','Cu','Gadolinium Oxysulfide','Si']
densities = [None, None, None, None, None, None, None, None]
thicknesses = [10, 1, 0.436, 1, 1, 0.436, 1, 1, 0.436, 1, 1, 0.436, 1]
spectra = sp.Spek.load_from_file('25Xbeam_varian.txt',spectrum_delimeter=' ')

# Create the detector
detector = det()
detector.add_layers(materials, thicknesses, densities=densities)
# Initialize the gui.
gui = det_gui(spectra, detector=detector)