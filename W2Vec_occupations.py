import gensim.models.keyedvectors as word2vec
import pandas as pd

# Load Google's pre-trained Word2Vec model.
model = word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin', binary=True)

df_occupation = pd.read_csv('u.occupation', sep='\t', names=['occupation'], encoding='latin-1')
df_occupation = df_occupation.values


vec=[]
for i in range(len(df_occupation)):
    vec.append(model.similarity(df_occupation[i][0], 'scientist'))

df_vec = pd.DataFrame(df_occupation, vec, columns=['occupation'])
df_vec.to_csv('Occupation_embeddings.csv', sep='\t', encoding='utf-8')
