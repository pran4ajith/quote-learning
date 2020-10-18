from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
import numpy as np

'''
This function loads the GloVe word2vec model, pre-processes the
quotes database and apply the model to generate corresponding
word embeddings. Only used for processing the dataset.
'''
# load the Stanford GloVe model
filename = 'resources/models/glove.6B.50d.txt.word2vec'
word2vec_model = KeyedVectors.load_word2vec_format(filename, binary=False)

# Path of the quotes database
quote_path = "data/quotes.csv"
df = pd.read_csv(quote_path, names=['Quote', 'Author', 'Tags'], usecols=range(0,3))

df = df[['Quote', 'Tags']]
df.drop_duplicates(subset='Quote', inplace=True)
# df['connect'] = df['Tags'].apply(lambda x: " ".join(x))
print('Processing...')

def pre_process(text):
    if(isinstance(text, str)):
        text = re.sub(r'[^A-Za-z-\n ]|(misattributed\S+)|(from\S+)|(attributed\S+)', '', text.lower().strip())
        text = re.sub(r'[-]', ' ', text)
        text = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        text = [word for word in text if word not in stop_words]
        return text
    else:
        return ['NA']

df['filtered'] = df['Quote'].apply(pre_process)
print(df['filtered'].head())

# Filtering out words not present in the word2vec model vocabulary we use
def filter_words(words):
    # remove out-of-vocabulary words by checking with the word2vec model vocabulary
    words = [word for word in words if word in word2vec_model.vocab]
    if len(words) >= 1:
        return words
    else:
        return np.nan

df['filtered'] = df['filtered'].apply(filter_words)
print(df['filtered'].head())

df.to_csv('quote_model/quote_v3_quotes_trained_word2vec.csv')