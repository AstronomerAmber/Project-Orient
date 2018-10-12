import numpy as np
import pandas as pd
import logging
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level = logging.DEBUG)

user_cols = ['user_id','age','gender','occupation','zip_code']
#importing the data files onto dataframes
df_users = pd.read_csv('../Data/u.user', sep='|', names=user_cols, encoding='latin-1')

def nearest_region(x1):
    x = x1[0]
    if x=='0' or x=='1':
        return 'Eastcoast'
    if x=='2' or x=='3':
        return 'South'
    if x=='4' or x=='5' or x=='6':
        return 'Midwest'
    if x=='7' or x=='8':
        return 'Frontier'
    if x=='9' :
        return 'Westcoast'
    else:
        return 'None'

def nearest_region_nums(x1):
    x = x1[0]
    if x=='0' or x=='1':
        return [0.0,0.1]
    if x=='2' or x=='3':
        return [0.2,0.3]
    if x=='4' or x=='5' or x=='6':
        return [0.4,0.6]
    if x=='7' or x=='8':
        return [0.7,0.8]
    if x=='9' :
        return [0.9,1.0]
    else:
        return 'None'

def tuned_users(nearest_nyears,U_sim,age,gender,occupation,location,W_age, W_gen,W_job, W_zip):#Create onehot encoded matrix for user demographic information
    def nearest_nyears(x, base=nearest_nyears):
        return int(base * round(float(x)/base))
    A = W_gen * pd.get_dummies(df_users.gender)
    B = W_job * pd.get_dummies(df_users.occupation)
    C = W_age * pd.get_dummies(df_users['age'].apply(nearest_nyears))
    D = W_zip * pd.get_dummies(df_users['zip_code'].apply(nearest_region))

    df_new = pd.concat([A,B,C,D], axis = 1)

    User_info = df_new.iloc[0].copy() #get an example user profile
    User_info.iloc[0:] = 0 #empty profile to fill with input user
    User_info[gender] = 1 * W_gen
    User_info[nearest_nyears(age)] = 1 * W_age
    User_info[nearest_region(location)] = 1 * W_zip
    User_info[occupation] = 1 * W_job
    #User_info.head(50)

    #User: r = np.random.randint(0,943), for random user df_new.iloc[r] to use a random user from dataset
    sim=[]
    for i in range(len(df_new)): #finds the
        sim.append(cosine_similarity([User_info], [df_new.iloc[i]]))

    user_idx = np.where(np.squeeze(sim) >= U_sim)[0] # X users with the highest similarity to input user
    if len(user_idx) < 10 or len(user_idx) > 200:
        user_idx = np.where(np.squeeze(sim) >= np.sort(np.squeeze(sim))[-100])[0]
    #user = user_idx+1
    return(user_idx)

def region_info(nearest_nyears,U_sim,age,gender,occupation,location,W_age, W_gen,W_job, W_zip):
    def nearest_nyears(x, base=nearest_nyears):
        return int(base * round(float(x)/base))
    A = W_gen * pd.get_dummies(df_users.gender)
    B = W_job * pd.get_dummies(df_users.occupation)
    C = W_age * pd.get_dummies(df_users['age'].apply(nearest_nyears))
    D = W_zip * pd.get_dummies(df_users['zip_code'].apply(nearest_region))

    df_new = pd.concat([A,B,C,D], axis = 1)

    User_info = df_new.iloc[0].copy() #get an example user profile
    User_info.iloc[0:] = 0 #empty profile to fill with input user
    User_info[gender] = 1 * W_gen
    User_info[nearest_nyears(age)] = 1 * W_age
    User_info[nearest_region(location)] = 1 * W_zip
    User_info[occupation] = 1 * W_job
    return(nearest_region(location),nearest_region_nums(location))
