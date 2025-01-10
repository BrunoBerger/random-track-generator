from track_generator import TrackGenerator
from utils import Mode, SimType
import matplotlib.pyplot as plt
import numpy as np

def generate_track_plots(use_same_params=False):
    """
    Generate and plot 8 tracks with consistent subplot sizes and linspace variations.
    """
    # Base parameters
    base_params = {
        'n_points': 20,
        'n_regions': 10,
        'min_bound': -50,
        'max_bound': 80,
        'mode': Mode.EXTEND,
        'sim_type': SimType.FSDS,
        'plot_track': False,
        'visualise_voronoi': False,
        'create_output_file': False,
        'output_location': '/',
        'lat_offset': 51.197682,
        'lon_offset': 5.323411
    }

    if not use_same_params:
        variations = [
            # Tight technical track
            {
                'n_points': 25,
                'n_regions': 15,
            },
            # Wide flowing track
            {
                'n_points': 15,
                'n_regions': 8,
            },
            # Complex technical section
            {
                'n_points': 30,
                'n_regions': 12,
            },
            # Simple oval-like track
            {
                'n_points': 12,
                'n_regions': 6,
            },
            # Medium complexity, balanced track
            {
                'n_points': 20,
                'n_regions': 10,
            },
            # High-density track
            {
                'n_points': 25,
                'n_regions': 12,
            },
            # Long track with varied sections
            {
                'n_points': 22,
                'n_regions': 14,
            },
            # Compact technical track
            {
                'n_points': 18,
                'n_regions': 12,
            }
        ]
    else:
        variations = [base_params.copy() for _ in range(8)]

    # Create figure with 4x2 subplots with fixed subplot sizes
    fig = plt.figure(figsize=(20, 10))
    
    # Create GridSpec to ensure all subplots are exactly the same size
    gs = fig.add_gridspec(2, 4, width_ratios=[1, 1, 1, 1], height_ratios=[1, 1])
    axes = [fig.add_subplot(gs[i]) for i in range(8)]

    # Generate and plot each track
    for idx, (variation, ax) in enumerate(zip(variations, axes)):
        # Create parameters for this track
        track_params = base_params.copy()
        track_params.update(variation)
        
        # Generate track
        track_gen = TrackGenerator(**track_params)
        track_gen.create_track()
        
        # Plot the track
        ax.scatter(*track_gen.cones_left.T, color='b', s=4)
        ax.scatter(*track_gen.cones_right.T, color='#f7b307', s=4)
        
        # Find this track's bounds
        x_min = min(track_gen.cones_left[:, 0].min(), track_gen.cones_right[:, 0].min())
        x_max = max(track_gen.cones_left[:, 0].max(), track_gen.cones_right[:, 0].max())
        y_min = min(track_gen.cones_left[:, 1].min(), track_gen.cones_right[:, 1].min())
        y_max = max(track_gen.cones_left[:, 1].max(), track_gen.cones_right[:, 1].max())
        
        # Calculate center and range of the track
        x_center = (x_max + x_min) / 2
        y_center = (y_max + y_min) / 2
        x_range = x_max - x_min
        y_range = y_max - y_min
        
        # Use the larger range to ensure the track fits while maintaining aspect ratio
        plot_range = max(x_range, y_range) * 1.1  # Add 10% margin
        
        # Set limits centered on the track
        ax.set_xlim(x_center - plot_range/2, x_center + plot_range/2)
        ax.set_ylim(y_center - plot_range/2, y_center + plot_range/2)
        
        # Remove axis labels and ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add title
        param_text = [f"{variation['n_points']} points", 
                     f"{variation['n_regions']} regions"]
        ax.set_title(f"{idx+1}. | {', '.join(param_text)}", fontsize=10)
        
        # Ensure square aspect ratio
        ax.set_aspect('equal')

    plt.tight_layout()
    plt.savefig("track_gen_multiplot.pdf", dpi=300, bbox_inches='tight')
    plt.close()

# Generate different variations:
generate_track_plots(use_same_params=False)