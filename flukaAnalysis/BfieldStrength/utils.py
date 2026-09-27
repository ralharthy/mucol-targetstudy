import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import awkward as ak
import mucol as mu
import config
hep.style.use(hep.style.CMS)

def emittance_acceptance(x, xp, emittance=0.2):
    """
    Calculate the transverse emittance and return an Awkward boolean
    mask selecting particles inside the specified emittance ellipse.

    Parameters
    ----------
    x : awkward.Array
        Particle x positions [cm].
    xp : awkward.Array
        Particle x' values (cx/cz) [rad].
    emittance : float, optional
        Maximum accepted emittance [cm rad].
        Default is 0.2 cm rad.

    Returns
    -------
    accept_mask : awkward.Array
        Boolean Awkward Array with the same structure as x/xp.
        True for particles inside the emittance ellipse.
    twiss_params : list
        [alpha, beta, gamma]
    """

    ## Flatten only for calculating the beam moments
    x_flat = ak.to_numpy(ak.flatten(x))
    xp_flat = ak.to_numpy(ak.flatten(xp))

    ## Twiss parameters
    xx = np.mean(x_flat**2)
    xxp = np.mean(x_flat * xp_flat)
    xpxp = np.mean(xp_flat**2)

    eps = np.sqrt(xx * xpxp - xxp**2)

    beta = xx / eps
    alpha = -xxp / eps
    gamma = xpxp / eps

    ## Emittance ellipse
    accept_mask = ( (gamma * x**2) + (2 * alpha * x * xp) + (beta * xp**2) ) <= emittance

    ## Return Twiss parameters
    twiss_params = [alpha, beta, gamma]

    return accept_mask, twiss_params


def plot_ps(x, xp, emittance=0.2, title=None, xlabel=None, ylabel=None, cmap="viridis", vmax=None, output=None):
    """
    Plot transverse phase space (x, x') with an emittance acceptance ellipse.

    Parameters
    ----------
    x : awkward.Array
        Particle x positions [cm].
    xp : awkward.Array
        Particle x' values (cx/cz) [rad].
    emittance : float
        Maximum accepted emittance [cm rad].
    title : str, optional
        Plot title.
    xlabel : str, optional
        x-axis label.
    ylabel : str, optional
        y-axis label.
    cmap : str, optional
        Matplotlib colormap.
    """
    ## Calculate acceptance mask and Twiss parameters
    if emittance is not None:
        accept_mask, twiss_params = emittance_acceptance(
            x,
            xp,
            emittance=emittance
        )
        alpha, beta, gamma = twiss_params

    ## Flatten for plotting
    x_flat = ak.to_numpy(ak.flatten(x))
    xp_flat = ak.to_numpy(ak.flatten(xp))

    ## Emittance ellipse
    if emittance is not None:
        phi = np.linspace(0, 2 * np.pi, 500)
    
        x_ellipse = np.sqrt(emittance * beta) * np.cos(phi)
    
        xp_ellipse = (
            -alpha / np.sqrt(beta)
            * np.sqrt(emittance)
            * np.cos(phi)
            + np.sqrt(emittance / beta)
            * np.sin(phi)
        )

    ## Histogram
    fig, ax = plt.subplots(figsize=(7, 5.4))

    xbins = np.linspace(-30, 30, 100)
    ybins = np.linspace(-0.5, 0.5, 100)

    H, xedges, yedges = np.histogram2d(
        x_flat, xp_flat,
        bins=[xbins, ybins],
    )

    pcm = ax.pcolormesh(
        xedges,
        yedges,
        H.T,
        shading="auto",
        cmap=cmap,
        vmax=vmax,
    )

    ## Acceptance ellipse
    if emittance is not None:
        ax.plot(
            x_ellipse, xp_ellipse,
            "r-", lw=1.3,
            label=fr"$\epsilon={emittance}$ cm·rad",
        )
        ax.legend(fontsize=13, labelcolor="white")

    ## Labels
    ax.set_xlabel(
        xlabel if xlabel is not None else r"$x$ [cm]",
        fontsize=14,
    )
    ax.set_ylabel(
        ylabel if ylabel is not None else r"$x'$ [rad]",
        fontsize=14,
    )
    
    ax.set_title(title, fontsize=15)
    ax.tick_params(labelsize=14)

    ## Colorbar
    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label("Count", fontsize=14)
    cbar.ax.tick_params(labelsize=14)

    ## Particle counts
    if emittance is not None:
        total = ak.sum(ak.num(x, axis=-1))
        accepted = ak.sum(accept_mask)
    
        ax.text(
            0.05, 0.07,
            f"Total = {total:,}\n"
            f"Accepted = {accepted:,}\n"
            f"Fraction = {accepted / total:.1%}",
            transform=ax.transAxes,
            color="white",
            fontsize=12,
            fontweight="bold",
            ha="left",
            va="bottom",
        )
    else:
        total = ak.sum(ak.num(x, axis=-1))
    
        ax.text(
            0.05, 0.06,
            f"Total = {total:,}",
            transform=ax.transAxes,
            color="white",
            fontsize=12,
            fontweight="bold",
            ha="left",
            va="bottom",
        )

    if output is not None:
        fig.savefig(output, bbox_inches="tight")
        plt.close()
        print("Saved output: ", output)
    else:
        plt.tight_layout()
        plt.show()

    # return fig, ax


def plot_ET(energy, time, loc=None, title=None, xbins=None, ybins=None, xlabel=None, ylabel=None, cmap="viridis", vmax=None, output=None):
    """
    Plot a 2D energy-vs-time histogram.

    Parameters
    ----------
    energy : awkward.Array
        Energy values. Can be an Awkward Array or NumPy array.
    time : awkward.Array
        Time values. Can be an Awkward Array or NumPy array.
    loc : str, optional
        Location of data.
    title : str, optional
        Plot title.
    xbins : array-like, optional
        Bin edges for the time axis.
    ybins : array-like, optional
        Bin edges for the energy axis.
    xlabel : str, optional
        X-axis label.
    ylabel : str, optional
        Y-axis label.
    cmap : str, default="viridis"
        Matplotlib colormap.
    vmax : float, optional
        Maximum value for the color scale.
    output : str, optional
        Path to save the figure. If None, the figure is not saved.

    Returns
    -------
    fig, ax
        Matplotlib figure and axes.
    """

    ## Convert Awkward Arrays to flat NumPy arrays
    energy = ak.to_numpy(ak.flatten(energy))
    time = ak.to_numpy(ak.flatten(time))

    xbin_loc = {
        "prod": np.linspace(4.7, 5.4, 50),
        "esc": np.linspace(4.7, 5.4, 50),
        "det1": np.linspace(7.5, 8.5, 50),
        "det2": np.linspace(10.8, 11.8, 50),
        "det3": np.linspace(14, 16.5, 50),
        "det4": np.linspace(17.5, 20, 50),
    }

    ## Default binning
    if xbins is None:
        if loc is None:
            xbins = np.linspace(np.min(time), 20, 50)
        else:
            xbins = xbin_loc[loc] 

    if ybins is None:
        ybins = np.linspace(0, 4, 50)

    ## 2D histogram
    H, xedges, yedges = np.histogram2d(
        time,
        energy,
        bins=[xbins, ybins],
    )

    ## Plot
    fig, ax = plt.subplots(1, 1, figsize=(7, 5.4))

    pcm = ax.pcolormesh(
        xedges,
        yedges,
        H.T,
        shading="auto",
        cmap=cmap,
        vmax=vmax,
    )

    ax.tick_params(labelsize=14)
    ax.set_xlabel(
        xlabel if xlabel is not None else r"Time [ns]",
        fontsize=14,
    )
    ax.set_ylabel(
        ylabel if ylabel is not None else r"Energy [GeV]",
        fontsize=14,
    )
    ax.set_title(title, fontsize=15)

    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label("Count", fontsize=14)
    cbar.ax.tick_params(labelsize=14)

    if output is not None:
        fig.savefig(output, bbox_inches="tight")
        plt.close()
        print("Saved output: ", output)
    else:
        plt.tight_layout()
        plt.show()


def plot_xy(x, y, loc=None, title=None, xbins=None, ybins=None, xlabel=None, ylabel=None, cmap="viridis", vmax=None, output=None):
    """
    Plot a 2D energy-vs-time histogram.

    Parameters
    ----------
    x : awkward.Array
        Energy values. Can be an Awkward Array or NumPy array.
    y : awkward.Array
        Time values. Can be an Awkward Array or NumPy array.
    loc : str, optional
        Location of data.
    title : str, optional
        Plot title.
    xbins : array-like, optional
        Bin edges for the time axis.
    ybins : array-like, optional
        Bin edges for the energy axis.
    xlabel : str, optional
        X-axis label.
    ylabel : str, optional
        Y-axis label.
    cmap : str, default="viridis"
        Matplotlib colormap.
    vmax : float, optional
        Maximum value for the color scale.
    output : str, optional
        Path to save the figure. If None, the figure is not saved.
    """

    ## Convert Awkward Arrays to flat NumPy arrays
    x = ak.to_numpy(ak.flatten(x))
    y = ak.to_numpy(ak.flatten(y))

    xybins = np.linspace(-10,10,100)

    ## Default binning
    if xbins is None:
        xbins = xybins

    if ybins is None:
        ybins = xybins

    ## 2D histogram
    H, xedges, yedges = np.histogram2d(
        x, y,
        bins=[xbins, ybins],
    )

    ## Plot
    fig, ax = plt.subplots(1, 1, figsize=(7, 5.4))

    pcm = ax.pcolormesh(
        xedges,
        yedges,
        H.T,
        shading="auto",
        cmap=cmap,
        vmax=vmax,
    )

    ax.tick_params(labelsize=14)
    ax.set_xlabel(
        xlabel if xlabel is not None else r"x [cm]",
        fontsize=14,
    )
    ax.set_ylabel(
        ylabel if ylabel is not None else r"y [cm]",
        fontsize=14,
    )
    ax.set_title(title, fontsize=15)

    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label("Count", fontsize=14)
    cbar.ax.tick_params(labelsize=14)

    if output is not None:
        fig.savefig(output, bbox_inches="tight")
        plt.close()
        print("Saved output: ", output)
    else:
        plt.tight_layout()
        plt.show()
    

param_title = {
    "energy": "Energy",
    "p": "p",
    "px": r"$p_x$",
    "py": r"$p_y$",
    "pt": r"$p_T$",
    "pz": r"$p_z$",
    "x": "x-spatial",
    "y": "y-spatial",
    "z": "z-spatial",
    "cx": "Angular",
    "cy": "Angular",
    "cz": "Angular",
    "gen": "Generation",
    "Mother": "Mother Id",
    "ICODE": "Interaction code",
}

param_xlabel = {
    "energy": "Energy [GeV]",
    "p": "p [GeV/c]",
    "px": r"$p_x$ [GeV/c]",
    "py": r"$p_y$ [GeV/c]",
    "pt": r"$p_T$ [GeV/c]",
    "pz": r"$p_z$ [GeV/c]",
    "x": "x [cm]",
    "y": "y [cm]",
    "z": "z [cm]",
    "cx": r"$\cos\theta_x$",
    "cy": r"$\cos\theta_y$",
    "cz": r"$\cos\theta_z$",
    "gen": "Generation",
    "Mother": "Mother Id",
    "ICODE": "Interaction code",
}

param_bins = {
    "energy": np.linspace(0,6,81),
    "p": np.linspace(0,6,81),
    "px": np.linspace(0,1,81),
    "py": np.linspace(0,1,81),
    "pt": np.linspace(0,1,81),
    "pz": np.linspace(0,6,81),
    "x": np.linspace(-30,30,91),
    "y": np.linspace(-30,30,91),
    "z": np.linspace(-8.5,8.5,86),
    "cx": np.linspace(-1,1,81),
    "cy": np.linspace(-1,1,81),
    "cz": np.linspace(-1,1,81),
    "gen": np.linspace(0.5,6.5,19),
    "Mother": np.linspace(0.5,34.5,35),
    "ICODE": np.linspace(100.5,105.5,6),
}

def plot1d_fields(data, loc="det1", param="p", part=13, bins=None, title=None, xlabel=None, ylabel=None, ylim=None, logy=False, norm=False, mask=None, stage=None, vlines=None, output=None):
    """
    Plot a 1D distribution of a particle parameter for different magnetic
    field configurations.

    Parameters
    ----------
    data : dictionary of awkward.Array
        Simulation data containing the different magnetic field configurations
        (e.g. B01, B02, ...).
    loc : str, optional
        Detector/location name from which to extract the particle data.
        Default is "det1".
    param : str, optional
        Particle parameter to plot.
        Examples: "p", "px", "py", "pt", "pz", "energy", "x", "y", "z",
        "cx", "cy", "cz", "gen", "Mother", "ICODE".
        Default is "p".
    part : int, optional
        Particle ID used to select the particle symbol for plot labels.
        Default is 13.
    bins : array-like, optional
        Histogram bin edges. If None, the predefined bins in `param_bins`
        corresponding to `param` are used.
    title : str, optional
        Custom plot title. If None, the default title is used.
    xlabel : str, optional
        Custom x-axis label. If None, the predefined label corresponding
        to `param` is used.
    ylabel : str, optional
        Custom y-axis label. If None, the default particle count label
        is used.
    ylim : float, optional
        Upper limit for the y-axis.
    logy : bool, optional
        If True, use a logarithmic scale for the y-axis.
        Default is False.
    norm : bool, optional
        If True, normalize the histogram by the number of primary protons
        (`nPrimaries`) for each simulation.
        Default is False.
    mask : bool Awkward.array, optional
        Mask to be applied on the data.
    vlines : list, optional
        draws vertical lines on the plot.
    output : str, optional
        Path to save the figure. If None, the figure is not saved.
    """
    fig, ax = plt.subplots(1, 1, 
                           figsize=(6.5, 5))

    if bins is None:
            bins = param_bins[param]
    
    for b in config.Brange:
        Bfield = f"B{b:02d}"

        hist = data[Bfield][loc][config.PARTICLE_NAME[part]][param]

        sel = ak.ones_like(hist, dtype=bool)
        if mask is not None:
            sel = mask[Bfield][loc][stage]

        values = ak.flatten(hist[sel])
        
        # Normalize to number of protons if requested
        weights = None
        if norm:
            weights = np.ones(len(values)) / data[Bfield].metadata.nPrimaries
                
        ax.hist(
                values,
                bins=bins,
                histtype="step",
                color=config.COLOR_MAP[Bfield],
                label=f"{b}T ",
                weights=weights,
            )

    # Draw vertical lines
    if vlines is not None:
        if np.isscalar(vlines):
            vlines = [vlines]

        for x in vlines:
            ax.axvline(x, color="black", linestyle="--", linewidth=0.8)
    
    if logy:
        ax.set_yscale("log")
        ax.tick_params(
            axis="y",
            which="both",
            labelsize=14
        )
    ax.set_xlabel(param_xlabel[param], fontsize=14)
    ax.set_ylabel(rf'{config.PARTICLE_SYM[part]} count', fontsize=14)
    if norm:
        ax.set_ylabel(
            rf'{config.PARTICLE_SYM[part]} / primary proton',
            fontsize=14
        )
    ax.legend(fontsize=12)
    ax.tick_params(axis='both', labelsize=14)
    
    if ylim is not None:
        ax.set_ylim(0,ylim)
    
    if title is None:
        ax.set_title(fr'{config.PARTICLE_SYM[part]} {param_title[param]} distributions [{loc}]', fontsize=16)
    else:
        ax.set_title(title, fontsize=16)

    text_xcoord = 0.95
    text_ycoord = 0.07
    text_ha = "right"
    if (param_title[param] == "Angular"):
        text_xcoord = 0.05
        text_ycoord = 0.07
        text_ha = "left"
    
    ax.text(
        text_xcoord, text_ycoord,
        f"{data[Bfield].metadata.beamEnergy} GeV beam\n"
        f"{data[Bfield].metadata.nPrimaries:,} protons\n"
        f"{data[Bfield].metadata.target.material} target",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        ha=text_ha,
        va="bottom"
    )

    if output is not None:
        fig.savefig(output, bbox_inches="tight")
        plt.close()
        print("Saved output: ", output)
    else:
        plt.tight_layout()
        plt.show()