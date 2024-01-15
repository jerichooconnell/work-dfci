import numpy as np
from ggems import *
import matplotlib.pyplot as plt
import argparse

# Some variables to define the asg

period = 10*0.167  # mm
detector_width = 397  # mm
detector_height = 298  # mm from the varex 4030cb datasheet
y_dist = 1500  # mm focus from Varian
lamella_height = 1.310  # mm
lamella_width = 0.036  # mm

# Define the asg values
xvals = np.linspace(-detector_width/2, detector_width /
                    2, int(detector_width/period))
yvals = np.ones_like(xvals)

# Define the angles
theta = np.rad2deg(np.arctan(xvals/y_dist))

# Define the point where the angles enter the asg
# This is the opposite distance tan(theta) is opposite over adjacent
# So the opposite distance is the y value and the adjacent distance is the y value divided by tan(theta)
ray_x0 = y_dist * np.tan(np.deg2rad(theta))


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
                    action='store_false', help='Disable OpenGL')
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
                    type=int, default=int(1e7), help="Number of particles")
parser.add_argument('-s', '--seed', required=False, type=int,
                    default=777, help="Seed of pseudo generator number")

args = parser.parse_args()

# ------------------------------------------------------------------------------
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
    opengl_manager.set_world_size(3.0, 3.0, 3.0, 'm')
    opengl_manager.set_image_output('data/axis')
    opengl_manager.set_displayed_particles(number_of_displayed_particles)
    opengl_manager.set_particle_color('gamma', 152, 251, 152)
    # opengl_manager.set_particle_color('gamma', color_name='red') # Using registered color
    opengl_manager.initialize()

# ------------------------------------------------------------------------------
# STEP 3: Choosing an OpenCL device
opencl_manager.set_device_to_activate(device)

# STEP 6: Physics
processes_manager.add_process('Compton', 'gamma', 'all')
processes_manager.add_process('Photoelectric', 'gamma', 'all')
processes_manager.add_process('Rayleigh', 'gamma', 'all')


# ------------------------------------------------------------------------------
# STEP 4: Setting GGEMS materials
materials_database_manager.set_materials('data/materials.txt')

# ------------------------------------------------------------------------------
# # STEP 5: Phantoms and systems

# phantom = GGEMSVoxelizedPhantom(f'phantom')
# phantom.set_phantom('data/test2.mhd', 'data/range_test.txt')
# phantom.set_position(0, 0, 0, 'mm')
# phantom.set_rotation(0.0, 0.0, 0, 'rad')
# phantom.set_visible(True)

cbct_detector = GGEMSCTSystem('custom')
cbct_detector.set_ct_type('flat')
cbct_detector.set_number_of_modules(1, 1)
cbct_detector.set_number_of_detection_elements(500, 500, 1)  # Might be a sham
cbct_detector.set_size_of_detection_elements(0.8, 0.8, 3, 'mm')
cbct_detector.set_material('GOS')
# Center of inside detector, adding half of detector (= SDD surface + 10.0/2 mm half of depth)
cbct_detector.set_source_detector_distance(400., 'mm')
cbct_detector.set_source_isocenter_distance(200., 'mm')
# cbct_detector.set_rotation(0.0, 0.0, 0.0, 'deg')
# cbct_detector.set_global_system_position(0.0, 0.0, 0.0, 'mm')
cbct_detector.set_threshold(10, 'keV')
cbct_detector.save('out/ggems_edep')
cbct_detector.store_scatter(True)
cbct_detector.set_visible(True)

# ct_detector = GGEMSCTSystem('Stellar')
# ct_detector.set_ct_type('curved')
# ct_detector.set_number_of_modules(1, 46)
# ct_detector.set_number_of_detection_elements(64, 16, 1)
# ct_detector.set_size_of_detection_elements(0.6, 0.6, 0.6, 'mm')
# ct_detector.set_material('GOS')
# ct_detector.set_source_detector_distance(1085.6, 'mm')
# ct_detector.set_source_isocenter_distance(595.0, 'mm')
# ct_detector.set_rotation(0.0, 0.0, 0.0, 'deg')
# ct_detector.set_threshold(10.0, 'keV')
# ct_detector.save('data/projection')
# ct_detector.store_scatter(True)

# ct_detector = GGEMSCTSystem('Stellar')
# ct_detector.set_ct_type('curved')
# ct_detector.set_number_of_modules(1, 46)
# ct_detector.set_number_of_detection_elements(64, 16, 1)
# ct_detector.set_size_of_detection_elements(0.6, 0.6, 0.6, 'mm')
# ct_detector.set_material('GOS')
# ct_detector.set_source_detector_distance(200, 'mm')
# ct_detector.set_source_isocenter_distance(100, 'mm')
# ct_detector.set_rotation(0.0, 0.0, 0.0, 'deg')
# ct_detector.set_threshold(10.0, 'keV')
# ct_detector.save('data/projection')
# ct_detector.set_visible(True)
# ct_detector.store_scatter(True)

# ------------------------------------------------------------------------------

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
point_source.set_beam_aperture(8, 'deg')
point_source.set_focal_spot_size(0.01, 0.01, 0.01, 'mm')
point_source.set_monoenergy(50, 'keV')
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
