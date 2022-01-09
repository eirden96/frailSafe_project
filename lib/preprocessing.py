################################################
# All functions need for preprocessing of      #
# 1. clinical data                             #
# 2. beacons data                              #
################################################

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from datetime import datetime
from sklearn.metrics import silhouette_score
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix
from sklearn.cluster import SpectralClustering

########### PREPROCESSING FUNCTIONS FOR CLINICAL DATA #######################

#remove erroneous values from the dataset by replacing them with nan 
def remove_erroneous_values(df):
    erroneous_dict = {999: np.nan, "test non realizable": np.nan, "Test not adequate": np.nan}
    df_without_erroneous = df.replace(erroneous_dict)
    return df_without_erroneous

# Transform catecorical to numerical values using Label Encoder
def transform_categorical_to_numerical(df, new_df):
    labelen = LabelEncoder()
    for col in df.columns:
        if df[col].dtypes == np.object:
            new_df[col] = labelen.fit_transform(df[col])
    return new_df

# Fill missing (nan) values with the median of the respective feature 
def fill_na_with_median(df):
    for col in df.columns:
        df_filled = df.fillna(df[col].median())
    return df_filled

# Feature selection using variance threshold and selecting K-Best 
def feature_selection_var_kbest(df, drop_y, thres, k_best):

    #start with Variance Threshold
    vt = VarianceThreshold(threshold = thres)
    _ = vt.fit(df)

    # Get the boolean mask
    mask = vt.get_support()

    df_reduced = df.loc[:, mask]
    df_reduced.drop(drop_y, axis = 1, inplace = True)

    #select K-Best
    selector = SelectKBest(mutual_info_classif, k = k_best)
    selector.fit(df_reduced, df[drop_y])
    # Get columns to keep and create new dataframe with those only
    cols = selector.get_support(indices=True)
    features_df_new = df_reduced.iloc[:,cols]

    return features_df_new

########### PREPROCESSING FUNCTIONS FOR BEACONS DATA #######################


def keep_correct_users(df):
    df["is_partid_num"] = df.part_id.str.isdigit()
    df = df[df.is_partid_num == True]
    df.drop(["is_partid_num"], axis=1, inplace=True)
    df.dropna(inplace = True)
    df.reset_index(inplace=True)
    df.drop(["index"], axis=1, inplace=True)

    return df

def correct_room_labels(df):
    df = df.replace({r'Ki': 1, r'ki': 1, r'K': 1}, regex= True) # Kitchen
    df = df.replace({r'Lu': 2, r'li': 2, r'Sea': 2, r'Li': 2, r'Le': 2, r'Sit': 2, r'TV': 2, r'T': 2}, regex= True) # Living Room
    df = df.replace({r'Of': 3, r'De': 3, r'Wor': 3}, regex= True) # Office
    df = df.replace({r'Ba': 4, r'Wa': 4, r'Bst': 4, r'Bqt': 4}, regex= True) # Bathroom
    df = df.replace({r'Be': 5, r'be': 5, r'Cham': 5, r'2nd': 5}, regex= True) #Bedroom
    df = df.replace({r'Ver': 6, r'Out': 6, r'Gar': 6, r'Gua': 6}, regex= True) # Outdoor
    df = df.replace({r'Ent': 7, r'Hall': 7}, regex= True) # Hall 
    df = df.replace({r'Din': 8}, regex= True) # Dinning room
    df = df.replace({r'Pant': 9, r'Stor': 9}, regex= True) # Storage
    df = df.replace({r'Laun': 10}, regex= True) # Laundry
    df = df.replace({r'Box': 11}, regex= True) # Box
    replace_dic = {1: 'Kitchen', 2: 'Livingroom', 3: 'Office', 4: 'Bathroom', 5: 'Bedroom', 6: 'Outdoor', 7: 'Hall', 8: 'Dinningroom', 9: 'Storage', 10: 'Laundry', 11: 'Box' }
    df = df.replace(replace_dic) 

    return df 

def generate_new_features(df, new_df):
    i = 1
    j = 0
    rooms_list = pd.Series(df['room'].unique())

    for idx in new_df['part_id']:
        # create room dictionary
        flag = True
        room_dict = {r: 0 for r in rooms_list}
        while flag:
            # compute difference
            if df['ts_date'][i-1] == df['ts_date'][i] or pd.to_numeric(df['ts_date'][i-1]) + 1 == pd.to_numeric(df['ts_date'] [i]) : 
                time_dif = abs((datetime.strptime('{} {}'.format(df['ts_date'][i] , df['ts_time'][i]), '%Y%m%d %H:%M:%S') - datetime.strptime('{} {}'.format(df['ts_date'][i-1] , df['ts_time'][i-1]), '%Y%m%d %H:%M:%S')).total_seconds())
                room = df['room'][i-1]
                room_dict[room] +=  time_dif
            if idx != df['part_id'][i]:
                flag = False   
            i = i + 1
            if i == len(df):
                break
        total_time = sum(room_dict.values())
        
        # add % to beacons room time 
        for col in new_df.columns[new_df.columns != 'part_id']:
            if total_time != 0: 
                new_df[col][j] = "{:.1f}".format((room_dict[col]/total_time) * 100)
        j=j+1

    return new_df      








