from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics import mean_squared_error as rmse
from scipy.sparse.linalg import svds
from scipy.sparse import coo_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import sys
import logging
import scipy.sparse as sps

logging.basicConfig(level = logging.DEBUG)

gender = 'F'
occupation = 'scientist'
age = 25
location = 'CA'
if location=='CA'or'OR' or 'HI' or 'WA' or 'AK':
    location = '90000'

#int(location[0])
genre = 'Documentary'
genre1 = 'Adventure'

W_age = 0.0
W_gen = 0.25
W_job = 1.00
W_zip = 0.00

data_cols = ['user_id', 'item_id', 'rating', 'timestamp']
item_cols = ['movie_id','movie_title','release_date', 'video_release_date','IMDb_URL','unknown','Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance ','Sci-Fi','Thriller','War' ,'Western']
user_cols = ['user_id','age','gender','occupation','zip_code']

#importing the data files onto dataframes
df_users = pd.read_csv('u.user', sep='|', names=user_cols, encoding='latin-1')
df_item = pd.read_csv('u.item', sep='|', names=item_cols, encoding='latin-1')
df_data = pd.read_csv('u.data', sep='\t', names=data_cols, encoding='latin-1')
df_data = df_data.drop(['timestamp'], axis=1)
df_predicted_ratings = pd.read_csv('predicted_ratings.csv', sep='\t', encoding='latin-1')
df_predicted_ratings = df_predicted_ratings.drop(['Unnamed: 0'], axis=1)

def nearest_5years(x, base=5):
    return int(base * round(float(x)/base))

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

#logging.info(nearest_region(location))

A = W_gen * pd.get_dummies(df_users.gender)
B = W_job * pd.get_dummies(df_users.occupation)
C = W_age * pd.get_dummies(df_users['age'].apply(nearest_5years))
D = W_zip * pd.get_dummies(df_users['zip_code'].apply(nearest_region))

df_new = pd.concat([A,B,C,D], axis = 1)
#User information
User_info = df_new.iloc[0].copy() #get an example user profile
User_info.iloc[0:] = 0 #empty profile to fill with input user
User_info[gender] = 1 * W_gen
User_info[nearest_5years(age)] = 1 * W_age
User_info[nearest_region(location)] = 1 * W_zip
User_info[occupation] = 1 * W_job
User_info.head(50)

#r = np.random.randint(0,943), for random user df_new.iloc[r]
sim=[]
for i in range(len(df_new)): #finds the
    sim.append(cosine_similarity([User_info], [df_new.iloc[i]]))

user = np.squeeze(np.argsort(sim, axis=0)[-100:])# 20 users with the highest similarity to input user
user = user+1 #to get the correct indexing
user
df_data_sort = df_data.sort_values('user_id', ascending=True)#.head()
#sort movie IDs/recommendations by user ID
#correct index
df_data_sort.head()#shape
df_predicted_ratings.head()#shape
#pkr = previously_known_rating
df_pkr = pd.concat([df_data_sort,df_predicted_ratings])
df_full_matrix = pd.concat([df_pkr.drop_duplicates(subset=['user_id', 'item_id'],keep=False),df_data_sort]).sort_values('user_id', ascending=True)

df_full_matrix.shape
#943*1682
#include way to get rid of bias in movie recommender



#All movie IDs/recommendations from top 20 users
df_top_movies = df_full_matrix.loc[df_full_matrix['user_id'].isin(user)]
#average ratings for all movies from top users
df_top_movies=df_top_movies.groupby('item_id', as_index=False)['rating'].mean().sort_values('rating', ascending=False)
top_movies_list = df_top_movies['item_id'][0:100].index.tolist()
idx = top_movies_list[::]

df_genre = df_item.iloc[:,6:25].iloc[idx[::]]
g = np.where((df_genre[genre] == 1) | (df_genre[genre1] == 1))[0]
logging.debug(df_item['movie_title'].loc[idx[::]].iloc[list(g)][0:3])
