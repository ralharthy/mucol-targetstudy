import numpy as np
import pathlib

simName = "TrgCenter"

home = pathlib.Path.home()
projectDir = home / pathlib.Path("fluka/mucol-targetstudy/")
dataDir = projectDir / pathlib.Path("flukaData/")
# pathlib.Path.cwd() --> this gives the current working directory (whatever that was)
analysisDir = pathlib.Path(__file__).parent
simDir = projectDir / pathlib.Path(f"flukaSims/{analysisDir.name}/{simName}/")
parquetDir = projectDir / pathlib.Path("parquet/")
# parquetDir.mkdir(parents=True, exist_ok=True)

# HDFS: use for merged fluka outputs (reserve for spawn>1)
hdfs_flukaData = pathlib.Path("/hdfs/store/user/ralharth/mucol-targetstudy/flukaData/")
hdfs_simData = hdfs_flukaData / pathlib.Path(f"{analysisDir.name}/")

# # nfs_scratch: use for fluka output
nfs_scratch_flukaData = pathlib.Path("/nfs_scratch/ralharth/mucol-targetstudy/flukaData")
nfs_scratch_simData = nfs_scratch_flukaData / pathlib.Path(f"{analysisDir.name}/")
nfs_scratch_simOutput = nfs_scratch_flukaData / pathlib.Path(f"{analysisDir.name}/{simName}/")

spawn = 10
# Brange = range(3,11)
Brange = np.concatenate(([0], np.arange(3, 11)))

COLOR_MAP = {
    "B00": "black",
    "B03": "dodgerblue",
    "B04": "orange",
    "B05": "red",
    "B06": "darkgray",
    "B07": "darkviolet",
    "B08": "forestgreen",
    "B09": "deeppink",
    "B10": "saddlebrown",
}

PARTICLE_CODES = {
    1: "Proton",
    2: "AProton",
}