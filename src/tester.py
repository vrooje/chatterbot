import csv
import nltk
import talkparse as tp

talkparse = tp.TalkParser()
print talkparse.parsecsv('../galaxy_zoo_discussions.csv',upperbound=10)
