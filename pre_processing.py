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

def convert_to_numeric(original_data = clinical_data, replace_dict = None, isRegex = False):
    try: 
        if replace_dict != None:
            print(" We have a replace dict")
            preprocessed_data = original_data.replace(replace_dict, regex = isRegex)
            return preprocessed_data

        print("No replace dictionary given. Will use pre-defined replacements")
        preprocessed_data = original_data.replace({'F': 0, 'M': 1})
        preprocessed_data = preprocessed_data.replace({'Yes': 1, 'No' :0})
        preprocessed_data = preprocessed_data.replace({r'well': 2, r'moderately': 1, r'poorly': 0}, regex=True)
        preprocessed_data = preprocessed_data.replace({True: 1, False :0})
        preprocessed_data = preprocessed_data.replace({'<5 sec': 1, '>5 sec' :0})
        preprocessed_data = preprocessed_data.replace({'> 5 h per week': 2,'> 2 h and < 5 h per week': 1, '< 2 h per week' :0})
        preprocessed_data = preprocessed_data.replace({r'5': 5, r'4': 4, r'3': 3, r'2': 2, r'1': 1}, regex=True)
        preprocessed_data = preprocessed_data.replace({'Frail': 2,'Pre-frail': 1, 'Non frail' :0})
        return preprocessed_data
        
    except Exception as e:
        raise e

def remove_erroneous_data(original_data, erroneous_dic):

    preprocessed_data = original_data.replace(erroneous_dic)
    return preprocessed_data


def replace_erroneous_data(data):
    pass 


