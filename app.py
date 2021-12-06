from flask import Flask, render_template, request, jsonify
from deploy.model_utils import *
from deploy.spotipy_api import *
from deploy.database.model import *
import db

db.Base.metadata.create_all(db.engine)
app = Flask(__name__, template_folder='deploy/template', static_folder='deploy/static')


@app.route('/')
def index():
    entry = DataEntry().get_last_entry()
    return render_template("index.html", entry=entry)

"""
View that receives the query from the form and returns the result contacting spotify
"""
@app.route('/get_spotify_query_result', methods=['POST'])
def get_spotify_query_result():
    if request.method == 'POST':
        print("Request received")
        print(request.form)
        query = request.form['query']
        result, error = query_spotify(query)
        return jsonify(result=result, error=error)

@app.route('/get_prediction_for_song', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        song_id = request.form['query']
        release_date =  request.form['release_date']

        song_features = get_data_for_new_song(song_id)
        print(song_features)
        prediction = predict_value(song_features)
        print(prediction)
        save_new_entry(release_date,  song_features, prediction) # Save the new entry in the database
        return str(prediction)


if __name__ == '__main__':
    app.run(debug=True)