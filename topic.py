import gensim

# ===================== Generate Topic =====================
def generate_topic(pipeline, dataframe):
    processed_text = pipeline.named_steps["preprocess"].transform(dataframe)
    tokens = processed_text["tokens"]
    dictionary = gensim.corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(text) for text in tokens]
    
    if not any(corpus):
        return "No topic"
    
    ldamodel = gensim.models.LdaModel(corpus, num_topics=1, id2word=dictionary)
    top_words = [dictionary[word_id] for word_id, prob in ldamodel.get_topic_terms(0, topn=2)]
    
    return '  '.join(top_words)
# ===========================================================

