import os
import pandas as pd
import matplotlib.pyplot as plt


N = 0 #Total count of number of files in all directories

labels = []
freqs = []
for dirpath, dirnames, filenames in os.walk('dataset'):
    N += len(filenames)
    labels.append(dirpath.split('\\')[-1])
    freqs.append(len(filenames))
    print("Files in", dirpath, len(filenames))
labels = labels[1:]
freqs = freqs[1:]

print("Total files", N)
print('num countries', len([subdirs for subdirs in os.walk('dataset')]))

#######Plotting#######
# d = {'Countries': labels, 'Frequencies': freqs}
# df = pd.DataFrame(data=d)
# df = df.sort_values(by=['Frequencies'], ascending=False)
# df = df.reset_index(drop=True)
# df = df.loc[0:(len(df)/2), :]
# #df.set_index('Countries')
#
# df.plot(x="Countries", y="Frequencies", kind='bar', figsize=(10,2))
# plt.xticks(rotation=45, ha="right")
# plt.subplots_adjust(bottom=0.2)
# plt.title('Frequencies of Countries from 50k GeoWorld Game samples')
# plt.show()