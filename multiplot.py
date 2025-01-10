from track_generator import TrackGenerator
from utils import Mode, SimType
import matplotlib.pyplot as plt
import numpy as np

def generate_track_plots(use_same_params=False):
    """
    Generate and plot 8 tracks, either with different variations or the same parameters.
    
    Args:
        use_same_params (bool): If True, generate 8 identical tracks with base parameters
    """
    # Base parameters
    base_params = {
        'n_points': 20,
        'n_regions': 10,
        'min_bound': 0,
        'max_bound': 250,
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
        # Different variations for each track
        variations = [
            # Tight technical track
            {
                'n_points': 25,
                'n_regions': 15,
                'max_bound': 150
            },
            # Wide flowing track
            {
                'n_points': 15,
                'n_regions': 8,
                'max_bound': 300
            },
            # Complex technical section
            {
                'n_points': 30,
                'n_regions': 12,
                'max_bound': 200
            },
            # Simple oval-like track
            {
                'n_points': 12,
                'n_regions': 6,
                'max_bound': 250
            },
            # Medium complexity, balanced track
            {
                'n_points': 20,
                'n_regions': 10,
                'max_bound': 225
            },
            # High-density short track
            {
                'n_points': 25,
                'n_regions': 12,
                'max_bound': 175
            },
            # Long track with varied sections
            {
                'n_points': 22,
                'n_regions': 14,
                'max_bound': 350
            },
            # Compact technical track
            {
                'n_points': 18,
                'n_regions': 12,
                'max_bound': 160
            }
        ]
    else:
        # Create 8 identical variations using base parameters
        variations = [base_params.copy() for _ in range(8)]

    # Create figure with 4x2 subplots
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()

    # Generate and plot each track
    for idx, variation in enumerate(variations):
        # Create parameters for this track
        track_params = base_params.copy()
        track_params.update(variation)
        
        # Generate track
        track_gen = TrackGenerator(**track_params)
        track_gen.create_track()
        
        # Plot on corresponding subplot
        ax = axes[idx]
        ax.scatter(*track_gen.cones_left.T, color='b', s=1)
        ax.scatter(*track_gen.cones_right.T, color='y', s=1)
        ax.set_aspect('equal')
        
        # Remove axis labels and ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add title
        param_text = [f"n_pts={variation['n_points']}", 
                     f"n_reg={variation['n_regions']}", 
                     f"max={variation['max_bound']}"]
        ax.set_title(f"{idx+1}. {', '.join(param_text)}", fontsize=10)

    plt.tight_layout()
    filename = "track_variations_same.png" if use_same_params else "track_variations_different.png"
    plt.savefig(filename)
    plt.close()

# Example usage:
# For different variations:
generate_track_plots(use_same_params=False)

# For same parameters:
generate_track_plots(use_same_params=True)