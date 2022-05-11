import  json
import  matplotlib.pyplot as plt
import numpy as np
f = open('../../Downloads/tiktokusernationalistics_rel.json')
f2 = open('../../Downloads/videos_rel.json')
# returns JSON object as
# a dictionary
users = json.load(f)
print(users)
videos = json.load(f2)
arr1 = []
arr2 = []
for x in users[:1000]:
    arr1.append(x['relevancyScore'])
for x in videos:
    arr2.append(x['relScore'])
print(len(arr1))
print(len(arr2))
arr2 = np.array(arr2)[np.array((arr2))>0]
plt.hist(arr1, density=True, bins=100)  # density=False would make counts
plt.ylabel('Probability')
plt.xlabel('Data')
plt.show()
plt.hist(arr2, density=True, bins=100)  # density=False would make counts
plt.ylabel('Probability')
plt.xlabel('Data')
plt.show()
