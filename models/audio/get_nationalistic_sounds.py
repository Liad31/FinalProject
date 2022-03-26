import os
import  numpy as np
import pandas as pd
import  matplotlib.pyplot as plt
sounds = np.load('nationalistic_songs.npy', allow_pickle=True)
sounds =list(sounds)
df = pd.read_csv('../../../Downloads/sheet1.csv')
df = df['קישור לסאונד בטיקטוק']
for i in range(len(df)):
    sounds.append(str(df.iat[i]).split('-')[-1])
    print(type(sounds[i]))
    print(type(sounds[-1]))
sounds = np.array(sounds)
sounds = np.array(sounds)
np.save('nationalistic_songs', sounds)
