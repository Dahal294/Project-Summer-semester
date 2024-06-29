import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer




class BagOfWords:
    def __init__(self, dataframe, column_name):
        self.dataframe = dataframe
        self.column_name = column_name
        self.vectorizer = TfidfVectorizer()
        self.fitted = False  # Indicator to check if the vectorizer is fitted

    def tf_idf(self):
        series = self.dataframe[self.column_name]
        tf_idf_matrix = self.vectorizer.fit_transform(series)
        self.fitted = True  # Set the indicator to True after fitting
        tf_idf_df = pd.DataFrame(tf_idf_matrix.toarray(), columns=self.vectorizer.get_feature_names_out())
        return tf_idf_df

    def tf_idf_query(self, row_number):
        if not self.fitted:
            raise ValueError("The TF-IDF vectorizer is not fitted. Call tf_idf() first.")
        text = self.dataframe.loc[row_number, self.column_name]
        tf_idf_vector = self.vectorizer.transform([text])
        return tf_idf_vector
    


