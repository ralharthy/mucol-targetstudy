import awkward as ak
import pandas as pd
import numpy as np
import mucol as mu
import pathlib as path
import os
import sys

# -----------------------
# Config
# -----------------------
simName = "TrgCenter"
studyName = "BfieldStrength"
rootDir = path.Path(__file__).resolve().parents[2]
simulationDir = rootDir / path.Path(f"flukaSims/{studyName}/{simName}/")

# Get B-field from run.py
if len(sys.argv) < 2:
    raise ValueError("Missing Bfield argument")
Bfield = f"{int(sys.argv[1]):02d}"

locations = ["esc", "prod", "det1"]
cols = [
    "id", "energy", "p",
    "x", "y", "z",
    "cx", "cy", "cz",
    "time", "gen", "event", "parentId"
]
meta = {
    "beamEnergy": 8,
    "nPrimaries": 1_000_000 * int(sys.argv[2]),
    "Bfield": int(Bfield),
    "target": {
        "material": "Inconel",
        "radius_cm": 0.15,
        "length_cm": 17,
    }
}

# -----------------------
# Main: load everything
# -----------------------
all_events = {}

for loc in locations:
    location_events = []
    
    for r in range(1, int(sys.argv[2]) + 1):
        runNumber = f"{Bfield}{r:03d}"
        filename = f"{simulationDir}/run{runNumber}_{loc}.txt"
        df = pd.read_csv(
            filename,
            sep=r"\s+",
            names=cols,
            skiprows=1
        )
        events = mu.build_events(df)
        events = ak.with_field(events, r, "run")
        location_events.append(events)
        
    # combine events
    events = ak.concatenate(location_events)
    events = ak.with_field(events, loc, "location")
    all_events[loc] = events

# -----------------------
# Final structure
# -----------------------
all_events = ak.Record(all_events)
particle_events = mu.combine_particles(all_events, locations)
data = ak.with_field(particle_events, meta, "metadata")

# Output to parquet
analysisDir = path.Path(__file__).resolve().parent
outputDir = analysisDir / path.Path("parquet/")
os.makedirs(outputDir, exist_ok=True)
output = outputDir / path.Path(f"{simName}_B{Bfield}.parquet")
ak.to_parquet(data, output)

print(f"Saved output to: {output}")