"""
Plot historgams over risks for involvement in LNL IV
given different diagnosis scenarios.
"""
from pathlib import Path
import matplotlib.pyplot as plt

import numpy as np
import lyscripts.plot.histograms as lyhist
import h5py as h5

from _utils import Histogram, Posterior, draw


filename = Path("thesis_plots/graph_results/risks/risks.hdf5")
USZ_COLORS = {
    "blue": '#005ea8',
    #"green": '#00afa5',
    "orange": '#f17900',
    #"red": '#ae0060',
    #"gray": '#c5d5db',
}


if __name__ == "__main__":
    plt.style.use(Path(".mplstyle"))

    fig, axes = plt.subplot_mosaic(
        [['N0', 'II']],
        figsize=lyhist.get_size(width="full", ratio=4),
        sharey=True,
        layout="constrained",
        )

    with h5.File(filename, 'r') as f:
        # Print all root level object names (aka keys) 
        # these are the datasets in the file
        dataset = f['III']
        scenarios = ['N0', 'II']
        t_stages = ['early', 'late']
        
        for scen in scenarios:  
            plots = []
            for stage in t_stages:
                color = USZ_COLORS["blue"] if stage == "early" else USZ_COLORS["orange"]
                dataset = f[f'III/{scen}/{stage}']
                plots.append(Histogram(
                    filename=filename,
                    dataname=f'III/{scen}/{stage}',
                    kwargs={
                        "color": color,
                        "label": rf"{stage}, {scen}: {100.*np.mean(dataset):.1f} $\pm$ {100.*np.std(dataset):.1f}%",
                    }
                ))
            draw(axes[scen], contents=plots, xlim=(0., 40.))
            axes[scen].legend()
            axes[scen].set_xlabel("Risk $R$ [%]")
    plt.savefig('thesis_plots/plots/risks/III.png', dpi=300)