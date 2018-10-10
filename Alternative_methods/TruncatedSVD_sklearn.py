'''
Experimented with sklearn's Dimensionality reduction using truncated SVD (aka LSA, latent semantic analysis).
This transformer performs linear dimensionality reduction by means of truncated singular value decomposition (SVD). Contrary to PCA, this estimator does not center the data before computing the singular value decomposition. This means it can work with scipy.sparse matrices efficiently.
Inspiration taken from: https://www.kaggle.com/robindong/collaborative-filtering-to-recommend-books
'''  
import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics import mean_squared_error as rmse
from scipy.sparse.linalg import svds
from scipy.sparse import coo_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

data_cols = ['user_id', 'item_id', 'rating', 'timestamp']
item_cols = ['movie_id','movie_title','release_date', 'video_release_date','IMDb_URL','unknown','Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance ','Sci-Fi','Thriller','War' ,'Western']
user_cols = ['user_id','age','gender','occupation','zip_code']

#importing the data files onto dataframes
df_users = pd.read_csv('u.user', sep='|', names=user_cols, encoding='latin-1')
df_item = pd.read_csv('u.item', sep='|', names=item_cols, encoding='latin-1')
df_data = pd.read_csv('u.data', sep='\t', names=data_cols, encoding='latin-1')

df_users.head(5)
df_item.head(5)
df_data.head(5)

n_users = df_data.user_id.unique().shape[0] #or len(df['user_id'].unique())
n_items = df_data.item_id.unique().shape[0]

# Use Coordinate Matrix of scipy to create sparse matrix for books and users
matrix = coo_matrix((df_data.user_id.astype(float), (df_data.item_id, df_data.rating)))

print(matrix)
sparsity=round(1.0-len(df_data)/float(n_users*n_items),3)
print('The sparsity of the MovieLens 100K-dataset is '+str(sparsity*100) + '%')

svd = TruncatedSVD(n_components=3, n_iter=4, random_state=0) #(n_components=2, algorithm=’randomized’, n_iter=5, random_state=None, tol=0.0)
sigma = svd.fit_transform(matrix)
print(svd.explained_variance_ratio_)
print(svd.explained_variance_ratio_.sum())
print(sigma.shape)

#every row of this matrix represents a vectorized latent factor
# Create similarities for every movie
udf = pd.DataFrame(cosine_similarity(sigma))
udf.head()

associated_movies = udf.iloc[968].sort_values(ascending = False)

idx = associated_movies.index[:100]
print(df_item['movie_title'][idx])
