import matplotlib.pyplot
import gensim
from request import get_pmid, get_topics
from flask import Flask
from flask_cors import CORS
from flask import request, render_template, jsonify
from sklearn.pipeline import Pipeline
from cluster import preprocess_document, document_to_vector
import matplotlib
matplotlib.use('Agg') 
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import gensim.downloader as api
from topic import generate_topic
import concurrent.futures
import pandas as pd

app = Flask(__name__)
CORS(app)



# ==================== loading the word2vec moel =================


model = api.load("glove-wiki-gigaword-300")

pipeline = Pipeline([
     ("preprocess", preprocess_document()), 
     ("vectorize", document_to_vector(model))
])

@app.route("/", methods=["GET", "POST"])


def result(name=None):
        if request.method == "POST":
            data = request.get_json()
            user_input = data.get("user_input")
            pmid_list = get_pmid(user_input)
            dataframe = pd.DataFrame(columns=["PMID", "topics"])
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(get_topics, pmid) for pmid in pmid_list]
                for future in concurrent.futures.as_completed(futures):
                     dataframe.loc[len(dataframe)] = future.result()
            
            # dataframe=get_topics(get_pmid(user_input))
            document_vectors = pipeline.fit_transform(dataframe)
            linked = linkage(document_vectors, method = 'ward')
            num_clusters = 10
            cluster_labels = fcluster(linked, num_clusters, criterion ='maxclust')
            dataframe['cluster'] = cluster_labels
            matplotlib.pyplot.figure()
            dn = dendrogram(linked)
            matplotlib.pyplot.savefig('output.png')
            response_data = []
            grouped_data = dataframe.groupby("cluster")
            topic_dict = {}
            for cluster, group  in grouped_data:
                 topic = generate_topic(pipeline, group)
                 topic_dict.update({cluster: topic})
            #      print(f" cluster {cluster} topics:")
            #      print(topic)
            # print(topic_dict)
            for index, row in dataframe.iterrows():
                response_data.append({
                    "PMID": row['PMID'],
                    "TOPIC": row["topics"],
                    "cluster": int(row['cluster'])
                })
             
            for row in response_data:
                cluster_id = row['cluster']  # Get the cluster ID for each row
                if cluster_id in topic_dict:  # Check if the topic for that cluster exists
                    row['cluster_topic'] = topic_dict[cluster_id]  # Add the topic to the row

            return jsonify(response_data)
        else: 
            return render_template("home.html")
       
if __name__ == "__main__":
    app.run()
