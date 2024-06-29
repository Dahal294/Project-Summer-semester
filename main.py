<<<<<<< HEAD
import requests
from request import get_pmid, get_abstract, preprocess
from flask import Flask
from flask import request, render_template
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from cluster import BagOfWords


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
@app.route('/<name>')
def result():
        if request.method == "POST":
            user_input = request.form["user_input"]
            dataframe=get_abstract(get_pmid(user_input))
            processed = preprocess(dataframe)
            bow = BagOfWords(processed, "clean_msg")
            tf_idf_df = bow.tf_idf()
            num_clusters = 5
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            kmeans.fit(tf_idf_df)
            processed['cluster'] = kmeans.labels_
            return render_template('dataframe.html', dataframe = processed )
        else: 
            return render_template("home.html")
       
if __name__ == "__main__":
    app.run()
=======
from bs4 import BeautifulSoup
import requests
from request import get_result

# url = 'https://en.wikipedia.org/wiki/Springer_Science%2BBusiness_Media'

# response = requests.get(url)

# soup = BeautifulSoup(response.text, "html.parser")
# print(soup.get_text())
# print(soup.prettify())

get_result()
>>>>>>> 8135ae4 (Second commit)
