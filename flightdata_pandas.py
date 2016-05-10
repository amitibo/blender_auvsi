import numpy as np
import pandas as pd
import NED
import glob
import os
import json

BASE_PATH = r'F:\AUVSI 2016 experiments\flight_2016_05_05\.auvsi_ground\flight_data'


def main():
    
    paths = glob.glob(os.path.join(BASE_PATH, 'resized_*.json'))
    paths = sorted(paths)
    
    lat, lon, alt = [], [], []
    ph_roll, ph_pitch, ph_yaw = [], [], []
    vn_roll, vn_pitch, vn_yaw = [], [], []
    for path in paths:
        with open(path, 'r') as f:
            d = json.load(f)
            lat.append(d['lat'])
            lon.append(d['lon'])
            alt.append(d['relative_alt'])
            ph_roll.append(d['all']['PixHawk']['roll'])
            ph_pitch.append(d['all']['PixHawk']['pitch'])
            ph_yaw.append(d['all']['PixHawk']['yaw'])
            if "VectorNav" in d['srcs']:
                vn_roll.append(d['all']['VectorNav']['roll'])
                vn_pitch.append(d['all']['VectorNav']['pitch'])
                vn_yaw.append(d['all']['VectorNav']['yaw'])
            else:
                vn_roll.append(np.NaN)
                vn_pitch.append(np.NaN)
                vn_yaw.append(np.NaN)

    dd = {
        'lat': np.array(lat)*1e-7,
        'lon': np.array(lon)*1e-7,
        'alt': np.array(alt)*1e-3,
        'ph_roll': ph_roll, 'ph_pitch': ph_pitch, 'ph_yaw': ph_yaw,
        'vn_roll': vn_roll, 'vn_pitch': vn_pitch, 'vn_yaw': vn_yaw,
    }

    df = pd.DataFrame(dd)
    df.to_csv('flight_data.csv')
    

if __name__ == '__main__':
    main()