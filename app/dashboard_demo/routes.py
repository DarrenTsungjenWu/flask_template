from flask import Flask, Blueprint, render_template, request, jsonify, Markup
from app.dashboard_demo import blueprint
import pandas as pd
import numpy as np
import json
import mysql.connector
from plotly.offline import plot
from plotly.graph_objs import Scatter
from connector_module import get_connection, get_cursor, create_and_delete_example_table, delete_selected_row

# app = Flask(__name__)
# @app.route("/", methods=["GET", "POST"])

@blueprint.route('/main_page', methods = ['POST', 'GET'])
def print_hello():
    (cursor, cnx) = get_cursor()
    sql = "SELECT * FROM `example`"
    cursor.execute(sql)
    df=cursor.fetchall()

    # Plot #
    x, y = [], []
    for i in range(len(df)):
        x.append(df[i]['event_date'])
        y.append(df[i]['col_0'])
    # my_plot_div = plot([Scatter(x=[1, 2, 3], y=[4, 5, 6])], output_type='div')
        my_plot_div = plot([Scatter(x=x, y=y)], output_type='div')
        
    return render_template("tables-data_copy3.html", df = df, # tables-data_copy2 crud_table
                            div_placeholder=Markup(my_plot_div),
                            )

@blueprint.route('/save_table', methods = ['POST', 'GET'])
def save_table():
    if request.method == 'POST':
        example_table_data = json.loads(request.data)
        example_table_data = pd.DataFrame(example_table_data)
        #update_example_table(example_table_data)
        print(example_table_data)
        create_and_delete_example_table(example_table_data)

    return jsonify('success')

@blueprint.route('/delete_row', methods = ['POST', 'GET'])
def delete_row():
    if request.method == 'POST':
        example_table_data = json.loads(request.data) # json loads byte object to frontend
        # print(example_table_data['event_date'])
        delete_selected_row(example_table_data['event_date'])

    return jsonify('success')

if __name__ == "__main__":
    app.run()
