from src.dataset_utils import *

def generate_nlp_dataset():
       columns_to_drop  = ['uri']

       dataset_full = get_full_dataset(columns_to_drop=columns_to_drop)

       def count_hits(artist):
              return len(dataset_full[(dataset_full['artist'] == artist) & (dataset_full['target'] == 1)])

       def count_flops(artist):
              return len(dataset_full[(dataset_full['artist'] == artist) & (dataset_full['target'] == 0)])
              

       artists = dataset_full['artist'].unique()
       print(artists)
       # add new empty column at start of dataset
       dataset_full.insert(0, 'has_hits', '')
       # for each artist, count the number of hits and flops
       for artist in artists:
              # print(artist)
              # check if artitst is float
              if type(artist) == float:
                     artist = str(artist)
                     artist = 'unknown'

              if count_hits(artist) <= count_flops(artist):
                     # print("Artist {} has less than 10 hits".format(artist))
                     dataset_full['has_hits'][dataset_full['artist'] == artist] = 0
              else:
                     # print("Artist {} has more than 10 hits".format(artist))
                     dataset_full['has_hits'][dataset_full['artist'] == artist] = 1
              

       dataset_full.to_csv('dataset_full_token.csv')

       return dataset_full