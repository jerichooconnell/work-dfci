import matplotlib.pyplot as plt
import numpy as np
import uproot

import opengate as gate
from opengate.tests import utility

# plot

data = uproot.open('/home/jericho/1-Workspace/opengate_ggems_comparison/scatter/out/ogate_1e07_100kVp_hits.root')['Hits']
data = (
    data.arrays(library="numpy")["edep"] * 1000
)  # MeV to KeV