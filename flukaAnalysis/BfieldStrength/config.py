import numpy as np
import pathlib

simName = "TrgCenter"
# simName = "Sol150"

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
locations = ["esc", "prod", "det1", "det2", "det3", "det4"]

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

PARTICLE_NAME = {
    1: "Proton",
    2: "AProton",
    8: "Neutron",
    9: "ANeutron",
    10: "MuPlus",
    11: "MuMinus",
    13: "PiPlus",
    14: "PiMinus",
    15: "KaonPlus",
    16: "KaonMinus",
    17: "Lambda",
    18: "ALambda",
    20: "SigmaMinus",
    21: "SigmaPlus",
    23: "PiZero",
    34: "XiZero",
}

PARTICLE_SYM = {
    1: "p",
    8: "n",
    10: "$\\mu^+$",
    11: "$\\mu^-$",
    13: "$\\pi^+$",
    14: "$\\pi^-$",
    15: "K+",
    16: "K-",
    17: "$\\lambda$",
    20: "$\\Sigma$-",
    21: "$\\Sigma$+",
    23: "$\\pi^0$",
    34: "$\\Xi^0$",
}

class CaseInsensitiveDict(dict):
    def __init__(self, data=None):
        super().__init__()
        if data is not None:
            for key, value in data.items():
                self[key] = value

    def __getitem__(self, key):
        return super().__getitem__(key.casefold())

    def __setitem__(self, key, value):
        super().__setitem__(key.casefold(), value)

    def __contains__(self, key):
        return super().__contains__(key.casefold())

    def get(self, key, default=None):
        return super().get(key.casefold(), default)

PARTICLE_CODE = CaseInsensitiveDict({
    name: code for code, name in PARTICLE_NAME.items()
})