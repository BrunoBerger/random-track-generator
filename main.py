from track_generator import TrackGenerator
from utils import Mode, SimType

# Input parameters
n_points = 20
n_regions = 10
min_bound = 0
max_bound = 250
mode = Mode.EXTEND
sim_type = SimType.FSDS

# Output options
plot_track = False
visualise_voronoi = False
create_output_file = True
output_location = '/'
print("TEST")

# Generate track
track_gen = TrackGenerator(n_points, n_regions, min_bound, max_bound, mode, plot_track, visualise_voronoi, create_output_file, output_location, lat_offset=51.197682, lon_offset=5.323411, sim_type=sim_type)
track_gen.create_track()
track_gen.export_plot()
