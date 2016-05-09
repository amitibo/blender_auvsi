import bpy
from bpy import context
import numpy as np
import NED
import glob
import os
import json
import math


BASE_PATH = r'I:\AUVSI 2016 experiments\flight_2016_04_17\.auvsi_ground\flight_data'
PLANE_SCALE = 0.01

def load_flightdata():
    flight_datas = glob.glob(os.path.join(BASE_PATH, 'resized_*.json'))
    flight_datas = sorted(flight_datas)
    
    yaw_pixhawk = []
    yaw_vectornav = []
    pitch = []
    roll = []
    src = []
    lat = []
    lon = []
    alt = []
    
    for flight_data in flight_datas:
        with open(flight_data, 'r') as f:
            data = json.load(f)
            yaw_pixhawk.append(data['all']['PixHawk']['yaw'])
            try:
                yaw_vectornav.append(data['all']['VectorNav']['yaw'])
                src.append(1)
            except:
                yaw_vectornav.append(0)
                src.append(0)
            pitch.append(data['pitch'])
            roll.append(data['roll'])
            
            lat.append(data['lat']*1e-7)
            lon.append(data['lon']*1e-7)
            alt.append(data['relative_alt']*1e-3)

    ned = NED.NED(lat[0], lon[0], alt[0])
    X, Y, H = [], [], []
    print('**********\n'*3)
    for la, lo, al in zip(lat, lon, alt):
        print(la, lo, al)
        y, x, h = ned.geodetic2ned([la, lo, al])
        print(y, x, h)
        X.append(x)
        Y.append(y)
        H.append(h)
    
    flight_data = {
        'x': X,
        'y': Y,
        'z': H,
        'yaw': yaw_pixhawk
    }
    return flight_data

    yaw_pixhawk = np.array(yaw_pixhawk)
    yaw_vectornav = np.array(yaw_vectornav)
    pitch = np.array(pitch)
    roll = np.array(roll)
    lat = np.array(lat)
    lon = np.array(lon)
    alt = np.array(alt)
    
    

def main():

    obj = bpy.context.selected_objects[0]
    bpy.context.active_object.animation_data_clear()
    
    fd = load_flightdata()
    
    obj.scale = (PLANE_SCALE, PLANE_SCALE, PLANE_SCALE)
    for i, (x, y, z) in enumerate(zip(fd['x'], fd['y'], fd['z'])):
        bpy.context.scene.frame_set(i)
        obj.location = (x/100, y/100, z/100)
        obj.rotation_euler[0] = 0
        obj.rotation_euler[1] = math.pi/2
        obj.rotation_euler[2] = 0#math.pi/2
        obj.keyframe_insert('location')
        if i == 100:
            break
    
    
if __name__ == '__main__':
    main()
    