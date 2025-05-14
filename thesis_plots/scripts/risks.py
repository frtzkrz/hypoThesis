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

LNL = 'V'
filename = Path("thesis_plots/graph_results/risks/risks.hdf5")
USZ_COLORS = {
    "blue": '#005ea8',
    #"green": '#00afa5',
    "orange": '#f17900',
    #"red": '#ae0060',
    #"gray": '#c5d5db',
}
SCEN_DICT = {
    'N0': 'N0',
    'II': 'II involved',
    'III': 'III involved',
    'IV': 'IV involved',
    'II_III': 'II & III involved',
    'II_III_IV': 'II, III & IV involved',
}

if __name__ == "__main__":
    plt.style.use(Path(".mplstyle"))

    fig, axes = plt.subplot_mosaic(
        [['N0', 'II'],
         ['III', 'IV'],
         ['II_III', 'II_III_IV']],
        figsize=lyhist.get_size(width="full", ratio=1.5),
        sharey=True,
        layout="constrained",
        )

    with h5.File(filename, 'r') as f:
        # Print all root level object names (aka keys) 
        # these are the datasets in the file
        dataset = f[LNL]
        scenarios = ['N0', 'II', 'III', 'IV', 'II_III', 'II_III_IV']
        t_stages = ['early', 'late']
        
        for i, scen in enumerate(scenarios):  
            plots = []
            for stage in t_stages:
                color = USZ_COLORS["blue"] if stage == "early" else USZ_COLORS["orange"]
                dataset = f[f'{LNL}/{scen}/{stage}']
                plots.append(Histogram(
                    filename=filename,
                    dataname=f'{LNL}/{scen}/{stage}',
                    kwargs={
                        "color": color,
                        "label": rf"{SCEN_DICT[scen]}, {stage}: {100.*np.mean(dataset):.1f} $\pm$ {100.*np.std(dataset):.1f}%",
                    }
                ))
            draw(axes[scen], contents=plots, xlim=(.5, 9.5))
            axes[scen].legend()
            if i >= len(scenarios)-2: axes[scen].set_xlabel("Risk $R$ [%]")
    path = Path(f"thesis_plots/plots/risks")
    path.mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{path}/V.png", dpi=300)