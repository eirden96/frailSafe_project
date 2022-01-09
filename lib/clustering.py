import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def create_clustering_confusion_matrix(y_truth, cluster_labels, model_name):
    cm = confusion_matrix(y_truth, cluster_labels)

    plt.imshow(cm, interpolation= 'none', cmap='Blues')

    for (i,j), z in np.ndenumerate(cm):
        plt.text(j,i,z, ha ='center', va='center')
    plt.xlabel(model_name)
    plt.ylabel('Ground Truth')
    plt.show()   