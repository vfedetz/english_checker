import urllib2, functools, math

# Input: string filename of the file to load
# Output: unformatted text
def loadText(filename):
    file = open(filename,'r')
    text = file.read()
    onlyletters = filter(lambda x: x.isalpha(), text)
    onlylower = onlyletters.lower()
    return onlylower

def letterNGrams(msg, n):
   return [msg[i:i+n] for i in range(len(msg) - (n-1))]

# need to do this when the file is space delimited
class OneGramDistSPACES(dict):
   def __init__(self, filename):
      self.gramCount = 0

      for line in open(filename):
         (word, count) = line[:-1].split(' ')
         self[word] = int(count)
         self.gramCount += self[word]

   def __call__(self, key):
      if key in self:
         return float(self[key]) / self.gramCount
      else:
         return 1.0 / (self.gramCount * 10**(len(key)-2))

# class used to load in n-gram files and counts
class OneGramDist(dict):
   def __init__(self, filename):
      self.gramCount = 0

      for line in open(filename):
         (word, count) = line[:-1].split('\t')
         self[word] = int(count)
         self.gramCount += self[word]

   def __call__(self, key):
      if key in self:
         return float(self[key]) / self.gramCount
      else:
         return 1.0 / (self.gramCount * 10**(len(key)-2))

def nGramStringProb(ngram_counts, obs_ngrams):
    ans = 0
    for ngram in obs_ngrams:
        if ngram in ngram_counts:
            ans = ans + math.log10(ngram_counts[ngram])
    return ans

# Load up the gram count files
top_1k_words = loadText('1000_most_common_words.txt')
bigram_counts = OneGramDist('eng_bigrams.txt')
trigram_counts = OneGramDist('eng_trigrams.txt')
quadgram_counts = OneGramDistSPACES('eng_quadgrams.txt')

# Main function
# seems to return around 22-25 for english
def isEnglish(text):
    score = 0
    obs_bigrams = letterNGrams(text, 2)
    obs_trigrams = letterNGrams(text, 3)
    obs_quadgrams = letterNGrams(text, 4)
    
    bigram_score = nGramStringProb(bigram_counts, obs_bigrams)
    trigram_score = nGramStringProb(trigram_counts, obs_trigrams)
    quadgram_score = nGramStringProb(quadgram_counts, obs_quadgrams)
    
    # print bigram_score/len(text)
    # print trigram_score/len(text)
    # print quadgram_score/len(text)
    score = (bigram_score + trigram_score + quadgram_score) / len(text)
    
    return score
    
# # TESTING
# text = loadText('some_eng')
# print text
# print isEnglish(text)

# import random, string
# count = 0
# while count < 10:
#     arr = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10000))
#     #print arr
#     print "Score of random", isEnglish(arr)
#     count=count+1
