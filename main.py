import gensim
from request import get_pmid, get_topics
from flask import Flask
from flask_cors import CORS
from flask import request, render_template, jsonify
from sklearn.pipeline import Pipeline
from cluster import preprocess_document, document_to_vector
from scipy.cluster.hierarchy import linkage, fcluster


app = Flask(__name__)
CORS(app)


# ==================== loading the word2vec moel =================
model = gensim.models.KeyedVectors.load_word2vec_format('PubMedWord2Vec.bin', binary=True)

pipeline = Pipeline([
     ("preprocess", preprocess_document()), 
     ("vectorize", document_to_vector(model))
])

@app.route("/", methods=["GET", "POST"])



def result(name=None):
        if request.method == "POST":
            data = request.get_json()
            user_input = data.get("user_input")
            dataframe=get_topics(get_pmid(user_input))
            document_vectors = pipeline.fit_transform(dataframe)
            linked = linkage(document_vectors, method = 'ward')
            num_clusters = 10
            cluster_labels = fcluster(linked, num_clusters, criterion ='maxclust')
            dataframe['cluster'] = cluster_labels
            response_data = []
            for index, row in dataframe.iterrows():
                response_data.append({
                    "PMID": row['PMID'],
                    "TOPIC": row["topics"],
                    "cluster": int(row['cluster'])
                })
            
            return jsonify(response_data)
        else: 
            return render_template("home.html")
       
if __name__ == "__main__":
    app.run()
