import re
import numpy as np
import pandas as pd
import warnings

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import gensim
import pyLDAvis.gensim_models # don't skip this
import matplotlib.pyplot as plt

# Stemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# NLTK Stop words
import nltk
from nltk.corpus import stopwords

#wordcloud
from wordcloud import WordCloud

def do_cluster(start_date, end_date):
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    dataset_path = f'static/csv/questions_{start_date}_{end_date}.csv'
    df = pd.read_csv(dataset_path)

    # Menghilangkan informasi jam pada created_at
    df['created_at'] = pd.to_datetime(df['created_at']).dt.date

    # Mengelompokkan content berdasarkan tanggal dibuat yang sama
    df = df.groupby(['created_at'])['content'].apply(' '.join).reset_index()
    data = df['content'].values.tolist()

    stop_words = stopwords.words('indonesian')
    stop_words.extend(['ya', 'yg', 'sih', 'suka', 'indonesia', 'orang', 'aja', 'nya', 'lakukan', 'ga'])

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    # Stemming dan tokenize kalimat
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence).encode('utf-8'), deacc=True))

    data_words = list(sent_to_words(data))
    def tokenize_and_stem(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # Define functions for stopwords, bigrams, trigrams and lemmatization
    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)

    # Create Dictionary
    id2word = corpora.Dictionary(data_words_bigrams)

    # Create Corpus
    texts = data_words_bigrams

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=20, 
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)

    for t in range(lda_model.num_topics):
        plt.figure(figsize=(8, 6), dpi=120)
        plt.imshow(WordCloud(width=800, height=400).fit_words(dict(lda_model.show_topic(t, 100))))
        plt.axis("off")
        plt.title("Topic #" + str(t))
        plt.savefig(f'static/wordclouds/{start_date}_{end_date}_topic{t}.png')

    topics_dict = []
    for t in range(lda_model.num_topics):
        d = dict(lda_model.show_topic(t, 10))
        d = {str(k):float(v) for k,v in d.items()}
        topics_dict.append(d)
    return topics_dict
