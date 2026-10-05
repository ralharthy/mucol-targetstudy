import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mucol.fieldmap_utils as fm
import os
import subprocess as sp
import mplhep as hep
plt.style.use(hep.style.CMS)

Bvalue = 10  # Tesla
SolWidth = 200  # cm
radius = 70  # cm

# ----------------------------------------------
# Config
# ----------------------------------------------
g4bl_directory = 'g4blDatasets/'
os.makedirs("g4blDatasets", exist_ok=True)
g4blfile = "SolChannelFm.g4bl"

g4bl_data = f'B{Bvalue}L{SolWidth}R{radius}_fmCylinder.txt'

os.makedirs("flukaDatasets", exist_ok=True)
output = "flukaDatasets/" + g4bl_data.replace('fm', 'fluka').replace('.txt', '.inp')
os.makedirs("plots", exist_ok=True)
plot_output = "plots/" + g4bl_data.replace('fm', 'fluka').replace('.txt', '.png')

if os.path.exists(g4bl_directory + g4bl_data):
    os.remove(g4bl_directory + g4bl_data)

if os.path.exists(g4bl_directory + g4bl_data):
    os.remove(g4bl_directory + g4bl_data)

sp.run(
    ["bash", "-c", f"g4bl {g4blfile}"],
    check=True,
)

# ----------------------------------------------
# Upload g4bl data
# ----------------------------------------------
print(f"Processing g4bl output for:\n   B = {Bvalue} T\n   Solenoid width = {SolWidth} cm\n   Radius = {radius} cm")
cols = ['r', 'z', 'Br', 'Bz']
df = pd.read_csv(
    g4bl_directory + g4bl_data,
    sep=r"\s+",
    names=cols,
    skiprows=4
)

# ----------------------------------------------
# Helper function
# ----------------------------------------------
def tenDigit(n):
    digit_count = len(str(n))
    if digit_count > 9:
        n = round(n,6)
        return n
    else:
        return n

# ----------------------------------------------
# Producing plot
# ----------------------------------------------
print(f"\nProducing plot...")

df = df.sort_values(by=['z', 'r']).reset_index(drop=True)

Br = df['Br'].apply(tenDigit)
Bz = df['Bz'].apply(tenDigit)
z = df['z']
r = df['r']

Bz_axis = Bz[r == 0]
z_axis = z[r == 0]
z_axis = z_axis / 10  # convert from mm to cm for plotting and reporting
printMaxB = f'Maximum B-field on axis: {max(Bz_axis):.4f} T at z = {z_axis[Bz_axis.idxmax()]:.2f} cm'
printMinB = f'Minimum B-field on axis: {min(Bz_axis):.4f} T at z = {z_axis[Bz_axis.idxmin()]:.2f} cm'

plt.figure(figsize=(7, 4.5))
plt.plot(z_axis, Bz_axis, color='orange')
plt.xlabel('z [cm]', fontsize=14)
plt.ylabel('Bz [T]', fontsize=14)
plt.tick_params(axis='both', labelsize=14)
plt.title(f'Bz on beam axis for {Bvalue}T', fontsize=16)
plt.savefig(plot_output, bbox_inches='tight')
plt.close()

print(f"Output saved: {plot_output}")

# ----------------------------------------------
# Generating FLUKA input
# ----------------------------------------------
print("\nGenerating FLUKA input...")

lines = []

for i, (br, bz) in enumerate(zip(Br, Bz)):
    if i % 3 == 0:
        lines.append(f"{'MGNDATA':<10}{br:>10}{bz:>10}")

    elif i % 3 == 1:
        lines.append(f"{br:>10}{bz:>10}")

    else:
        if i == 2:
            lines.append(f"{br:>10}{bz:>10}{'FMCYLIN':<10}\n")
        elif i == 5:
            lines.append(f"{br:>10}{bz:>10} &\n")
        else:
            lines.append(f"{br:>10}{bz:>10} &&\n")

with open(output, "w") as file:
    file.write("".join(lines))
    # file.write("\n")

print('Checking if the last line is properly formatted...')
# read file
with open(output, "r") as f:
    lines = f.readlines()

last_line = lines[-1].rstrip("\n")

# ensure minimum length of 73 characters
if len(last_line) < 73:
    # pad to at least 73 chars
    last_line = last_line.ljust(73)

# force '&&' at positions 72 and 73 (0-based indexing: 71 and 72)
last_line = last_line[:71] + "&&"

# replace last line and write back
lines[-1] = last_line #+ "\n"

with open(output, "w") as f:
    f.writelines(lines)

print('Done!')

print(f"FLUKA input saved: {output}")

# ----------------------------------------------
# Printing maximum and minimum B-field on axis
# ----------------------------------------------
print("\n" + printMaxB)
print(printMinB)