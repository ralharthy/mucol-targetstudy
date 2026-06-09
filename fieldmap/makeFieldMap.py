import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mucol.fieldmap_utils as fm
import os

# Config
directory = 'Bfield_g4blDatasets/'
filename_cylin = 'B5L200R70_fmCylinder.txt'
filename_grid = 'B5L200R70_fmGrid.txt'

## --------------------------------------------
## ------------ For cylinder data -------------
## --------------------------------------------
if filename_cylin is not None:
    filename = directory + filename_cylin
    coords_cylin = fm.getCoords(filename)

    print(f'Processing file: {filename} with coordinates: {coords_cylin}')
    data = fm.dataOrganizer(filename)
    data_sorted = fm.sortData(data)

    os.makedirs("Bfield_flukaDatasets", exist_ok=True)
    output = "Bfield_flukaDatasets/" + filename_cylin.replace('fm', 'fluka').replace('.txt', '.inp')

    print(f'Printing into output file: {output}')
    with open(output, "w+") as file:
        if coords_cylin == 'rz':
            for i in range(len(data_sorted)):
                Br = fm.tenDigit(data_sorted['Br'].iloc[i])
                Bz = fm.tenDigit(data_sorted['Bz'].iloc[i])

                name = 'FMCYLIN'
                space = ' '
                mgn = 'MGNDATA'        
                
                if i % 3 == 0:
                    line = f"{mgn:<10}{Br:>10}{Bz:>10}"
                elif i % 3 == 1:
                    line = f"{Br:>10}{Bz:>10}"
                else:
                    if i == 2:
                        line = f"{Br:>10}{Bz:>10}{name:<10}\n"
                    elif i == 5:
                        line = f"{Br:>10}{Bz:>10} &\n"
                    else:
                        line = f"{Br:>10}{Bz:>10} &&\n"
                

                file.write(line)

        if coords_cylin == 'xyz':
            for i in range(len(data_sorted)):
                Bx = fm.tenDigit(data_sorted['Bx'].iloc[i])
                By = fm.tenDigit(data_sorted['By'].iloc[i])
                Bz = fm.tenDigit(data_sorted['Bz'].iloc[i])

                name = 'FMGRID'
                space = ' '
                mgn = 'MGNDATA'        
                
                if i % 2 == 0:
                    line = f"{mgn:<10}{Bx:>10}{By:>10}{Bz:>10}"
                else:
                    if i == 1:
                        line = f"{Bx:>10}{By:>10}{Bz:>10}{name:<10}\n"
                    elif i == 3:
                        line = f"{Bx:>10}{By:>10}{Bz:>10} &\n"
                    else:
                        line = f"{Bx:>10}{By:>10}{Bz:>10} &&\n"
                

                file.write(line)

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

    os.makedirs("BfieldPlots", exist_ok=True)
    plot_output = "BfieldPlots/" + filename_cylin.replace('fm', 'fluka').replace('.txt', '.png')

    if coords_cylin == 'rz':
        print(f'Plotting the field map and saving to: {plot_output}\n')
        on_axis = (data_sorted['r'] == 0)
        z = data_sorted[on_axis]['z']
        Bz = data_sorted[on_axis]['Bz']
        plt.figure(figsize=(8, 6))
        plt.plot(z, Bz, color='orange')
        plt.xlabel('z [cm]')
        plt.ylabel('Bz [T]')
        plt.title('Bz on beam axis')
        plt.savefig(plot_output)
        plt.close()

## --------------------------------------------
## -------------- For grid data ---------------
## --------------------------------------------
if filename_grid is not None:
    filename = directory + filename_grid
    coords_grid = fm.getCoords(filename)

    print(f'Processing file: {filename} with coordinates: {coords_grid}')
    data = fm.dataOrganizer(filename)
    data_sorted = fm.sortData(data)

    os.makedirs("Bfield_flukaDatasets", exist_ok=True)
    output = "Bfield_flukaDatasets/" + filename_grid.replace('fm', 'fluka').replace('.txt', '.inp')

    print(f'Printing into output file: {output}')
    with open(output, "w+") as file:
        if coords_grid == 'rz':
            for i in range(len(data_sorted)):
                Br = fm.tenDigit(data_sorted['Br'].iloc[i])
                Bz = fm.tenDigit(data_sorted['Bz'].iloc[i])

                name = 'FMCYLIN'
                space = ' '
                mgn = 'MGNDATA'        
                
                if i % 3 == 0:
                    line = f"{mgn:<10}{Br:>10}{Bz:>10}"
                elif i % 3 == 1:
                    line = f"{Br:>10}{Bz:>10}"
                else:
                    if i == 2:
                        line = f"{Br:>10}{Bz:>10}{name:<10}\n"
                    elif i == 5:
                        line = f"{Br:>10}{Bz:>10} &\n"
                    else:
                        line = f"{Br:>10}{Bz:>10} &&\n"
                

                file.write(line)

        if coords_grid == 'xyz':
            for i in range(len(data_sorted)):
                Bx = fm.tenDigit(data_sorted['Bx'].iloc[i])
                By = fm.tenDigit(data_sorted['By'].iloc[i])
                Bz = fm.tenDigit(data_sorted['Bz'].iloc[i])

                name = 'FMGRID'
                space = ' '
                mgn = 'MGNDATA'        
                
                if i % 2 == 0:
                    line = f"{mgn:<10}{Bx:>10}{By:>10}{Bz:>10}"
                else:
                    if i == 1:
                        line = f"{Bx:>10}{By:>10}{Bz:>10}{name:<10}\n"
                    elif i == 3:
                        line = f"{Bx:>10}{By:>10}{Bz:>10} &\n"
                    else:
                        line = f"{Bx:>10}{By:>10}{Bz:>10} &&\n"
                

                file.write(line)

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