################################################
#  These functions are used for pre-processing #
# The goals are                                #
# 1. non-numeric values to numeric             #
# 2. removing erroneous values and replace     #
#    with NaN                                  #
# 3. fill in missing values                    #
################################################

import pandas as pd

clinical_data = pd.read_csv('clinical_dataset.csv', delimiter=';')

def convert_to_numeric(original_data = clinical_data, replace_dict = None, replace_dic_regex = None):
    try: 
        preprocessed_data = original_data.replace(replace_dict)
        preprocessed_data = preprocessed_data.replace(replace_dic_regex, regex = True)
        return preprocessed_data
        
    except Exception as e:
        raise e

def remove_erroneous_data(original_data, erroneous_dic):

    preprocessed_data = original_data.replace(erroneous_dic)
    return preprocessed_data


def replace_erroneous_data(data):
    pass 


