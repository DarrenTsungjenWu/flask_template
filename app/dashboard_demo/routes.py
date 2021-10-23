from flask import Flask, render_template
from app.dashboard_demo import blueprint
from flask import Blueprint 
import pandas as pd
import numpy as np

# app = Flask(__name__)
# @app.route("/", methods=["GET", "POST"])

@blueprint.route('/main_page', methods = ['POST', 'GET'])
def print_hello():
    return render_template("tables-data_copy.html")

if __name__ == "__main__":
    app.run()
