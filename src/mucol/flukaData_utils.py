import awkward as ak
import pandas as pd
import numpy as np

def eta_from_cz(cz):
    cz = ak.where(cz == 1.0,  0.9999999, cz)
    cz = ak.where(cz == -1.0, -0.9999999, cz)
    return 0.5 * np.log((1.0 + cz) / (1.0 - cz))
    
def build_events(df):
    df = df.sort_values("event").reset_index(drop=True)
    arr = ak.Array(df.to_dict(orient="list"))

    # kinematics (particle-level)
    px = arr.p * arr.cx
    py = arr.p * arr.cy
    pt = np.sqrt(px**2 + py**2)
    pz = arr.p * arr.cz
    eta = eta_from_cz(arr.cz)

    arr = ak.with_field(arr, px, "px")
    arr = ak.with_field(arr, py, "py")
    arr = ak.with_field(arr, pt, "pt")
    arr = ak.with_field(arr, pz, "pz")
    arr = ak.with_field(arr, eta, "eta")

    # group into events
    events = ak.unflatten(arr, ak.run_lengths(arr.event))

    return events

def split_by_particle(events):
    return ak.Record({
        # "Pion": events[(events.id == 13) | (events.id == 14) | (events.id == 23)],
        "PiPlus": events[events.id == 13],
        "PiMinus": events[events.id == 14],
        # "PiZero": events[events.id == 23],
        "MuPlus": events[events.id == 10],
        "MuMinus": events[events.id == 11],
        # "Proton": events[events.id == 1],
        "KaonPlus": events[events.id == 15],
        "KaonMinus": events[events.id == 16],
        "Lambda": events[events.id == 17],
        "AntiLambda": events[events.id == 18],
        "SigmaMinus": events[events.id == 20],
        "SigmaPlus": events[events.id == 21],
    })

def combine_particles(events, locations):
    return ak.Record({
        loc: split_by_particle(events[loc])
        for loc in locations
    })