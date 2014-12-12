##
# dotastro hackday experimental code for working with GZ discussion
# data.  calculation of TFIDF metric for terms in discussions orgaized
# by hashtags.  this should serve as an example of how to digest and
# do stuff with the talk data.
#
# mjsottile@gmail.com / dec. 2014
##
import csv
import nltk
import talkparse as tp
import math
from operator import itemgetter, attrgetter, methodcaller

talkparse = tp.TalkParser()
data = talkparse.parsecsv('../../galaxy_zoo_discussions.csv')

# counts for term frequencies
global_terms_in_doc = {}
global_term_freq = {}

## accumulate frequency information for tfidf computation
for entry in data:
    entry_id = entry['discussion_id']

    # an entry id may occur multiple times for a given discussion
    if entry_id not in global_terms_in_doc:
        global_terms_in_doc[entry_id] = {}

    tokens = entry['text']['tokens']
    
    for token in tokens:
        if token in global_terms_in_doc[entry_id]:
            global_terms_in_doc[entry_id][token] += 1
        else:
            global_terms_in_doc[entry_id][token]  = 1

        if token in global_term_freq:
            global_term_freq[token] += 1
        else:
            global_term_freq[token]  = 1

#             
num_docs = len(data)
result = []

tfidfs = {}

### NOTE: make sure to compute tfidf by discussion as the document,
### not each discussion entry as document.
for entry in data:
    entry_id = entry['discussion_id']

    max_freq = 0;

    tokens = entry['text']['tokens']
    
    for token in tokens:
        freq = global_terms_in_doc[entry_id][token]
        if freq > max_freq:
            max_freq = freq
            
    for token in tokens:            
        freq = global_terms_in_doc[entry_id][token]
        idf = math.log(float(1 + num_docs) / float(1 + global_term_freq[token]))
        tfidf = float(freq) / float(max_freq) * float(idf)
        tfidfs[token] = tfidf

# pull out tokens and organize them by hashtag
hashtag_map = {}
for entry in data:
    for hashtag in entry['text']['hashtags']:
        if not hashtag in hashtag_map.keys():
            hashtag_map[hashtag] = []
        hashtag_map[hashtag] = list(set(hashtag_map[hashtag]+entry['text']['tokens']))

# for each hashtag, pull out the set of terms that occur with them
# as well as the TFIDF for each term
for hashtag in hashtag_map.keys():
    words = hashtag_map[hashtag]

    thisdoc = []
    for word in words:
        if word in tfidfs:
            thisdoc.append((word,tfidfs[word]))

    thisdoc = sorted(thisdoc, key=itemgetter(1))

    # debug print
    print "\n\nHASHTAG:"+hashtag+"\n"+str(thisdoc)

# print stuff
for term in tfidfs.keys():
    if tfidfs[term] > 2.0:
        print term+" : "+str(tfidfs[term])
        
