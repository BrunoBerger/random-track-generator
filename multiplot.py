from track_generator import TrackGenerator
from utils import Mode, SimType
import matplotlib.pyplot as plt
import numpy as np

def generate_track_plots(use_same_params=False):
    """
    Generate and plot 8 tracks, with each track optimally filling its subplot.
    """
    # Base parameters
    base_params = {
        'n_points': 20,
        'n_regions': 10,
        'min_bound': -50,
        'max_bound': 100,
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

    # Create figure with 4x2 subplots
    fig = plt.figure(figsize=(20, 10))
    
    # Generate and plot each track
    for idx, variation in enumerate(variations):
        # Create parameters for this track
        track_params = base_params.copy()
        track_params.update(variation)
        
        # Generate track
        track_gen = TrackGenerator(**track_params)
        track_gen.create_track()
        
        # Plot on corresponding subplot
        ax = fig.add_subplot(2, 4, idx + 1)
        ax.scatter(*track_gen.cones_left.T, color='b', s=1)
        ax.scatter(*track_gen.cones_right.T, color='y', s=1)
        
        # Find this track's bounds with a small margin
        x_min = min(track_gen.cones_left[:, 0].min(), track_gen.cones_right[:, 0].min())
        x_max = max(track_gen.cones_left[:, 0].max(), track_gen.cones_right[:, 0].max())
        y_min = min(track_gen.cones_left[:, 1].min(), track_gen.cones_right[:, 1].min())
        y_max = max(track_gen.cones_left[:, 1].max(), track_gen.cones_right[:, 1].max())
        
        # Add 5% margin
        x_margin = (x_max - x_min) * 0.05
        y_margin = (y_max - y_min) * 0.05
        
        # Set limits for this subplot
        ax.set_xlim(x_min - x_margin, x_max + x_margin)
        ax.set_ylim(y_min - y_margin, y_max + y_margin)
        
        # Remove axis labels and ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add title
        param_text = [f"n_pts={variation['n_points']}", 
                     f"n_reg={variation['n_regions']}"]
        ax.set_title(f"{idx+1}. {', '.join(param_text)}", fontsize=10)
        
        # Ensure square aspect ratio
        ax.set_aspect('equal')

    plt.tight_layout()
    plt.savefig("multiplot.png", dpi=300, bbox_inches='tight')
    plt.close()

# Example usage:
generate_track_plots(use_same_params=False)
