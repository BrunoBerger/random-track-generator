from track_generator import TrackGenerator
from utils import Mode, SimType
import matplotlib.pyplot as plt
import numpy as np

def generate_track_plots(num_plots=8, use_same_params=False, file_type="pdf"):
    """
    Generate track multiplots for the thesis.

    Args:
        num_plots (int): Number of plots to generate (4 or 8).
        use_same_params (bool): Whether to use the same parameters for all tracks.
    """
    if num_plots not in [2, 4, 6, 8]:
        raise ValueError("num_plots should be either 4, 6, 8.")
    plots_per_row = int(num_plots / 2)
    
    # Base parameters
    base_params = {
        'n_points': 20,
        'n_regions': 10,
        'min_bound': -50,
        'max_bound': 80,
        'mode': Mode.RANDOM, # EXPAND, EXTEND, RANDOM
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
            {'n_points': 25,'n_regions': 15,}, # Tight technical track
            {'n_points': 15,'n_regions': 8,}, # Wide flowing track
            {'n_points': 30,'n_regions': 12,}, # Complex technical section
            {'n_points': 12,'n_regions': 6,}, # Simple oval-like track
            {'n_points': 20,'n_regions': 10,}, # Medium complexity, balanced track
            {'n_points': 25,'n_regions': 12,}, # High-density track
            {'n_points': 22,'n_regions': 14,}, # Long track with varied sections
            {'n_points': 18,'n_regions': 12,} # Compact technical track
        ][:num_plots]
    else:
        variations = [base_params.copy() for _ in range(num_plots)]
    
    # Calculate number of rows
    num_rows = -(-num_plots // plots_per_row)  # Ceiling division

    # Create figure with appropriate layout
    fig = plt.figure(figsize=(plots_per_row * 5, num_rows * 5))
    gs = fig.add_gridspec(num_rows, plots_per_row, width_ratios=[1] * plots_per_row, height_ratios=[1] * num_rows)
    axes = [fig.add_subplot(gs[i]) for i in range(num_plots)]

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
        
        # Find track bounds and center plot
        x_min = min(track_gen.cones_left[:, 0].min(), track_gen.cones_right[:, 0].min())
        x_max = max(track_gen.cones_left[:, 0].max(), track_gen.cones_right[:, 0].max())
        y_min = min(track_gen.cones_left[:, 1].min(), track_gen.cones_right[:, 1].min())
        y_max = max(track_gen.cones_left[:, 1].max(), track_gen.cones_right[:, 1].max())
        x_center, y_center = (x_max + x_min) / 2, (y_max + y_min) / 2
        plot_range = max(x_max - x_min, y_max - y_min) * 1.1
        
        ax.set_xlim(x_center - plot_range/2, x_center + plot_range/2)
        ax.set_ylim(y_center - plot_range/2, y_center + plot_range/2)
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"{idx+1}: {variation['n_points']} pts, {variation['n_regions']} regs", fontsize=10)
        ax.set_aspect('equal')

    # Hide unused subplots
    for i in range(num_plots, num_rows * plots_per_row):
        fig.add_subplot(gs[i]).axis("off")

    plt.tight_layout()
    # plt.savefig(f"track_gen_multiplot.{file_type}", dpi=300, bbox_inches='tight')
    plt.savefig(f"track_gen_multiplot.pdf", dpi=300, bbox_inches='tight')
    plt.savefig(f"track_gen_multiplot.png", dpi=300, bbox_inches='tight')
    plt.close()

generate_track_plots(num_plots=6, use_same_params=False, file_type="png")