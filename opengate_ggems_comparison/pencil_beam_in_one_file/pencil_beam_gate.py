import opengate as gate
import opengate.tests.utility as utility


paths = utility.get_default_test_paths(
    __file__, "gate_test004_simulation_stats_actor"
)

# create the simulation
sim = gate.Simulation()

# main options
ui = sim.user_info
ui.g4_verbose = True
ui.g4_verbose_level = 1
ui.visu = True
ui.visu_type = "vrml"
ui.visu_filename = "geant4VisuFile.wrl"
# ui.visu_verbose = True
ui.visu_verbose = True
ui.number_of_threads = 15
ui.random_engine = "MersenneTwister"
ui.random_seed = "auto"

# change physics
p = sim.get_physics_user_info()
p.physics_list_name = "G4EmStandardPhysics_option4"
p.enable_decay = True

m = gate.g4_units.m
um = gate.g4_units.um

# Set this really high to cut them all
sim.physics_manager.global_production_cuts.electron = 1 * m


sim.physics_manager.global_production_cuts.gamma = 10 * um
# cuts.electron = 10 * um
sim.physics_manager.global_production_cuts.positron = 10 * um
sim.physics_manager.global_production_cuts.proton = 10 * um

MeV = gate.g4_units.MeV
keV = gate.g4_units.keV

p.energy_range_min = 1 * keV
p.energy_range_max = 1 * MeV


# paths = gate.get_default_test_paths(__file__, "gate_test004_simulation_stats_actor")

# add a material database
sim.add_material_database("./data/materials.db")

# Units
m = gate.g4_units.m
cm = gate.g4_units.cm
MeV = gate.g4_units.MeV
mm = gate.g4_units.mm
Bq = gate.g4_units.Bq
deg = gate.g4_units.deg

# Change world size
world = sim.world
world.size = [1 * m, 1 * m, 1 * m]
world.material = "Vacuum"

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
source.n = 1e3 #/ ui.number_of_threads #number of particles
source.direction.theta = [0, 12.5 * deg]
source.direction.phi = [0, 360 * deg]
source.direction.type = "iso"
# source.direction.momentum = [0, 0, -1]

# add phsp actor detector 1 (overlap!)
# dose = sim.add_actor("DoseActor", "edep")
# dose.output = "out/gate_edep_test2.mhd"
# dose.mother = det.name
# dose.size = [200,200,40]
# dose.spacing = [0.1 * mm, 0.1 * mm, 0.1 * mm]
# # dose.size = [20 * mm, 20 * mm, 4 * mm]
# dose.hit_type = "random"
# dose.uncertainty = True

# dose = sim.add_actor("DoseActor", "hits")
# dose.output = "out/gate_edep_test2.mhd"
# dose.mother = det.name
# dose.size = [200,200,40]
# dose.spacing = [0.1 * mm, 0.1 * mm, 0.1 * mm]
# # dose.size = [20 * mm, 20 * mm, 4 * mm]
# dose.hit_type = "random"
# dose.uncertainty = True
# dose = sim.add_actor('DoseActor', 'Hits')
dose = sim.add_actor("DigitizerHitsCollectionActor", "Hits")
# dose = sim.add_actor('DoseActor', 'Hits')
dose.mother = det.name
dose.output = 'test_hits.root'
dose.attributes = ['TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
                'CreatorProcess', 'VolumeName', 'TrackID']
# dose.mother = ['crystal1', 'crystal2']
# dose.output = 'test_hits.root'
# dose.attributes = ['TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
#                 'CreatorProcess', 'VolumeName', 'TrackID']
dose.output = "out/gate_edep_test2.mhd"
dose.mother = det.name
dose.size = [200,200,40]
dose.spacing = [0.1 * mm, 0.1 * mm, 0.1 * mm]
dose.size = [20 * mm, 20 * mm, 4 * mm]
dose.hit_type = "random"
dose.uncertainty = True

# detector in w2 (on top of world)
det2 = sim.add_volume("Box", "detector2")
det2.mother = "world"
det2.material = "GOS"
det2.size = [20 * mm, 20 * mm, 4 * mm]
det2.translation = [0, 0, (-200-4.01) * mm]
det2.color = [1, 0, 0, 1]

# add phsp actor detector 1 (overlap!)
dose2 = sim.add_actor("DoseActor", "edep2")
dose2.output = "out/gate_edep2_test2.mhd"
dose2.mother = det2.name
dose2.size = [200,200,40]
dose2.spacing = [0.1 * mm, 0.1 * mm, 0.1 * mm]
dose2.hit_type = "random"
dose2.uncertainty = True

# sim.physics_manager.set_cut("detector2", "all", 0.01 * mm)
# sim.physics_manager.set_cut("detector", "all", 0.01 * mm)

# add stat actor
stats = sim.add_actor("SimulationStatisticsActor", "Stats")
stats.track_types_flag = True

# print
print("Geometry trees: ")
print(sim.dump_tree_of_volumes())

# start simulation
output = sim.start()
