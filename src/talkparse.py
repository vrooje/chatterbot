#
# Code for parsing talk forum data into something that can be processed further
# and/or used by a bot.
#
# 12/9/2014: mjsottile@gmail.com
#
import nltk
import csv
import sys

class TalkParser(object):
    def __init__(self):
        self.stopset = set(nltk.corpus.stopwords.words('english'))

    def parsecsv(self, fname, upperbound = None):
        """Parse CSV file containing talk data.  This should be replaceable
           with something that talks to the backing database containing the
           actual data.
        """
        csv.field_size_limit(sys.maxsize)

        with open(fname, 'r') as csvfile:
            talkreader = csv.reader(csvfile)

            rownum = 0
            header = []
            results = []
            
            for row in talkreader:
                result = {}
                if rownum == 0:
                    header = row
                elif rownum > upperbound:
                    break
                else:
                    for i,column in enumerate(header):
                        result[column] = row[i]
                        
                    result['text'] = self.parsebody(result['body'])

                    results.append(result)
                rownum += 1
            return results
        
    def parsebody(self, text):
        """Parse the body of a talk comment.  Hashtags are identified, and then
           the text is tokenized and stopwords are removed.
        """
        hashtags = []
        tokens_no_hashtags = []

        # tokenize the text, all lowercase
        tokens = nltk.WordPunctTokenizer().tokenize(text.lower())

        # assumption: None will only occur as the tail of the second list.
        skip_next = False
        for (t1,t2) in zip(tokens,tokens[1:]+[None]):
            if skip_next:
                skip_next = False
                continue
            
            if t2 is None:
                tokens_no_hashtags.append(t1)
            elif t1 == "#":
                hashtags.append(t2)
                skip_next = True
            else:
                tokens_no_hashtags.append(t1)
        
        filtered_tokens = [t for t in tokens_no_hashtags if not t in self.stopset]

        results = {'hashtags':hashtags, 'tokens': filtered_tokens}

        return results
    
