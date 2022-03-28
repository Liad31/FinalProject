import numpy as np

def get_train_sounds(train_data, sounds_bucket):
    train_sound_bucket = []
    for x in train_data:
        train_sound_bucket.append(x['musicId'])
    return np.intersect1d(train_sound_bucket, sounds_bucket)