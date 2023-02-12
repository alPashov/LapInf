from flask import Flask, render_template
import webbrowser #For Debig
from allPagesScraper import flask_list_return as scraper

list = scraper()

app = Flask(__name__)

@app.route("/")
def index_page():
    return str(list)

if __name__ == "__main__":
    webbrowser.open_new_tab("localhost:5050")
    app.run(host="0.0.0.0", port=5050)