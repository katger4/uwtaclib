# takes in a string of text as its single parameter 
# returns a list of the words in that string.
import re
def extract_words(text):
  word_list = re.split("[^\w']+", text)
  word_list = [i for i in word_list if i != '']
  return word_list

# takes in as a parameter the name of a file containing word sentiment scores (e.g., AFINN-111.csv). The function should return a dictionary whose keys are the words in and whose values are the numeric sentiment scores of those words.
# import os
def load_sentiments(filename):
  word_value = {}
  file = open(filename)
  for i in file:
    key, value = i.split(',')
    word_value[key] = float(value)
  return word_value

# Implement a function text_sentiment() (singular) that takes in two parameters: the text (a string) to analyze, and a dictionary of word sentiment values. The function should return the sentiment of the text, defined as: the sum of the sentiments of the words in the string.
def text_sentiment(text, word_value):
  wordz = extract_words(text)
  wordz_list = []
  # added this step so text_sentiment works
  for i in wordz:
    wordz_list.append(i.lower())
  # for key in wordz:
  #   if key in word_value:
  sentiments = {key: word_value[key] for key in wordz_list if key in word_value}
  return sum(sentiments.values())

# Implement a function load_tweets() that takes in the name of a file containing tweets, and returns a list of objects (dictionaries) representing those tweets.
# These "tweet files" will be structured with one tweet on each line, with that tweet represented as a JSON formatted string 
# entities.hashtags[i].text (the text field from each item in the entries.hashtags list). These are the hashtags that Twitter has extracted from the tweets (so you dont have to!)
import json
def load_tweets(filename):
  file = open(filename)
  some_list = []

  for i in file: 
    tweet = {}
    object = json.loads(i) #is a dictionary
    tweet["created_at"] = object["created_at"] # when the tweet was posted
    tweet["screen_name"] = object["user"]["screen_name"] # (the screen_name value inside the user dictionary): who authored the tweet (attribution is important!)
    tweet["text"] = object["text"] # class = str; the content of the tweet; the part we most care about
    tweet["retweet_count"] = object["retweet_count"] # class = int; how many times the tweet has been retweeted
    tweet["favorite_count"] = object["favorite_count"] # class = int; how many times the tweet has been favorited
    # print(tweet["favorite_count"]) # is all 0's (no favorites)
    tweet["hashtags"] = [] # create an empty list to append things to
    hash = object["entities"]["hashtags"]
    for i in hash:
      txt = i["text"]
      tweet["hashtags"].append(txt) # (the text field from each item in the entries.hashtags list).
    some_list.append(tweet)
    # print(type(tweet["retweet_count"]))

  return some_list

# Implement a function popularity() that takes in the name of a file containing tweets and returns a tuple containing the average number of retweets (in the first entry) and the average number of favorites (in the second entry).
def popularity(filename):
  tweetz = load_tweets(filename) # a list
  # print(tweetz[0]) # tweetz[0] is first tweet dict
  retweets_list = retweet_counts(tweetz) #[]
  # print (retweets_list)
  favorite_list = []
  for i in tweetz:
    favorite_count = i["favorite_count"]
    favorite_list.append(favorite_count)
  # print(favorite_list)
  avg_re = sum(retweets_list)/len(retweets_list)
  # print(avg_re) # 1178.39
  avg_fav = sum(favorite_list)/len(favorite_list)
  the_tuple = (avg_re, avg_fav)

  return the_tuple

##### helper functions
def retweet_counts(the_list):
  retweets_list = []
  for i in the_list:
    retweet_count = i["retweet_count"]
    retweets_list.append(retweet_count)
  return retweets_list

def add_hash(the_list):
  sym_hash = [] # append the '#' to each hashtag string in the list
  for i in the_list:
    sym = i.replace(i,'#'+i)
    sym_hash.append(sym)
  return sym_hash

def frequency(a_list):
  hash_freqs = {} 
  for hash in a_list:
    hash_freqs[hash] = hash_freqs.get(hash, 0) + 1 # for each hashtag in the list, find its current count (could be zero) and add to it
  return hash_freqs

def reverse_sort_reverse(the_tuple_list):
  reverse_tuple_list = [] # create an empty list to append the reversed list to
  for i in the_tuple_list:
    rev = tuple(reversed(i))
    reverse_tuple_list.append(rev)
  reverse_tuple_list.sort(reverse = True) # sort the reversed tuple in descending order (big to small)
  tuple_list = [] # un-reverse the sorted list of tuples
  for i in reverse_tuple_list:
    rev = tuple(reversed(i))
    tuple_list.append(rev)

  return tuple_list
##### end helper functions 

# Implement a function called hashtag_counts() that takes in the name of a file containing tweets and returns a list of tuples, where each tuple contains a hashtag in the data set and the number of times that hashtag was used (in that order). This list itself should be ordered by the frequency, so that most popular hashtags are at the top.
def hashtag_counts(filename):
  tweetz = load_tweets(filename)
  hashtags_list = []
  for i in tweetz:
    # if i["hashtags"] != []:
    hashtags = i["hashtags"]
    hashtags_list.append(hashtags)
  # flat_hash = [hash for lists in hashtags_list for hash in lists]
  flat_hash = [] # "flatten" the list of lists of hashtags into 1 list
  for lists in hashtags_list:
      for hash in lists:
          flat_hash.append(hash)
  sym_hash = add_hash(flat_hash)#[]
  # hashtags_list = sum(hashtags_list, []) # sum over all elements and get just one sum
  hash_freqs = frequency(sym_hash) #{} 

  hash_tup = hash_freqs.items()
  # reverse_tuple_list = [(value,key) for key,value in hash_tup]

  tuple_list = reverse_sort_reverse(hash_tup) #[] 

  return tuple_list

# Implement a function tweet_sentiments() (plural) that takes in two parameters: the name of the tweet data file and the name of a sentiment data file (in that order). This function should return a list of tweet objects (similar to your load_tweets() method, but with one difference: each tweet object should have an additional field (e.g., sentiment) that holds the sentiment of the tweet's text.
def tweet_sentiments(tweet_file, sentiment_file):
  tweet_obj_list = []
  words_values = load_sentiments(sentiment_file)
  tweetz = load_tweets(tweet_file)
  # sent_values = []
  for i in tweetz:
    text = i["text"]
    sent_value = text_sentiment(text, words_values)
    # sent_values.append(sent_value)
    tweet_obj = {}
    tweet_obj['sentiment'] = sent_value # add new key/value pair to empty dict, then copy all other k/v pairs
    tweet_obj["created_at"]= i["created_at"] 
    tweet_obj["screen_name"]= i["screen_name"] 
    tweet_obj["text"]= text
    tweet_obj["retweet_count"] = i["retweet_count"] 
    tweet_obj["favorite_count"] = i["favorite_count"] 
    tweet_obj["hashtags"] = i["hashtags"]

    tweet_obj_list.append(tweet_obj)

  return tweet_obj_list

# Implement a function hashtag_sentiments() that takes as parameters the name of a tweet data file and the name of a sentiment data file. This function should return a list of tuples, where each tuple contains (in order) a hashtag in the data set and the sentiment of that hashtag, defined as: the average sentiment of the tweets that contain that hashtag. This list itself should be ordered by the sentiment, so that most positive hashtags are at the top.

def hashtag_sentiments(tweet_file, sentiment_file, query=None):

  list_of_tuples = []
  # words_values = load_sentiments(sentiment_file)
  # hash_num = hashtag_counts(tweet_file)
  tweetz = tweet_sentiments(tweet_file, sentiment_file) # tweetz is a list of dicts
  # some_dict = {}
  hash_sent = []
  # hash_num_sent = [i + (''.join(i),) for i in hash_num]
  for i in tweetz:
    sent_value = i["sentiment"]
    hash_list = add_hash(i["hashtags"])
    # if i["hashtags"] != []:
    if hash_list != []:
      for i in hash_list:
        hashtag = i
        hash_sent.append((hashtag,sent_value))
  # hs_dict = {}
  from collections import defaultdict
  hs_dict = defaultdict(list)
  for i in hash_sent:
    hs_dict[i[0]].append(i[1])
  hs_dict = dict(hs_dict)
  
  avgDict = {}
  for key,value in hs_dict.items():
    avgDict[key] = sum(value)/float(len(value))

  unsorted_tuple = avgDict.items()
  list_of_tuples = reverse_sort_reverse(unsorted_tuple) #[]
  
  if query == None:
    return list_of_tuples
  else:
    r = re.compile(r'.*'+re.escape(query)+r'.*',re.IGNORECASE)
    filtered_list_of_tuples = []
    for i in list_of_tuples:
      match = r.match(i[0])
      if match:
        filtered_list_of_tuples.append(i)
    return filtered_list_of_tuples

# Implement one last function popular_sentiment() that takes as parameters (again) the name of a tweet data file and the name of a sentiment data file. This function should return the correlation (i.e., Pearson's r) between the sentiment of a tweet and the number of times that tweet was retweeted.
from scipy.stats import pearsonr
def popular_sentiment(tweet_file, sentiment_file):
  tweetz = tweet_sentiments(tweet_file, sentiment_file)

  retweets_list = retweet_counts(tweetz)
  sentiments_list = []
  for i in tweetz:
    sentiment = i["sentiment"]
    sentiments_list.append(sentiment)

  correlation = pearsonr(sentiments_list, retweets_list)
  return correlation[0]
####################################
## DO NOT EDIT BELOW THIS POINT!! ##
## #################################

# Run the method specified by the command-line
if __name__ == '__main__':
  #for parsing and friendly command-line error messages
  import argparse 
  parser = argparse.ArgumentParser(description="Analyze Tweets")
  subparsers = parser.add_subparsers(description="commands", dest='cmd')
  subparsers.add_parser('load_tweets', help="load tweets from file").add_argument('filename')
  subparsers.add_parser('popularity', help="show average popularity of tweet file").add_argument('filename')
  subparsers.add_parser('extract_words', help="show list of words from text").add_argument(dest='text', nargs='+')
  subparsers.add_parser('load_sentiments', help="load word sentiment file").add_argument('filename')

  sentiment_parser = subparsers.add_parser('sentiment', help="show sentiment of data. Must include either -f (file) or -t (text) flags.")
  sentiment_parser.add_argument('-f', help="tweets file to analyze", dest='tweets')
  sentiment_parser.add_argument('-t', help="text to analyze", dest='text', nargs='+')
  sentiment_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)

  subparsers.add_parser('hashtag_counts', help="show frequency of hashtags in tweet file").add_argument('filename')

  hashtag_parser = subparsers.add_parser('hashtag', help="show sentiment of hashtags.")
  hashtag_parser.add_argument('-f', help="tweets file to analyze", dest='tweets', required=True)
  hashtag_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)
  hashtag_parser.add_argument('-q', help="hashtag to analyze", dest="query", default=None)

  correlation_parser = subparsers.add_parser('correlation', help="show correlation between popularity and sentiment of tweets")  
  correlation_parser.add_argument('-f', help="tweets file to analyze", dest='tweets', required=True)
  correlation_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)

  args = parser.parse_args()

  try:
    if args.text:
      args.text = ' '.join(args.text) #combine text args
  except:
    pass

  #print(args) #for debugging

  # call function based on command given
  if args.cmd == 'load_tweets':
    tweets = load_tweets(args.filename)
    for tweet in tweets:
      print(tweet)

  elif args.cmd == 'popularity':
    print(popularity(args.filename))

  elif args.cmd == 'hashtag_counts':
    for key,value in hashtag_counts(args.filename):
      print(str(key),":",value)

  elif args.cmd == 'extract_words':
    print(extract_words(args.text))

  elif args.cmd == 'load_sentiments':
    for key,value in sorted(load_sentiments(args.filename).items()):
      print(key,value)

  elif args.cmd == 'sentiment':
    if args.tweets == None: #no file, do text
      sentiment = text_sentiment(args.text, load_sentiments(args.sentiments))
      print('"'+args.text+'":', sentiment)
    elif args.text == None: #no text, do file
      rated_tweets = tweet_sentiments(args.tweets, args.sentiments)
      for tweet in rated_tweets:
        print(tweet)
    else:
      print("Must include -f (tweet filename) or -t (text) flags to calculate sentiment.")

  elif args.cmd == 'hashtag':
    if(args.query == None): #split to test optional param
      rated_tags = hashtag_sentiments(args.tweets, args.sentiments)
    else:
      rated_tags = hashtag_sentiments(args.tweets, args.sentiments, args.query)
    for key,value in rated_tags:
      print(str(key),":",value)

  elif args.cmd == 'correlation':
    print("Correlation between popularity and sentiment: r="+str(popular_sentiment(args.tweets, args.sentiments)))