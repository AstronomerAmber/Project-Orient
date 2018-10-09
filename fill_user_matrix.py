
'''
Filling in a MovieLens Movie x User Matrix using keras
Inspired by:
https://nipunbatra.github.io/blog/2017/recommend-keras.html
'''

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import keras
from IPython.display import SVG
from keras.optimizers import Adam
from keras.layers import merge
from keras.utils.vis_utils import model_to_dot
import matplotlib.pyplot as plt
from sklearn import preprocessing

%config InlineBackend.figure_format = 'svg'

data_cols = ['user_id', 'item_id', 'rating', 'timestamp']
df_data = pd.read_csv('u.data', sep='\t', names=data_cols, encoding='latin-1')
df_data = df_data.drop(['timestamp'], axis=1)

#make sure ratings are scaled between 1-5
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(1, 5))
for n in range(943):
    df_data.loc[df_data['user_id'] == 1+n,['rating']] = min_max_scaler.fit_transform(df_data.loc[df_data['user_id'] == 1+n,['rating']])

df_data.user_id = df_data.user_id.astype('category').cat.codes.values
df_data.item_id = df_data.item_id.astype('category').cat.codes.values
#X_train = pd.read_csv('ua.base', sep='\t', names=data_cols, encoding='latin-1')
#X_test = pd.read_csv('ua.test', sep='\t', names=data_cols, encoding='latin-1')
#test data has 10 ratings for each user^

X_train, X_test = train_test_split(df_data, test_size=0.2)
n_users, n_movies = len(df_data.user_id.unique()), len(df_data.item_id.unique())
n_latent_factors = 3

#X_train.head()
movie_input = keras.layers.Input(shape=[1],name='Item')
movie_embedding = keras.layers.Embedding(n_movies + 1, n_latent_factors, name='Movie-Embedding')(movie_input)
movie_vec = keras.layers.Flatten(name='FlattenMovies')(movie_embedding)

user_input = keras.layers.Input(shape=[1],name='User')
user_embedding = keras.layers.Embedding(n_users + 1, n_latent_factors,name='User-Embedding')(user_input)
user_vec = keras.layers.Flatten(name='FlattenUsers')(user_embedding)

prod = keras.layers.dot([movie_vec, user_vec], axes = 1)

#take the dot product of the user . item embeddings to obtain the rating.

model = keras.Model([user_input, movie_input], prod)
model.compile('adam', 'mean_squared_error')
model.summary()

history = model.fit([X_train.user_id, X_train.item_id], X_train.rating, epochs=100, verbose=0)
pd.Series(history.history['loss']).plot(logy=True)
#plt.xlabel("Epoch")
#plt.ylabel("Train Error")
#plt.show()

y_hat = np.round(model.predict([X_test.user_id, X_test.item_id]),0)
y_true = X_test.rating
n_movies = np.arange(1,1683,1)
n_users = np.arange(1,944,1)
user_movie_matrixA = np.repeat(n_users, len(n_movies))
user_movie_matrixB = np.tile(n_movies, len(n_users))
user_movie_matrix = np.array([user_movie_matrixA,user_movie_matrixB])

all_rating = model.predict([user_movie_matrixA[::],user_movie_matrixB[::]])

df_users = pd.DataFrame(user_movie_matrixA)
df_movies = pd.DataFrame(user_movie_matrixB)
df_ratings = pd.DataFrame(all_rating)

df_all_rate = pd.concat([df_users,df_movies,df_ratings],axis=1)
df_all_rate.columns = ['user_id', 'item_id','rating']
#df_all_rate.head(3)

MAE = mean_absolute_error(y_true, y_hat)
RMSE = mean_squared_error(y_true, y_hat)

#compared to using MAE of 0.737 from SVD, which performed better than KNN at MAE 0.774
movie_embedding_learnt = model.get_layer(name='Movie-Embedding').get_weights()[0]
#pd.DataFrame(movie_embedding_learnt).describe()
user_embedding_learnt = model.get_layer(name='User-Embedding').get_weights()[0]
#pd.DataFrame(user_embedding_learnt).describe()

#save pandas DataFrame
df_all_rate.to_csv('predicted_ratings.csv', sep='\t', encoding='utf-8')
