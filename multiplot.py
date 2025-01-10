from track_generator import TrackGenerator
from utils import Mode, SimType
import matplotlib.pyplot as plt
import numpy as np

def generate_track_plots(use_same_params=False):
    """
    Generate and plot 8 tracks, either with different variations or the same parameters.
    All subplots will have consistent sizes.
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
        variations = [base_params.copy() for _ in range(8)]

    # Create figure with 4x2 subplots with fixed size
    fig = plt.figure(figsize=(20, 10))
    
    # Generate all tracks first to determine common axis limits
    all_tracks = []
    for variation in variations:
        track_params = base_params.copy()
        track_params.update(variation)
        track_gen = TrackGenerator(**track_params)
        track_gen.create_track()
        all_tracks.append(track_gen)
    
    # Find global min and max for x and y coordinates
    x_min = min(min(track.cones_left[:, 0].min(), track.cones_right[:, 0].min()) for track in all_tracks)
    x_max = max(max(track.cones_left[:, 0].max(), track.cones_right[:, 0].max()) for track in all_tracks)
    y_min = min(min(track.cones_left[:, 1].min(), track.cones_right[:, 1].min()) for track in all_tracks)
    y_max = max(max(track.cones_left[:, 1].max(), track.cones_right[:, 1].max()) for track in all_tracks)
    
    # Ensure square aspect ratio for the limits
    total_range = max(x_max - x_min, y_max - y_min)
    x_center = (x_max + x_min) / 2
    y_center = (y_max + y_min) / 2
    
    # Plot each track
    for idx, track_gen in enumerate(all_tracks):
        ax = fig.add_subplot(2, 4, idx + 1)
        ax.scatter(*track_gen.cones_left.T, color='b', s=1)
        ax.scatter(*track_gen.cones_right.T, color='y', s=1)
        
        # Set consistent limits for all subplots
        ax.set_xlim(x_center - total_range/2, x_center + total_range/2)
        ax.set_ylim(y_center - total_range/2, y_center + total_range/2)
        
        # Remove axis labels and ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add title
        param_text = [f"n_pts={variations[idx]['n_points']}", 
                     f"n_reg={variations[idx]['n_regions']}", 
                     f"max={variations[idx]['max_bound']}"]
        ax.set_title(f"{idx+1}. {', '.join(param_text)}", fontsize=10)
        
        # Ensure square aspect ratio
        ax.set_aspect('equal')

    plt.tight_layout()
    plt.savefig("multiplot.png", dpi=300, bbox_inches='tight')
    plt.close()

# Example usage:
# For different variations:
generate_track_plots(use_same_params=False)

# For same parameters:
# generate_track_plots(use_same_params=True)