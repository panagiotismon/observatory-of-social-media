from flask import Flask, request, render_template, redirect
from waitress import serve
try:
    from tools import trend_results, sentiment_results
except ImportError:
    import sys
    import os
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))
    from tools import trend_results, sentiment_results


app = Flask(__name__, static_url_path="/observatory/static", static_folder="static")

@app.route("/")
def root_page():
    return redirect("/observatory")


@app.route("/observatory")
def homepage():
    return render_template("index.html")


@app.route("/index.html")
def menu():
    return render_template("index.html")


@app.route("/observatory/index.html")
def observatory_menu():
    return render_template("index.html")


@app.route("/observatory/trends", methods=["GET"])
def trends_form():
    return render_template("trends.html")


@app.route("/observatory/trends/results", methods=["POST"])
def trend_analysis():
    return trend_results(request=request)


@app.route("/observatory/sentimentanalysis", methods=["GET"])
def sentimentanalysis_form():
    return render_template("sentimentanalysis.html")        


@app.route("/observatory/sentimentanalysis/results", methods=["POST"])
def sentiment_analysis():
    return sentiment_results(request=request)



if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000, threads=4)
    # app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
