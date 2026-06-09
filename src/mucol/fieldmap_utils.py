import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def tenDigit(n):
    digit_count = len(str(n))
    if digit_count > 9:
        n = round(n,6)
        return n
    else:
        return n
    
def getCoords(filename):
    with open(filename) as f:
        # skip 4 lines
        for _ in range(4):
            next(f)
        
        # read the next line
        line = next(f).strip()

        cols = line.split()
        ncols = len(cols)

    if ncols == 4:
        coords = 'rz'
    elif ncols == 6:
        coords = 'xyz'
    
    return coords

def dataOrganizer(filename):
    coord = getCoords(filename)

    if coord == 'rz':
        cols = ['r', 'z', 'Br', 'Bz']
    elif coord == 'xyz':
        cols = ['x', 'y', 'z', 'Bx', 'By', 'Bz']

    # data structure
    data = {}

    if coord == 'rz':
        df = pd.read_csv(
                filename,
                sep=r'\s+',
                names=cols,
                skiprows=4
            )
        df['r'] = df['r']/10
        df['z'] = df['z']/10
        df['Btot'] = np.sqrt(df['Br']**2 + df['Bz']**2)
    elif coord == 'xyz':
        df = pd.read_csv(
                filename,
                sep=r'\s+',
                names=cols,
                skiprows=4
            )
        df['x'] = df['x']/10
        df['y'] = df['y']/10
        df['z'] = df['z']/10
        df['Btot'] = np.sqrt(df['Bx']**2 + df['By']**2 + df['Bz']**2)
    
    data = df
    return data

def sortData(data):
    ncol = data.shape[1]
    if ncol == 5:
        data_sorted = data.sort_values(by=['z', 'r'])

    elif ncol == 7:
        data_sorted = data.sort_values(by=['z', 'y', 'x'])

    return data_sorted