import numpy as np
import matplotlib.pyplot as plt
import awkward as ak

def draw_hist(ax, hist, bins, label, color=None):
    if color is None:
        ax.hist(
            hist,
            bins=bins,
            histtype="step",
            color=color,
            label=label,
        )
    else:
        ax.hist(
            hist,
            bins=bins,
            histtype="step",
            color=color,
            label=label,
        )
        
    ax.legend(fontsize = 14)
    ax.tick_params(axis='both', labelsize=14)
    return ax

def draw_hist2d(ax, x, y, bins, vmin=None, vmax=None, cmap="magma", log=False):
    x = ak.to_numpy(x)
    y = ak.to_numpy(y)
    
    h = ax.hist2d(
        x, y,
        bins=bins,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        norm=LogNorm() if log else None,
    )
        
    # ax.legend(fontsize = 14)
    ax.tick_params(axis='both', labelsize=14)
    return ax, h