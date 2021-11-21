from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from spotipy_api import *

app = Flask(__name__, template_folder='template')


@app.route('/')
def index():
    return render_template("index.html")

"""
View that receives the query from the form and returns the result contacting spotify
"""
@app.route('/get_spotify_query_result', methods=['POST'])
def get_spotify_query_result():
    if request.method == 'POST':
        print("Request received")
        print(request.form)
        query = request.form['query']
        result = query_spotify(query)
        return jsonify(result)

def predict_value(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(-1, 1)
    print(to_predict)
    loaded_model = joblib.load('model-spotify.sav')
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/get_prediction_for_song', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        song_id = request.form['query']
        song_features = get_data_for_new_song(song_id)
        print(song_features)
        prediction = predict_value(song_features)
        print(prediction)
        return str(prediction)


if __name__ == '__main__':
    app.run(debug=True)