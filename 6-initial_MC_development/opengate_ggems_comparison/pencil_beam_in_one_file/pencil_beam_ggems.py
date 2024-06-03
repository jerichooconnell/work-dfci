# ------------------------------------------------------------------------------
#
#    $$$$$$\   $$$$$$\  $$$$$$$$\ $$\      $$\  $$$$$$\
#   $$  __$$\ $$  __$$\ $$  _____|$$$\    $$$ |$$  __$$\
#   $$ /  \__|$$ /  \__|$$ |      $$$$\  $$$$ |$$ /  \__|
#   $$ |$$$$\ $$ |$$$$\ $$$$$\    $$\$$\$$ $$ |\$$$$$$\
#   $$ |\_$$ |$$ |\_$$ |$$  __|   $$ \$$$  $$ | \____$$\
#   $$ |  $$ |$$ |  $$ |$$ |      $$ |\$  /$$ |$$\   $$ |
#   \$$$$$$  |\$$$$$$  |$$$$$$$$\ $$ | \_/ $$ |\$$$$$$  |
#    \______/  \______/ \________|\__|     \__| \______/
#
# ------------------------------------------------------------------------------

# Import the necessary GGEMS modules
import argparse
from ggems import *

# ------------------------------------------------------------------------------
# Read arguments
parser = argparse.ArgumentParser(
    prog='visualization.py',
    description='''-->> 6 - OpenGL Visualization Example <<--''',
    epilog='''''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-v', '--verbose', required=False,
                    type=int, default=0, help='Set level of verbosity')
parser.add_argument('-e', '--nogl', required=False,
                    action='store_true', help='Disable OpenGL')
parser.add_argument('-w', '--wdims', required=False,
                    default=[800, 800], type=int, nargs=2, help='OpenGL window dimensions')
parser.add_argument('-m', '--msaa', required=False, type=int,
                    default=8, help='MSAA factor (1x, 2x, 4x or 8x)')
parser.add_argument('-a', '--axis', required=False,
                    action='store_true', help='Drawing axis in OpenGL window')
parser.add_argument('-p', '--nparticlesgl', required=False, type=int, default=256,
                    help='Number of displayed primary particles on OpenGL window (max: 65536)')
parser.add_argument('-b', '--drawgeom', required=False,
                    action='store_true', help='Draw geometry only on OpenGL window')
parser.add_argument('-c', '--wcolor', required=False, type=str,
                    default='black', help='Background color of OpenGL window')
parser.add_argument('-d', '--device', required=False, type=str,
                    default='0', help="OpenCL device running visualization")
parser.add_argument('-n', '--nparticles', required=False,
                    type=int, default=int(1e8), help="Number of particles")
parser.add_argument('-s', '--seed', required=False, type=int,
                    default=777, help="Seed of pseudo generator number")

args = parser.parse_args()

# Getting arguments
verbosity_level = args.verbose
seed = args.seed
device = args.device
number_of_particles = args.nparticles
number_of_displayed_particles = args.nparticlesgl
is_axis = args.axis
msaa = args.msaa
window_color = args.wcolor
window_dims = args.wdims
is_draw_geom = args.drawgeom
is_gl = args.nogl
# ------------------------------------------------------------------------------
# STEP 0: Level of verbosity during computation
GGEMSVerbosity(0)

# ------------------------------------------------------------------------------
# STEP 1: Calling C++ singleton
opencl_manager = GGEMSOpenCLManager()
materials_database_manager = GGEMSMaterialsDatabaseManager()
processes_manager = GGEMSProcessesManager()
range_cuts_manager = GGEMSRangeCutsManager()
volume_creator_manager = GGEMSVolumeCreatorManager()

# ------------------------------------------------------------------------------
# STEP 2: Params for visualization
if is_gl:
    opengl_manager = GGEMSOpenGLManager()
    opengl_manager.set_window_dimensions(window_dims[0], window_dims[1])
    opengl_manager.set_msaa(msaa)
    opengl_manager.set_background_color(window_color)
    opengl_manager.set_draw_axis(is_axis)
    opengl_manager.set_world_size(1.0, 1.0, 1.0, 'm')
    opengl_manager.set_image_output('data/axis')
    opengl_manager.set_displayed_particles(number_of_displayed_particles)
    opengl_manager.set_particle_color('gamma', 152, 251, 152)
    # opengl_manager.set_particle_color('gamma', color_name='red') # Using registered color
    opengl_manager.initialize()

# ------------------------------------------------------------------------------
# STEP 3: Choosing an OpenCL device
opencl_manager.set_device_to_activate(device)

# ------------------------------------------------------------------------------
# STEP 4: Setting GGEMS materials
materials_database_manager.set_materials('data/materials.txt')

# ------------------------------------------------------------------------------
# STEP 5: Phantoms and systems
volume_creator_manager = GGEMSVolumeCreatorManager()
volume_creator_manager.set_dimensions(40, 200, 200)
volume_creator_manager.set_element_sizes(0.1, 0.1, 1, "mm")
volume_creator_manager.set_output('data/volume.mhd')
volume_creator_manager.set_range_output('data/range_volume.txt')
volume_creator_manager.set_material('GOS')
volume_creator_manager.set_data_type('MET_INT')
volume_creator_manager.initialize()
volume_creator_manager.write()

# STEP 5: Phantoms and systems
volume_creator_manager = GGEMSVolumeCreatorManager()
volume_creator_manager.set_dimensions(40, 200, 200)
volume_creator_manager.set_element_sizes(0.1, 0.1, 1, "mm")
volume_creator_manager.set_output('data/volume2.mhd')
volume_creator_manager.set_range_output('data/range_volume2.txt')
volume_creator_manager.set_material('GOS')
volume_creator_manager.set_data_type('MET_INT')
volume_creator_manager.initialize()
volume_creator_manager.write()

# Loading phantom
phantom = GGEMSVoxelizedPhantom('phantom')
phantom.set_phantom('data/volume.mhd', 'data/range_volume.txt')
phantom.set_rotation(0.0, 0.0, 0.0, 'deg')
phantom.set_position(0.0, 0.0, 0, 'mm')
phantom.set_visible(True)

phantom2 = GGEMSVoxelizedPhantom('phantom2')
phantom2.set_phantom('data/volume2.mhd', 'data/range_volume2.txt')
phantom2.set_rotation(0.0, 0.0, 0.0, 'deg')
phantom2.set_position(300.01, 0.0, 0, 'mm')
phantom2.set_visible(True)

dosimetry = GGEMSDosimetryCalculator()
dosimetry.attach_to_navigator('phantom')
dosimetry.set_output_basename('out2/ggems_dosimetry_no_tle')
dosimetry.water_reference(False)
dosimetry.set_tle(False)
dosimetry.set_dosel_size(0.1, 0.1, 1, 'mm')
dosimetry.uncertainty(True)
dosimetry.edep(True)
dosimetry.hit(False)
dosimetry.edep_squared(False)

dosimetry2 = GGEMSDosimetryCalculator()
dosimetry2.attach_to_navigator('phantom2')
dosimetry2.set_output_basename('out2/ggems_dosimetry_no_tle2')
dosimetry2.water_reference(False)
dosimetry2.set_tle(False)
dosimetry2.set_dosel_size(0.1, 0.1, 1, 'mm')
dosimetry2.uncertainty(True)
dosimetry2.edep(True)
dosimetry2.hit(False)
dosimetry2.edep_squared(False)

# cbct_detector = GGEMSCTSystem('custom')
# cbct_detector.set_ct_type('flat')
# cbct_detector.set_number_of_modules(1, 1)
# cbct_detector.set_number_of_detection_elements(200, 200, 40) # Might be a sham
# cbct_detector.set_size_of_detection_elements(0.1, 0.1, 0.1, 'mm')
# cbct_detector.set_material('GOS')
# cbct_detector.set_source_detector_distance(400., 'mm') # Center of inside detector, adding half of detector (= SDD surface + 10.0/2 mm half of depth)
# cbct_detector.set_source_isocenter_distance(200., 'mm')
# cbct_detector.set_rotation(0.0, 0.0, 0.0, 'deg')
# cbct_detector.set_global_system_position(0.0, 0.0, 0.0, 'mm')
# cbct_detector.set_threshold(0.1, 'keV')
# cbct_detector.save('out/ggems_edep')
# cbct_detector.store_scatter(True)
# cbct_detector.set_visible(True)
# cbct_detector.set_material_color('GOS', 255, 0, 0) # Custom color using RGB

# ------------------------------------------------------------------------------
# STEP 6: Physics
processes_manager.add_process('Compton', 'gamma', 'all')
processes_manager.add_process('Photoelectric', 'gamma', 'all')
processes_manager.add_process('Rayleigh', 'gamma', 'all')

# Optional options, the following are by default
processes_manager.set_cross_section_table_number_of_bins(220)
processes_manager.set_cross_section_table_energy_min(1.0, 'keV')
processes_manager.set_cross_section_table_energy_max(1.0, 'MeV')

# ------------------------------------------------------------------------------
# STEP 7: Cuts, by default but are 1 um
range_cuts_manager.set_cut('gamma', 0.01, 'mm', 'all')
range_cuts_manager.set_cut('e-', 0.01, 'mm', 'all')

# ------------------------------------------------------------------------------
# STEP 8: Source
point_source = GGEMSXRaySource('point_source')
point_source.set_source_particle_type('gamma')
point_source.set_number_of_particles(number_of_particles)
point_source.set_position(-200.0, 0.0, 0.0, 'mm')
point_source.set_rotation(0.0, 0.0, 0.0, 'deg')
point_source.set_beam_aperture(0.001, 'deg')
point_source.set_focal_spot_size(0.01, 0.01, 0.01, 'mm')
point_source.set_monoenergy(100, 'keV')
# point_source.set_polyenergy('data/spectrum_120kVp_2mmAl.dat')

# ------------------------------------------------------------------------------
# STEP 9: GGEMS simulation
ggems = GGEMS()
ggems.opencl_verbose(True)
ggems.material_database_verbose(False)
ggems.navigator_verbose(False)
ggems.source_verbose(True)
ggems.memory_verbose(True)
ggems.process_verbose(True)
ggems.range_cuts_verbose(True)
ggems.random_verbose(True)
ggems.profiling_verbose(True)
ggems.tracking_verbose(False, 0)

# Initializing the GGEMS simulation
ggems.initialize(seed)

if is_draw_geom and is_gl:  # Draw only geometry and do not run GGEMS
    opengl_manager.display()
else:  # Running GGEMS and draw particles
    ggems.run()


# ------------------------------------------------------------------------------
# STEP 10: Exit safely
dosimetry.delete()
ggems.delete()
clean_safely()
exit()
