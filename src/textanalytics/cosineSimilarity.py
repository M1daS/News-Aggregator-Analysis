

from analytic_normalization import normalize_corpus
from analytic_utils import build_feature_matrix
import numpy as np


def compute_cosine_similarity(doc_features, corpus_features,
                              top_n=3):
    # get document vectors
    doc_features = doc_features[0]
    # compute similarities
    similarity = np.dot(doc_features, 
                        corpus_features.T)
    similarity = similarity.toarray()[0]
    # get docs with highest similarity scores
    top_docs = similarity.argsort()[::-1][:top_n]
    top_docs_with_score = [(index, round(similarity[index], 3))
                            for index in top_docs]
    return top_docs_with_score

    
def init():
    article1Corpus = ['Twenty-four hours after President Donald Trump dictated a dejected letter to Kim Jong Un canceling their June 12 meeting, he appeared to reverse course, telling reporters Friday the diplomatic encounter could still occur on the same date if conditions keep improving.',
    'Trump suggested the two sides were again speaking after an abrupt silence from North Korea prompted US officials to worry.',
    'White House aides were not halting some of the summits planning, which was already underway in Singapore.',
    'And in a tweet on Friday evening, Trump said the US is "having very productive talks with North Korea" about reinstating the summit, likely on the same date',
    'We are having very productive talks with North Korea about reinstating the Summit which, if it does happen, will likely remain in Singapore on the same date, June 12th., and, if necessary, will be extended beyond that date',
    ]


    #querry corpus - these Documents similarity are compared to each item in article1corpus
    article2Corpus = ['Donald Trump has suggested his summit with Kim Jong-un could still go on as planned, marking yet another dramatic reversal for the US president.',
    'Trump told reporters at the White House on Friday, adding that his administration was in talks with Pyongyang and the summit was still possible on its originally scheduled date of 12 June',
    'Trump tweeted later on Friday that the US was having “very productive talks” with Pyongyang about the possible summit.',
    'North Korea’s vice foreign minister Kim Kye-gwan said in a statement']  


    # normalize and extract features from the toy corpus
    norm_corpus = normalize_corpus(article1Corpus, lemmatize=True)
    tfidf_vectorizer, tfidf_features = build_feature_matrix(norm_corpus,
                                                            feature_type='tfidf',
                                                            ngram_range=(1, 1), 
                                                            min_df=0.0, max_df=1.0)
                                                            
    # normalize and extract features from the query corpus
    norm_query_docs =  normalize_corpus(article2Corpus, lemmatize=True)            
    query_docs_tfidf = tfidf_vectorizer.transform(norm_query_docs)

    cosineDict = {}
    for index, doc in enumerate(article2Corpus):
        
        doc_tfidf = query_docs_tfidf[index]
        top_similar_docs = compute_cosine_similarity(doc_tfidf,
                                                 tfidf_features,
                                                 top_n=2)

        similarDocList = []
        for doc_index, sim_score in top_similar_docs:
            similarDocList.append(article1Corpus[doc_index])
        cosineDict[doc] = similarDocList


    print(cosineDict)
    return cosineDict