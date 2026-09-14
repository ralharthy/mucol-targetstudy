import subprocess
import awkward as ak
import numpy as np
import pathlib
import datetime
import config
import sys

if __name__ == "__main__":
    data = {}
    for b in config.Brange:
        subprocess.run(
            [sys.executable, "akProducer.py", str(b)], #str(config.spawn)],
            check=True
        )

        B = f"{b:02d}"
        data[f"B{B}"] = ak.from_parquet(f"{config.parquetDir}/{config.simName}_B{B}.parquet")
        print(f"{config.parquetDir}/{config.simName}_B{B}.parquet was successfully added to data[B{B}]")
        print(f"B = {b:<2}, done!")

    print("\nConverting data to an awkward array...")
    data = ak.Record({
        f"B{b:02d}": data[f"B{b:02d}"]
        for b in config.Brange
    })
    suffix = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output = config.hdfs_flukaData / pathlib.Path(f"{str(config.analysisDir.name)}_{config.simName}_{suffix}.parquet")
    ak.to_parquet(data, output)
    print(f"Output: {output.name}")
    print(f"Output saved in:\n   {output}")
    print("Done!")


    