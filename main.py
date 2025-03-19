from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import concurrent.futures
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import umap
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.pipeline import Pipeline
from gensim.models import KeyedVectors
from request import get_pmid, get_topics
from cluster import preprocess_document, document_to_vector
from topic import generate_topic

matplotlib.use('Agg')

# ===================== Flask App Initialization =======================================
app = Flask(__name__)
CORS(app)
# ======================================================================================

# ===================== Loading word2vec(Bio Embedding Vector) Model ===================
model = KeyedVectors.load_word2vec_format(
    r'D:\Project\backend\Project-Summer-semester\bio_embedding_extrinsic',
    binary=True,
)
# ======================================================================================

# ======================== Data Pipeline for Preprocessing and Transforming ============
pipeline = Pipeline([
    ("preprocess", preprocess_document()),
    ("vectorize", document_to_vector(model))
])
# ======================================================================================

# ===================== Fetching the Topics of Related Documents =======================
def fetch_topics(user_input):
    """Fetch topics for a given user input."""
    pmid_list = get_pmid(user_input)
    dataframe = pd.DataFrame(columns=["PMID", "topics"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_topics, pmid) for pmid in pmid_list]
        for future in concurrent.futures.as_completed(futures):
            dataframe.loc[len(dataframe)] = future.result()
    return dataframe
# =====================================================================================

# ===================== Performing Clustering on Document Vectors =====================
def perform_clustering(document_vectors, num_clusters=8):
    """Perform hierarchical clustering and return cluster labels."""
    cosine_dist_matrix = squareform(pdist(document_vectors, metric='cosine'))
    linked = linkage(cosine_dist_matrix, method='ward')
    cluster_labels = fcluster(linked, num_clusters, criterion='maxclust')
    return linked, cluster_labels
# ======================================================================================

# ===================== Plotting Dendrogram ============================================
def plot_dendrogram(linked, save_path='dendrogram.png'):
    """Plot and save dendrogram."""
    plt.figure()
    dendrogram(linked)
    plt.savefig(save_path)
# =====================================================================================

# ===================== Generating UMAP Visualization =================================
def plot_umap(cluster_labels, document_vectors, save_path='umap_output.png'):
    """Generate and save UMAP visualization."""
    umap_model = umap.UMAP(n_components=2, random_state=42)
    umap_embeddings = umap_model.fit_transform(document_vectors)
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='black')
    ax.set_facecolor('black')
    scatter = ax.scatter(umap_embeddings[:, 0], umap_embeddings[:, 1], 
                         c=cluster_labels, cmap='Paired', s=50)
    plt.colorbar(scatter, label='Cluster')
    plt.title("UMAP Projection of Document Vectors", color='white')
    plt.savefig(save_path)
# ====================================================================================

# ===================== Flask Route for Processing User Input ========================
@app.route("/", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        data = request.get_json()
        user_input = data.get("user_input")
        dataframe = fetch_topics(user_input)
        document_vectors = pipeline.fit_transform(dataframe)
        linked, cluster_labels = perform_clustering(document_vectors)
        dataframe['cluster'] = cluster_labels
        
        print("Silhouette Score:", silhouette_score(document_vectors, cluster_labels))
        print("Davies-Bouldin Score:", davies_bouldin_score(document_vectors, cluster_labels))
        
        plot_dendrogram(linked)
        plot_umap(cluster_labels, document_vectors)
        
        grouped_data = dataframe.groupby("cluster")
        topic_dict = {cluster: generate_topic(pipeline, group) for cluster, group in grouped_data}
        
        response_data = [
            {
                "PMID": row['PMID'],
                "TOPIC": row["topics"],
                "cluster": int(row['cluster']),
                "cluster_topic": topic_dict.get(row['cluster'], "Unknown")
            }
            for _, row in dataframe.iterrows()
        ]
        
        return jsonify(response_data)
    
    return render_template("home.html")
# ====================================================================================

# ===================== Running Flask App ============================================
if __name__ == "__main__":
    app.run()
# ====================================================================================
#============================= Thank You =============================================
