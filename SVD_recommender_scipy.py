'''
Using scipy to build a Singular Value Decomposition recommender system using Scipy

Experimented with building a recommendation system using Model-based collaborative filtering is based on matrix factorization where using scipy's singular value decomposition (SVD) to factorize the matrix.

Inspired by: Agnes Johannsdottir
https://cambridgespark.com/content/tutorials/implementing-your-own-recommender-systems-in-Python/index.html
'''
#MovieLens dataset
#100K movie ratings
#943 users
#1682 movies

import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics import mean_squared_error as rmse
from scipy.sparse.linalg import svds

header = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep='\t', names=header)
#df.head(5)
n_users = df.user_id.unique().shape[0] #or len(df['user_id'].unique())
n_items = df.item_id.unique().shape[0]
# Lets look at the number of book_id and user_id

#print('Number of users = ' + str(n_users) + ' | Number of movies = ' + str(n_items))

#Item-Item Collaborative Filtering: “Users who liked this item also liked …”
#User-Item Collaborative Filtering: “Users who are similar to you also liked …”

X_train, X_test = ms.train_test_split(df, test_size=0.25,random_state=0) #X_train, X_test, y_train, y_test = ms.train_test_split(features, targets,random_state=0)
#creating training and testing user-item matrix

sparsity=round(1.0-len(df)/float(n_users*n_items),3)
#print('The sparsity level of MovieLens100K is '+str(sparsity*100) + '%')

#Create two user-item matrices, one for training and another for testing
train_data_matrix = np.zeros((n_users, n_items))
for line in X_train.itertuples():
    train_data_matrix[line[1]-1, line[2]-1] = line[3]

test_data_matrix = np.zeros((n_users, n_items))
for line in X_test.itertuples():
    test_data_matrix[line[1]-1, line[2]-1] = line[3]

#get SVD components from train matrix. Choose k.
u, s, vt = svds(train_data_matrix, k = 20)
#X_train.shape
s_diag_matrix=np.diag(s)
X_pred = np.dot(np.dot(u, s_diag_matrix), vt)

#evaluate with mean squared eroor
#print('User-based CF MSE: ' + str(rmse(X_pred, test_data_matrix)))
