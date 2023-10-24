# ------------------------------------------------------------------------------
#
    #    $$$$$$\   $$$$$$\ $$$$$$$$\ $$$$$$$$\ 
    #   $$  __$$\ $$  __$$\\__$$  __|$$  _____|
    #   $$ /  \__|$$ /  $$ |  $$ |   $$ |      
    #   $$ |$$$$\ $$$$$$$$ |  $$ |   $$$$$\    
    #   $$ |\_$$ |$$  __$$ |  $$ |   $$  __|   
    #   $$ |  $$ |$$ |  $$ |  $$ |   $$ |      
    #   \$$$$$$  |$$ |  $$ |  $$ |   $$$$$$$$\ 
    #    \______/ \__|  \__|  \__|   \________|
    #
# ------------------------------------------------------------------------------

import opengate as gate
from opengate import get_default_test_paths

paths = get_default_test_paths(__file__, "gate_test004_simulation_stats_actor")

# create the simulation
sim = gate.Simulation()

ui = sim.user_info
# check if ui is defined
# if locals().get('ui', None) is not None:
# ui.visu_type = "vrml"
# ui.visu = True
# ui.visu_filename = "geant4VisuFile.wrl"
# ui.visu_verbose = True
ui.g4_verbose = True
# ui.check_volumes_overlap = True
ui.number_of_threads = 15
ui.random_seed = 654923

sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option4"


paths = gate.get_default_test_paths(__file__, "gate_test004_simulation_stats_actor")

# add a material database
sim.add_material_database("./data/materials.db")

# Units
m = gate.g4_units("m")
cm = gate.g4_units("cm")
MeV = gate.g4_units("MeV")
mm = gate.g4_units("mm")
Bq = gate.g4_units("Bq")

# Change world size
world = sim.world
world.size = [1 * m, 1 * m, 1 * m]
world.material = "G4_AIR"

# detector in w2 (on top of world)
det = sim.add_volume("Box", "detector")
det.mother = "world"
det.material = "GOS"
det.size = [20 * mm, 20 * mm, 4 * mm]
det.translation = [0, 0, -200 * mm]
det.color = [1, 0, 0, 1]

# Add a pencil beam source
source = sim.add_source("GenericSource", "source")
source.energy.mono = 0.1 * MeV
source.particle = "gamma"
source.position.type = "box"
source.position.size = [0.01 * mm, 0.01 * mm, 0.01 * mm]
source.position.translation = [0, 0, 200 * mm]
source.n = 1e9 / ui.number_of_threads #number of particles
source.direction.type = "momentum"
source.direction.momentum = [0, 0, -1]

# add phsp actor detector 1 (overlap!)
dose = sim.add_actor("DoseActor", "edep")
dose.output = "out/gate_edep_test.mhd"
dose.mother = det.name
dose.size = [200,200,40]
dose.spacing = [0.1 * mm, 0.1 * mm, 0.1 * mm]
# dose.size = [20 * mm, 20 * mm, 4 * mm]
dose.hit_type = "random"
dose.uncertainty = True

# detector in w2 (on top of world)
det2 = sim.add_volume("Box", "detector2")
det2.mother = "world"
det2.material = "GOS"
det2.size = [20 * mm, 20 * mm, 4 * mm]
det2.translation = [0, 0, (-200-20.01) * mm]
det2.color = [1, 0, 0, 1]

# add phsp actor detector 1 (overlap!)
dose2 = sim.add_actor("DoseActor", "edep2")
dose2.output = "out/gate_edep2_test.mhd"
dose2.mother = det2.name
dose2.size = [200,200,40]
dose2.spacing = [0.1 * mm, 0.1 * mm, 0.1 * mm]
# dose.size = [20 * mm, 20 * mm, 4 * mm]
dose2.hit_type = "random"
dose2.uncertainty = True

sim.physics_manager.set_cut("detector2", "all", 0.01 * mm)
sim.physics_manager.set_cut("detector", "all", 0.01 * mm)

# add stat actor
stats = sim.add_actor("SimulationStatisticsActor", "Stats")
stats.track_types_flag = True

# print
print("Geometry trees: ")
print(sim.dump_tree_of_volumes())

# start simulation
output = sim.start()
