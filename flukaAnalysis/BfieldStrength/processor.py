import matplotlib.pyplot as plt
import mplhep as hep
import pandas as pd
import numpy as np
import awkward as ak
from tqdm import tqdm
# from IPython.display import display, HTML
import config
import mucol as mu
import utils as u
from pathlib import Path
hep.style.use(hep.style.CMS)

## ----------------------------------------------------- >>>>>>>>>>>>
## -------------------- Upload data -------------------- >>>>>>>>>>>>
## ----------------------------------------------------- >>>>>>>>>>>>

data = {}
for b in tqdm(config.Brange, desc="Loading parquet files", unit="file"):
    B = f"{b:02d}"
    data[f"B{B}"] = ak.from_parquet(f"{config.nfs_scratch_simData}/{config.simName}_B{B}.parquet")

## ----------------------------------------------------- >>>>>>>>>>>>
## ------------------ Helper functions ----------------- >>>>>>>>>>>>
## ----------------------------------------------------- >>>>>>>>>>>>



## ----------------------------------------------------- >>>>>>>>>>>>
## ---------------------- Process ---------------------- >>>>>>>>>>>>
## ----------------------------------------------------- >>>>>>>>>>>>

part = 13
masks = {}

print("Applying Selections...")
for b in config.Brange:
    Bfield = f"B{b:02d}"
    masks[Bfield] = {}

    for loc in config.locations:
        d = data[Bfield][loc][config.PARTICLE_NAME[part]]
        masks[Bfield][loc] = {}

        ## Initial
        initial = d.p < 100
        
        ## momentum cut
        lowerMom = 0.19
        upperMom = 0.36
        pcut = (d.p >= lowerMom) & (d.p <= upperMom)

        ## emittance
        xp = d.cx / d.cz
        emit_accept, twiss = u.emittance_acceptance(d.x, xp, emittance=0.2)

        masks[Bfield][loc] = {
            "initial": initial,
            "pcut": pcut,
            "emit_accept": emit_accept
        }

## ----------------------------------------------------- >>>>>>>>>>>>
## ----------------------- Plots ----------------------- >>>>>>>>>>>>
## ----------------------------------------------------- >>>>>>>>>>>>
PLOTS_PATH = config.analysisDir / Path(f"{config.simName}") / Path(f"{config.PARTICLE_NAME[13]}") 
RESULTS_PATH = config.analysisDir / Path(f"{config.simName}") / Path(f"{config.PARTICLE_NAME[13]}") 
RESULTS_PATH.mkdir(parents=True, exist_ok=True)
ext = "png"

## --------------------------
## Fill in the selections  
## --------------------------

print("\nProducing 2D plots...")

sels = {}

for b in config.Brange:
    Bfield = f"B{b:02d}"
    sels[Bfield] = {}
    
    for loc in config.locations:
        sels[Bfield][loc] = {}
        
        mask = None
        for n, m in list(masks[Bfield][loc].items()):
            mask = m if mask is None else mask & m
            sels[Bfield][loc][n] = mask
            
            OUTPUT_PATH = PLOTS_PATH / Path(f"{loc}") / Path(f"{n}")
            OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
            
            d = data[Bfield][loc][config.PARTICLE_NAME[part]]

            ## --------------------------
            ## 2D Plots  
            ## --------------------------

            ## Phase space
            u.plot_ps(
                d.x[mask], (d.cx[mask] / d.cz[mask]),
                emittance = None,
                title = f"{config.PARTICLE_SYM[13]} phase space for {b}T [{loc}]",
                output = str(OUTPUT_PATH / f"{Bfield}_xxp.{ext}"),
            )

            u.plot_ps(
                d.y[mask], (d.cy[mask] / d.cz[mask]),
                emittance = None,
                xlabel = "y [cm]", ylabel = "y' [rad]",
                title = f"{config.PARTICLE_SYM[13]} phase space for {b}T [{loc}]",
                output = str(OUTPUT_PATH / f"{Bfield}_yyp.{ext}"),
            )

            ## Energy vs Time
            if (n != "initial"):
                ene_bins = np.linspace(0, 0.4, 81)
            else:
                ene_bins = None
                
            u.plot_ET(
                d.energy[mask], d.time[mask]*(10**9), 
                loc = loc,
                ybins = ene_bins,
                title = f"{config.PARTICLE_SYM[13]} energy vs time for {b}T [{loc}]", 
                output = str(OUTPUT_PATH / f"{Bfield}_EneTime.{ext}")
            )

            ## xy distribution
            u.plot_xy(
                d.x[mask], d.y[mask], 
                loc = loc,
                title = f"{config.PARTICLE_SYM[13]} xy distribution for {b}T [{loc}]",
                output = str(OUTPUT_PATH / f"{Bfield}_xy.{ext}"),
            )

## --------------------------
## 1D plots 
## --------------------------

print("\nProducing 1D plots and summary tables...")

for i, name in enumerate(masks["B00"]["prod"]):
    for loc in config.locations:
        OUTPUT_PATH = PLOTS_PATH / Path(f"{loc}") / Path(f"{name}")
        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        selection = sels[Bfield][loc][n]

        ## (data, loc="det1", param="p", part=13, bins=None, title=None, xlabel=None, ylabel=None, ylim=None, logy=False, norm=False, mask=None, output=None)

        ## momentum and energy plots
        e_bins = None
        p_bins = None
        pt_bins = None
        pz_bins = None
        y_plim = 120000
        y_ptlim = 40000
        y_elim = 140000
        if (name != "initial"):
            e_bins = np.linspace(0.09, 0.26, 60)
            p_bins = np.linspace(0.19, 0.36, 60)
            pt_bins = np.linspace(0, 0.4, 60)
            pz_bins = np.linspace(0, 0.4, 60)
            y_plim = 4500
            y_ptlim = 9000
            y_elim = 5000
            
        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "energy",
            bins = e_bins,
            ylim = y_elim,
            output = str(OUTPUT_PATH / f"energy.{ext}"),
        )

        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "p",
            bins = p_bins,
            ylim = y_plim,
            output = str(OUTPUT_PATH / f"p.{ext}"),
        )

        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "px",
            bins = pt_bins,
            output = str(OUTPUT_PATH / f"px.{ext}"),
        )

        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "py",
            bins = pt_bins,
            output = str(OUTPUT_PATH / f"py.{ext}"),
        )

        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "pt",
            bins = pt_bins,
            ylim = y_ptlim,
            output = str(OUTPUT_PATH / f"pt.{ext}"),
        )

        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "pz",
            bins = pz_bins,
            ylim = y_plim,
            output = str(OUTPUT_PATH / f"pz.{ext}"),
        )

        if (name == "initial"):
            u.plot1d_fields(
                data, loc = loc, part = part,
                param = "p",
                bins = np.linspace(0, 0.5, 81),
                vlines = [0.19, 0.36],
                output = str(OUTPUT_PATH / f"p_boundaries.{ext}"),
            )

        ## transverse spatial distributions
        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "x",
            output = str(OUTPUT_PATH / f"x.{ext}"),
        )

        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "y",
            output = str(OUTPUT_PATH / f"y.{ext}"),
        )

        if (loc == "esc") | (loc == "prod"):
            u.plot1d_fields(
                data, loc = loc, part = part, mask = sels, stage = name,
                param = "z",
                output = str(OUTPUT_PATH / f"z.{ext}"),
            )

        ## Angular distributions
        cz_bins = None
        cz_lim = 300000
        if (name != "initial"):
            cz_bins = np.linspace(0.5, 1, 60)
            cz_lim = 2500
            
        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "cx",
            output = str(OUTPUT_PATH / f"cx.{ext}"),
        )

        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "cy",
            output = str(OUTPUT_PATH / f"cy.{ext}"),
        )

        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "cz",
            bins = cz_bins,
            ylim = cz_lim,
            output = str(OUTPUT_PATH / f"cz.{ext}"),
        )

        ## Generation
        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "gen",
            output = str(OUTPUT_PATH / f"gen.{ext}"),
        )

        ## Mother
        u.plot1d_fields(
            data, loc = loc, part = part, mask = sels, stage = name,
            param = "Mother",
            logy = True,
            output = str(OUTPUT_PATH / f"mother.{ext}"),
        )

    mother_all = []
    mother_proton_prod = []
    mother_proton_esc = []
    det_counts = []
    for b in config.Brange:
        Bfield = f"B{b:02d}"
        
        d_prod = data[Bfield]["prod"][config.PARTICLE_NAME[part]][sels[Bfield]["prod"][name]]
        d_esc = data[Bfield]["esc"][config.PARTICLE_NAME[part]][sels[Bfield]["esc"][name]]
        d_det1 = data[Bfield]["det1"][config.PARTICLE_NAME[part]][sels[Bfield]["det1"][name]]
        d_det2 = data[Bfield]["det2"][config.PARTICLE_NAME[part]][sels[Bfield]["det2"][name]]
        d_det3 = data[Bfield]["det3"][config.PARTICLE_NAME[part]][sels[Bfield]["det3"][name]]
        d_det4 = data[Bfield]["det4"][config.PARTICLE_NAME[part]][sels[Bfield]["det4"][name]]

        # Number of pions in each event
        n_prod = ak.sum(ak.num(d_prod, axis=1))
        n_esc  = ak.sum(ak.num(d_esc,  axis=1))
        n_det1  = ak.sum(ak.num(d_det1,  axis=1))
        n_det2  = ak.sum(ak.num(d_det2,  axis=1))
        n_det3  = ak.sum(ak.num(d_det3,  axis=1))
        n_det4  = ak.sum(ak.num(d_det4,  axis=1))
        
        n_proton = ak.sum(ak.num(d_prod[d_prod.Mother == 1],  axis=1))
        n_proton_gen2 = ak.sum(ak.num(d_prod[(d_prod.Mother == 1) & (d_prod.gen == 2)],  axis=1))
        n_proton_gen3 = ak.sum(ak.num(d_prod[(d_prod.Mother == 1) & (d_prod.gen == 3)],  axis=1))
        n_proton_gen4 = ak.sum(ak.num(d_prod[(d_prod.Mother == 1) & (d_prod.gen == 4)],  axis=1))
        n_proton_gen5 = ak.sum(ak.num(d_prod[(d_prod.Mother == 1) & (d_prod.gen == 5)],  axis=1))

        n_esc_proton = ak.sum(ak.num(d_esc[d_esc.Mother == 1],  axis=1))
        n_esc_proton_gen2 = ak.sum(ak.num(d_esc[(d_esc.Mother == 1) & (d_esc.gen == 2)],  axis=1))
        n_esc_proton_gen3 = ak.sum(ak.num(d_esc[(d_esc.Mother == 1) & (d_esc.gen == 3)],  axis=1))
        n_esc_proton_gen4 = ak.sum(ak.num(d_esc[(d_esc.Mother == 1) & (d_esc.gen == 4)],  axis=1))
        n_esc_proton_gen5 = ak.sum(ak.num(d_esc[(d_esc.Mother == 1) & (d_esc.gen == 5)],  axis=1))
        
        n_aproton = ak.sum(ak.num(d_prod[d_prod.Mother == 2],  axis=1))
        n_neutron = ak.sum(ak.num(d_prod[d_prod.Mother == 8],  axis=1))
        n_aneutron = ak.sum(ak.num(d_prod[d_prod.Mother == 9],  axis=1))
        n_pip = ak.sum(ak.num(d_prod[d_prod.Mother == 13],  axis=1))
        n_pin = ak.sum(ak.num(d_prod[d_prod.Mother == 14],  axis=1))
        n_kp = ak.sum(ak.num(d_prod[d_prod.Mother == 15],  axis=1))
        n_kn = ak.sum(ak.num(d_prod[d_prod.Mother == 16],  axis=1))
        n_lambda = ak.sum(ak.num(d_prod[d_prod.Mother == 17],  axis=1))
        n_sigman = ak.sum(ak.num(d_prod[d_prod.Mother == 20],  axis=1))
        n_sigmap = ak.sum(ak.num(d_prod[d_prod.Mother == 21],  axis=1))
        n_pizero = ak.sum(ak.num(d_prod[d_prod.Mother == 23],  axis=1))
        n_kzero = ak.sum(ak.num(d_prod[d_prod.Mother == 24],  axis=1))
        n_akzero = ak.sum(ak.num(d_prod[d_prod.Mother == 25],  axis=1))
        n_xizero = ak.sum(ak.num(d_prod[d_prod.Mother == 34],  axis=1))


        mother_all.append({
            "B (T)": b,
            "Produced": n_prod,
            # "Escaped": n_esc,
            "Proton": n_proton/n_prod,
            # "AProton": n_aproton/n_prod,
            "Neutron": n_neutron/n_prod,
            # "ANeutron": n_aneutron/n_prod,
            "Pi+": n_pip/n_prod,
            "Pi-": n_pin/n_prod,
            # "Pi-0": n_pizero/n_prod,
            "Kaon+": n_kp/n_prod,
            "Kaon-": n_kn/n_prod,
            "K-zero": n_kzero/n_prod,
            "AK-zero": n_akzero/n_prod,
            "Lambda": n_lambda/n_prod,
            "Sigma-": n_sigman/n_prod,
            "Sigma+": n_sigmap/n_prod,
            # "Xi-zero": n_xizero/n_prod
        })

        mother_proton_prod.append({
            "B (T)": b,
            "Produced": n_prod,
            # "Escaped": n_esc,
            "Proton": n_proton,
            "gen-2": n_proton_gen2,
            "gen-3": n_proton_gen3,
            "gen-4": n_proton_gen4,
            "gen-5": n_proton_gen5,
        })

        mother_proton_esc.append({
            "B (T)": b,
            # "Produced": n_prod,
            "Escaped": n_esc,
            "Proton": n_esc_proton,
            "gen-2": n_esc_proton_gen2,
            "gen-3": n_esc_proton_gen3,
            "gen-4": n_esc_proton_gen4,
            "gen-5": n_esc_proton_gen5,
        })

        det_counts.append({
            "B (T)": b,
            "Produced": n_prod,
            "Escaped": n_esc,
            "det1": n_det1,
            "det2": n_det2,
            "det3": n_det3,
            "det4": n_det4,
        })
    
    df_mother_all = pd.DataFrame(mother_all)
    df_mother_proton_prod = pd.DataFrame(mother_proton_prod)
    df_mother_proton_esc = pd.DataFrame(mother_proton_esc)
    df_det_counts = pd.DataFrame(det_counts)

    # Save to CSV
    df_mother_all.to_csv(str(RESULTS_PATH / Path(f"{name}_mother_all.csv")), index=False, float_format="%.6g")
    print("Saved output: ", str(RESULTS_PATH / Path(f"{name}_mother_all.csv")))
        
    df_mother_proton_prod.to_csv(str(RESULTS_PATH / Path(f"{name}_mother_proton_prod.csv")), index=False)
    print("Saved output: ", str(RESULTS_PATH / Path(f"{name}_mother_proton_prod.csv")))

    df_mother_proton_esc.to_csv(str(RESULTS_PATH / Path(f"{name}_mother_proton_esc.csv")), index=False)
    print("Saved output: ", str(RESULTS_PATH / Path(f"{name}_mother_proton_esc.csv")))
        
    df_det_counts.to_csv(str(RESULTS_PATH / Path(f"{name}_det_counts.csv")), index=False)
    print("Saved output: ", str(RESULTS_PATH / Path(f"{name}_det_counts.csv")))
        