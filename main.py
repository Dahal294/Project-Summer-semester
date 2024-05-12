import requests
from request import get_pmid, get_abstract, preprocess
from flask import Flask
from flask import request, render_template


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
@app.route('/<name>')
def result():
        if request.method == "POST":
            user_input = request.form["user_input"]
            dataframe=get_abstract(get_pmid(user_input))
            processed = preprocess(dataframe)
            return render_template('dataframe.html', dataframe = processed )

        else: 
            return render_template("home.html")
       
if __name__ == "__main__":
    app.run()