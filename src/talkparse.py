#
# Code for parsing talk forum data into something that can be processed further
# and/or used by a bot.
#
# 12/9/2014: mjsottile@gmail.com
#
import nltk
import csv

class TalkParser(object):
    def __init__(self):
        self.stopset = set(nltk.corpus.stopwords.words('english'))

    def parsecsv(self, fname, upperbound = None):
        """Parse CSV file containing talk data.  This should be replaceable
           with something that talks to the backing database containing the
           actual data.
        """
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

        # parse hashtags with simple string split
        words = text.split()
        for word in words:
            if word[0] == '#':
                hashtags.append(word)

        results = {}
                
        results['hashtags'] = hashtags

        tokens = nltk.WordPunctTokenizer().tokenize(text)
        filtered_tokens = [t for t in tokens if not t in self.stopset]

        results['tokens'] = filtered_tokens

        return results
    
