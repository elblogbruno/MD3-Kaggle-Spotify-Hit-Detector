from src.dataset_utils import *
import nltk
import os

from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

def generate_nlp_dataset():
       # we do this so we don't need to generate the same csv all the time 
       # it takes lot of tie to do so.
       if os.path.isfile('data/dataset_full_token.csv'):
              return load_dataset('data/dataset_full_token.csv')
       else:
              columns_to_drop  = ['uri']

              dataset_full = get_full_dataset(columns_to_drop=columns_to_drop)

              def count_hits(artist):
                     return len(dataset_full[(dataset_full['artist'] == artist) & (dataset_full['target'] == 1)])

              def count_flops(artist):
                     return len(dataset_full[(dataset_full['artist'] == artist) & (dataset_full['target'] == 0)])
                     

              # artists = dataset_full['artist'].unique()
              # print("NULL ARTIST: " + str(dataset_full['artist'].isnull().sum()))

              # print('artist part')
              # artists = dataset_full['artist'].unique()
              
              # print(artists)
              # # add new empty column at start of dataset
              # dataset_full.insert(0, 'has_hits', '')
              # # for each artist, count the number of hits and flops
              # for artist in artists:
              #        if count_hits(artist) <= count_flops(artist) and count_hits(artist) > 5:
              #               # print("Artist {} has less than 10 hits".format(artist))
              #               dataset_full['has_hits'][dataset_full['artist'] == artist] = 0
              #        else:
              #               # print("Artist {} has more than 10 hits".format(artist))
              #               dataset_full['has_hits'][dataset_full['artist'] == artist] = 1

              # print("NLP Part")
              # tokens = dataset_full['track'].values

              # print(len(tokens))

              # freq = nltk.FreqDist(tokens)

              # freq = freq.most_common(10)

              # # plot the most common tokens
              # # freq.plot(10, cumulative=False)
              
              # def decide(x, freq):
              #        # print(x)
              #        for word in x:
              #               if word in freq:
              #                      return 1
              #        return 0


              # dataset_full.insert(0, 'top10', '')
              # # add a new column with a 1 if the track name is in the top 10 most common words
              # for i in range(len(dataset_full)):
              #        dataset_full['top10'][i] = decide(dataset_full['track'][i].split(), freq)
                     
              # # dataset_full['top10'] = dataset_full['track'].apply(lambda x: decide(x, freq))

              # dataset_full.drop(['track', 'artist'], axis=1, inplace=True)      

              # dataset_full.to_csv('data/dataset_full_token.csv')

              # print(dataset_full.isnull().sum())
              
              # count vectorizer
              # vectorizer = CountVectorizer(analyzer='word', tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
              # dataset_full_counts = vectorizer.fit_transform(dataset_full['track'])
              # print(dataset_full_counts)
              # print(vectorizer.get_feature_names_out())

              # tfidf_transformer = TfidfTransformer()
              # dataset_full_tfidf = tfidf_transformer.fit_transform(dataset_full_counts)
              # print(dataset_full_tfidf)
              # print(dataset_full_tfidf.shape)

              # settings that you use for count vectorizer will go here 
              tfidf_vectorizer=TfidfVectorizer(use_idf=True) 
              
              # just send in all your docs here 
              tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(dataset_full['track'].values)

              # get the first vector out (for the first document) 
              first_vector_tfidfvectorizer=tfidf_vectorizer_vectors[0] 
              
              dataset_full.insert(0, 'tfidf', '')
              # place tf-idf values in dataset-full as a column
              dataset_full['tfidf'] = first_vector_tfidfvectorizer.getnnz()

              dataset_full.drop(['track', 'artist'], axis=1, inplace=True)     

              return dataset_full