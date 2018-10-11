

def get_recommendations(gender,age,occupation,location,W_gen,W_age,W_job,W_zip,sim_users,n_movies,min_rating,genres): #,W_gen,W_job,W_zip, genres,age,location,gender,occupation

    #genres = ['Action','Adventure']
    #n_users = 10
    #n_top_movies = 3
    nearest_nyears = 5
    U_sim = 0.7 #% similarity cut for onehot encoded filter

    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    import pandas as pd
    from sklearn import preprocessing
    import Attribute_tuning as at
    data_cols = ['user_id', 'item_id', 'rating', 'timestamp']
    item_cols = ['movie_id','movie_title','release_date', 'video_release_date','IMDb_URL','unknown','Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War' ,'Western']
    user_cols = ['user_id','age','gender','occupation','zip_code']

    #importing the data files onto dataframes
    df_users = pd.read_csv('u.user', sep='|', names=user_cols, encoding='latin-1')
    df_item = pd.read_csv('u.item', sep='|', names=item_cols, encoding='latin-1')
    df_data = pd.read_csv('u.data', sep='\t', names=data_cols, encoding='latin-1')
    df_occupation = pd.read_csv('Occupation_embeddings.csv', names=['embedding','occupation'],sep='\t', encoding='latin-1')
    df_data = df_data.drop(['timestamp'], axis=1)
    df_predicted_ratings = pd.read_csv('predicted_ratings.csv', sep='\t', encoding='latin-1')
    df_predicted_ratings = df_predicted_ratings.drop(['Unnamed: 0'], axis=1)
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    min_max_scaler_age = preprocessing.MinMaxScaler(feature_range=(1, 101))
    min_max_scaler_rating = preprocessing.MinMaxScaler(feature_range=(1, 5))

    User_info = df_users.iloc[0].copy() #get an example user profile
    User_info.iloc[0:] = 0 #empty profile to fill with input user
    User_info['gender'] = gender
    User_info['age'] = age
    User_info['occupation'] = occupation
    User_info['zip_code'] = location

    df_users = df_users.append(User_info)
    #replace occupations with embedding
    for index, column in df_occupation.iterrows():
        df_users = df_users.replace({'occupation' : { df_occupation.iloc[index,1] : df_occupation.iloc[index,0]}})

    #normalize features for USER x n_factors
    df_users.age = df_users[['age']]/100.00
    df_users.occupation = min_max_scaler.fit_transform(df_users[['occupation']])

    #covert zip_code to float and for those that entered an invalid zip, change to 0
    df_users.zip_code = pd.to_numeric(df_users.zip_code, downcast='float', errors='coerce').fillna(0)
    df_users.zip_code = min_max_scaler.fit_transform(df_users[['zip_code']])
    df_users.gender = df_users.gender.map({'F': 1, 'M': 0.699}) #word2vec

    #USER x MOVIE
    #replace the predicted_ratings with have known 100,000 ratings to have full user matrix
    df_data_sort = df_data.sort_values('user_id', ascending=True)#.head()

    #make sure ratings are scaled between 1-5
    df_predicted_ratings.rating = min_max_scaler_rating.fit_transform(df_predicted_ratings[['rating']])
    #Get rid of bias in movie recommender: Adjust movie ratings according to user's rating patterns compared to the average.

    #pkr = previously_known_rating
    df_pkr = pd.concat([df_data_sort,df_predicted_ratings])
    df_full_matrix = pd.concat([df_pkr.drop_duplicates(subset=['user_id', 'item_id'],keep=False),df_data_sort]).sort_values('user_id', ascending=True)

    #User: r = np.random.randint(0,943), for random user df_users.iloc[r,1:] to use a random user from dataset

    Input_user = df_users.iloc[-1,1:]

    x = at.tuned_users(nearest_nyears,U_sim,age,gender,occupation,location,W_age, W_gen,W_job, W_zip) #one-hot encoded users that satisfy the input user's applied weights (to attributes)
    del at

    sim=[]
    for i in range(len(x)): #finds the similarity for the Word2Vec users from the set of one-hot encoded user profiles that satisfy the above condition
        sim.append(cosine_similarity([Input_user], [df_users.iloc[x[i],1:]]))

    user = np.squeeze(np.argsort(sim, axis=0)[-sim_users:]) #n users with the highest similarity to input user
    user_accuracy = 100*np.sort(np.squeeze(sim))[-sim_users]
    user = x[user]+1 #to get the correct indexing
    df_users.iloc[user]
    # Check that users seem reasonably similar:
    #df_users.loc[df_users['user_id'].isin(user)]#sort movie IDs/recommendations by user ID

    #All movie IDs/recommendations from top X users
    df_movies = df_full_matrix.loc[df_full_matrix['user_id'].isin(user)]

    #top user matrix & demographic breakdowns
    df_top_10 = df_users.loc[df_users['user_id'].isin(user)]

    Female = df_top_10.gender[df_top_10.gender == 1.0].count()/len(user) #female is 1, while male is 0.699 for Word2Vec
    df_top_10.gender[df_top_10.gender == 1.0].count()
    tech_job = df_top_10.occupation[df_top_10.occupation > 0.434].count()/len(user) #this is the value cut for technical profession
    location = df_top_10.zip_code[df_top_10.zip_code > 0.800].count()/len(user) #Westcoast zip_codes are greater than 80000 (0.8 when normalized)
    Age = df_top_10.age[df_top_10.age < 0.30].count()/len(user) #Less than the age of 30

    #average ratings for all movies from top users
    df_top_movies=df_movies.groupby('item_id', as_index=False)['rating'].mean().sort_values('rating', ascending=False)

    #minimum movie rating of 3 stars
    top_movies_list = df_top_movies.rating[df_top_movies.rating > min_rating].index.tolist()
    idx = top_movies_list[::]

    #classify genre
    df_genre = df_item.iloc[:,6:25].iloc[idx[::]]
    g = np.unique(np.where(df_genre[genres] == 1)[0])
    top_movies = df_item['movie_title'].loc[idx[::]].iloc[list(g)][0:n_movies].values
    ratings = np.round(df_top_movies['rating'].loc[idx[::]].iloc[list(g)][0:n_movies].values,2)

    return(np.dstack((top_movies,ratings))[0],ratings,str(np.round(user_accuracy,2)),str(np.round(Female,2)*100),str(np.round(Age,2)*100), str(np.round(tech_job,2)*100),str(np.round(location,2)*100))

