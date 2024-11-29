import gensim


def generate_topic( pipeline, dataframe):
    processed_text = pipeline.named_steps["preprocess"].transform(dataframe)
    dictionary = gensim.corpora.Dictionary(processed_text["tokens"])
    corpus = [dictionary.doc2bow(text) for text in processed_text['tokens']]
    ldamodel = gensim.models.LdaModel(corpus, num_topics=1, id2word=dictionary)
    top_words = [dictionary[word_id] for word_id, prob in ldamodel.get_topic_terms(0, topn=2)]
    
    # Return the words as a string joined by " + "
    return '  '.join(top_words)


