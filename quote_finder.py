from gensim.models import KeyedVectors

import image_read as image_read

import pandas as pd
import re
import numpy as np
from ast import literal_eval

'''
This class receives the image,
performs the similarity and recommends the quotes
'''

class QuoteFinder:
    def __init__(self, path):
        self.path = path
        #################### Loading word2vec model
        filename = 'resources/model/glove.6B.50d.txt.word2vec'
        self.word2vec_model = KeyedVectors.load_word2vec_format(filename, binary=False)
    
    def find_quote(self):
        #################### Loading the quote database
        quote_path = "resources/quote_model/quote_v3_quotes_trained_word2vec.csv"
        quote_df = pd.read_csv(quote_path)

        quote_df['filtered'].replace('', np.nan, inplace=True)
        # print(quote_df[quote_df.isna().any(axis=1)])
        quote_df.dropna(inplace=True)
        quote_df['filtered'] = quote_df['filtered'].apply(lambda x: literal_eval(x))


        #################### Reading google API output and extracting the image annotations
        image_labels = image_read.im_read(self.path)
        # print(image_labels)

        #################### Calculating similarity
        similarity_df = self.__similarity(quote_df, image_labels)

        return similarity_df['Quote'].head(8).tolist()

    def __similarity(self, quote_df, im_filtered):
        if(im_filtered):
            quote_df['new'] = quote_df['filtered'].apply(lambda x: self.word2vec_model.n_similarity(x, im_filtered))
        else:
            print("failed")
        new_quote = quote_df.sort_values(by=['new'], ascending=False)
        return new_quote
    


