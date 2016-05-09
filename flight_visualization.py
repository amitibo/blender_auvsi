import bpy
from bpy import context
import numpy as np
import pandas as pd
import NED
import glob
import os
import json

BASE_PATH = r'I:\AUVSI 2016 experiments\flight_2016_05_05\.auvsi_ground\flight_data'


def main():

    obj = bpy.context.selected_objects[0]
    bpy.context.active_object.animation_data_clear()
    
    df = pd.read_csv('flight_data.csv')
    
    row = next(df.iterrows())[1]
    ned = NED.NED(row['lat'], row['lon'], row['alt'])
    
    for row in df.iterrows():
        bpy.context.scene.frame_set(row[0])
        data = row[1]
        y, x, h = ned.geodetic2ned([data['lat'], data['lon'], data['alt']])
        obj.location = (x/100, y/100, -h/100)
        obj.keyframe_insert('location')
    
    
if __name__ == '__main__':
    main()
    