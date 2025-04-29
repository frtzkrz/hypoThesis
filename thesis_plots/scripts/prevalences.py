"""
Plot the predicted prevalences against the observed ones for the four simple models
that only contain the ipsilateral LNLs II and III.
"""
from itertools import cycle
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.stats
import h5py

import lyscripts.plot.histograms as lyhist


# Specify models and respective data source locations
MODELS = {}
for tag in ["I_A_prevalences", "I_B_prevalences", "I_C_prevalences"]:
    MODELS[tag] = Path(f"thesis_plots/graph_results/prevalences/{tag}.hdf5")

modelnames = [name for name in MODELS.keys()]

filename = 'I_2'

# define USZ colors
COLORS = {
    "green": '#00afa5',
    "orange": '#f17900',
    #"blue": '#005ea8',
    #"red": '#ae0060',
    # "gray": '#c5d5db',
}
COLOR_CYCLE = cycle(COLORS.values())
BINS = np.linspace(35., 85., 200)
HIST_KWARGS = {
    "density": True,
    "bins": BINS,
    "histtype": "stepfilled",
    "alpha": 0.7,
}

SCENARIO_DICT = {
    "IIoverall": "II overall",
    "IInotI": "II w/o I",
}
scenario_names = [name for name in SCENARIO_DICT.keys()]

if __name__ == "__main__":
    plt.style.use(Path(".mplstyle"))

    fig, ax = plt.subplot_mosaic(
        [[f'{modelname}/early', f'{modelname}/late'] for modelname in MODELS.keys()],
        sharex=True, sharey=True,
        figsize=lyhist.get_size(width="full"),
    )

    for i, (modelname, filepath) in enumerate(MODELS.items()):
        ylabel = modelname.split("_")[1]
        with h5py.File(name=filepath, mode="r") as h5_file:
            for scenario in scenario_names:
                color = next(COLOR_CYCLE)
                for stage in ["early", "late"]:
                    axname = f"{modelname}/{stage}"
                    scenario_name = SCENARIO_DICT[scenario]

                    dataset = h5_file[f"{scenario}/{stage}"]
                    values = 100. * dataset[:]
                    a = dataset.attrs.get("num_match", np.nan)
                    n = dataset.attrs.get("num_total", np.nan)
                    posterior = sp.stats.beta.pdf(BINS / 100., a+1, n-a+1) / 100.
                    max_idx = np.argmax(posterior)
                    max_x = BINS[max_idx]
                    max_y = posterior[max_idx]

                    ax[axname].hist(
                        values,
                        label=scenario_name,
                        color=color,
                        **HIST_KWARGS,
                    )
                    ax[axname].plot(
                        BINS, posterior,
                        label=f"{int(a)} / {int(n)}",
                        color=color,
                    )

                    ax[axname].set_ylim(0., 0.25)
                    if stage == "early":
                        ax[axname].set_ylabel(ylabel)

    ax[f"{modelnames[0]}/early"].legend(fontsize=6.0, ncol=2)
    ax[f"{modelnames[0]}/late"].legend(fontsize=6.0, ncol=2)

    ax[f"{modelnames[-1]}/early"].set_xlim(left=BINS[0], right=BINS[-1])
    ax[f"{modelnames[-1]}/late"].set_xlim(left=BINS[0], right=BINS[-1])
    ax[f"{modelnames[-1]}/early"].set_xlabel("early T-category prevalences [%]")
    ax[f"{modelnames[-1]}/late"].set_xlabel("late T-category prevalences [%]")

    plt.savefig(f"thesis_plots/plots/prevalences/{filename}.png", dpi=300)
