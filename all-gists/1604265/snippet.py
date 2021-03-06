
auth = OAuthHandler(CLIENT_ID, CLIENT_SECRET, CALLBACK)
auth.set_access_token(ACCESS_TOKEN)
api = API(auth)


venue = api.venues(id='4bd47eeb5631c9b69672a230')
stopwords = nltk.corpus.stopwords.words('portuguese')
tokenizer = RegexpTokenizer("[\w’]+", flags=re.UNICODE)


def freq(word, doc):
    return doc.count(word)


def word_count(doc):
    return len(doc)


def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))


def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count


def idf(word, list_of_docs):
    return math.log(len(list_of_docs) /
            float(num_docs_containing(word, list_of_docs)))


#Compute the frequency for each term.
vocabulary = []
docs = {}
all_tips = []
for tip in (venue.tips()):
    tokens = tokenizer.tokenize(tip.text)

    bi_tokens = bigrams(tokens)
    tri_tokens = trigrams(tokens)
    tokens = [token.lower() for token in tokens if len(token) > 2]
    tokens = [token for token in tokens if token not in stopwords]

    bi_tokens = [' '.join(token).lower() for token in bi_tokens]
    bi_tokens = [token for token in bi_tokens if token not in stopwords]

    tri_tokens = [' '.join(token).lower() for token in tri_tokens]
    tri_tokens = [token for token in tri_tokens if token not in stopwords]

    final_tokens = []
    final_tokens.extend(tokens)
    final_tokens.extend(bi_tokens)
    final_tokens.extend(tri_tokens)
    docs[tip.text] = {'freq': {}, 'tf': {}, 'idf': {}}

    for token in final_tokens:
        #The frequency computed for each tip
        docs[tip.text]['freq'][token] = freq(token, final_tokens)
        #The term-frequency (Normalized Frequency)
        docs[tip.text]['tf'][token] = tf(token, final_tokens)

    vocabulary.append(final_tokens)

for doc in docs:
    for token in docs[doc]['tf']:
        #The Inverse-Document-Frequency
        docs[doc]['idf'][token] = idf(token, vocabulary)

print docs