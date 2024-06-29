import requests
from request import get_pmid, get_abstract, preprocess
from flask import Flask
from flask_cors import CORS
from flask import request, render_template, jsonify
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from cluster import BagOfWords


app = Flask(__name__)

CORS(app)

@app.route("/", methods=["GET", "POST"])
def result(name=None):
        if request.method == "POST":
            data = request.get_json()
            user_input = data.get("user_input")
            dataframe=get_abstract(get_pmid(user_input))
            processed = preprocess(dataframe)
            bow = BagOfWords(processed, "clean_msg")
            tf_idf_df = bow.tf_idf()
            num_clusters = 5
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            kmeans.fit(tf_idf_df)
            processed['cluster'] = kmeans.labels_
            response_data = []
            for index, row in processed.iterrows():
                response_data.append({
                    "PMID": row['PMID'],
                    "cluster": int(row['cluster'])
                })
            
            return jsonify(response_data)
        else: 
            return render_template("home.html")
       
if __name__ == "__main__":
    app.run()
