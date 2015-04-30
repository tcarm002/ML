"""
------------------------------------------------
Hierarchical Agglomerative Clustering
------------------------------------------------

------------------------------------------------
Support Vector Regression with RBF kernel
------------------------------------------------

"""
# Authors: Triana Carmenate, Mike Novo

import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
import sys
from sklearn.svm import SVR
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize


print(__doc__)

f_part1_name = "../data/Part1_Data.csv"
f_part1_data = open(f_part1_name)
part1_data_prescale = np.loadtxt(f_part1_data,delimiter=",")

part1_data = scale(part1_data_prescale, axis=0)

reduced_data = PCA(n_components=2).fit_transform(part1_data)

x_min, x_max = reduced_data[:, 0].min() - 5, reduced_data[:, 0].max() + 5
y_min, y_max = reduced_data[:, 1].min() - 5, reduced_data[:, 1].max() + 5


good_data_indices = []
knn_graph = kneighbors_graph(reduced_data, 5)
n_clusters = 3
connectivity = None
num_of_good_data = 0
plt.figure(figsize=(10, 4))
for index, linkage in enumerate(('average', 'complete')): # ward
    plt.subplot(1, 3, index + 1)
    model = AgglomerativeClustering(linkage=linkage,
                                            connectivity=connectivity,
                                            n_clusters=n_clusters)
    t0 = time.time()
    model.fit(reduced_data)
    elapsed_time = time.time() - t0
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=model.labels_,
                        cmap=plt.cm.spectral)
    plt.title('linkage=%s (time %.2fs)' % (linkage, elapsed_time),
                      fontdict=dict(verticalalignment='top'))

    plt.autoscale()
    
    if linkage == 'complete':
        for x in range(0, model.labels_.size):
            if (model.labels_[x] == 1 or model.labels_[x] == 2):
                good_data_indices.append(x)
                num_of_good_data += 1

    plt.subplots_adjust(bottom=0, top=.89, wspace=0,
                                left=0, right=1)
    plt.suptitle('n_cluster=%i, connectivity=%r' %
                         (n_clusters, connectivity is not None), size=17)

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks()
plt.yticks()
plt.show()


"""
------------------------------------------------
Support Vector Regression with RBF kernel
------------------------------------------------
"""

f_part2_name = "../data/Part2_Data.csv"
f_part2_data = open(f_part2_name)
part2_data = np.loadtxt(f_part2_data,delimiter=",", skiprows=1)
# part2_data instead of data

f_part2_name_norm = "../data/Part2_Data_norm.csv"
f_part2_data_norm = open(f_part2_name_norm)
part2_data_norm = np.loadtxt(f_part2_data_norm,delimiter=",", skiprows=1)

# Function to get good data using good_data_indices
def get_good_data(data, indices):
 good_data = np.zeros(shape=(len(indices), 22))
 for i in range(0, len(indices)):
     for j in range(0, 22):
         good_data[i][j] = data[indices[i]][j]
 return good_data
 

part2_good_data = get_good_data(part2_data, good_data_indices)



# Use "expert's" rule to classify 
def efficiency_classifier(x, thresh_temp, thresh_occ):
# Expanded x
 x_exp = np.zeros((21*5, 4))

 class_values = np.zeros(21*5)

 for i in range (0, x.shape[0]): # from 0 to 21
	for j in range(0,5):
		# Make X expanded
		x_exp[i*5+j][0] = x[i][get_temp_column(j+1)]
		x_exp[i*5+j][1] = x[i][get_light_column(j+1)]
		x_exp[i*5+j][2] = x[i][get_occ_column(j+1)]
		x_exp[i*5+j][3] = x[i][get_temp_corr_column(j+1)]
        # Assign "expert's" labels
		if x[i][get_temp_column(j+1)] > thresh_temp and x[i][get_light_column(j+1)] == 0 and x[i][get_occ_column(j+1)] > thresh_occ:
			class_values[i*j+j] = 1
		elif x[i][get_temp_column(j+1)] > thresh_temp and x[i][get_light_column(j+1)] == 0 and x[i][get_occ_column(j+1)] < thresh_occ:
			class_values[i*j+j] = 1
		elif x[i][get_temp_column(j+1)] < thresh_temp and x[i][get_light_column(j+1)] == 1 and x[i][get_occ_column(j+1)] > thresh_occ:
			class_values[i*j+j] = 0.5
		elif x[i][get_temp_column(j+1)] < thresh_temp and x[i][get_light_column(j+1)] == 1 and x[i][get_occ_column(j+1)] < thresh_occ:
			class_values[i*j+j] = 1	
 return x_exp, class_values


def get_occ_column(region):
	return (region*4)-2

def get_light_column(region):
	return (region*4)-1

def get_temp_column(region):
	return region*4

def get_temp_corr_column(region):
	return (region*4)+1


x_exp, class_values = efficiency_classifier(part2_good_data, 21, 1)

print x_exp[:,1]


x_exp = scale(x_exp, axis=0)

X = x_exp

y = class_values


# Fit regression model
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=.01)
y_rbf = svr_rbf.fit(X[:,:2], y).predict(X[:,:2])


# Plot the results
plt.scatter(X[:,:1], y, c='k', label='data')
plt.hold('on')
plt.plot(X[:,:1], y_rbf, c='g', label='RBF model')
plt.xlabel('Temperature')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()

