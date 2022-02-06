from flask import Flask, render_template, request, jsonify
from deploy.model_utils import *
from deploy.spotipy_api import *
from deploy.database.model import *
import db

db.Base.metadata.create_all(db.engine)
app = Flask(__name__, template_folder='deploy/template', static_folder='deploy/static')

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}), 200

@app.route('/')
def index():
    last_user_entry = UserSongFeedback.get_last_entry()
    unique_count = UserSongFeedback.get_unique_count()
    unique_count_today = UserSongFeedback.get_unique_count_today()
    # print (last_user_entry.song_name , unique_count, unique_count_today)
    return render_template("index.html", last_user_entry=last_user_entry, unique_count_today=unique_count_today, unique_count=unique_count)

"""
View that receives the query from the form and returns the result contacting spotify
"""
@app.route('/get_spotify_query_result', methods=['POST'])
def get_spotify_query_result():
    if request.method == 'POST':
        print("Request received")
        print(request.form)
        if request.form['query'] == "":
            return jsonify({"error": "Please enter a query"})
        else:
            query = request.form['query']
        
        if 'index' in request.form:
            index = int(request.form['index'])
        else:
            index = 0

        result, error = query_spotify(query, index)

        print(index)

        index += 5

        return jsonify(result=result, error=error, index=index)


@app.route('/get_user_song_feedback', methods=['POST'])
def get_user_song_feedback():
    if request.method == 'POST':
        print("Request received")
        print(request.form)
        ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


        if request.form['song_uri'] == "":
            return jsonify({"message": "Please enter a song uri"})
        else:
            song_uri = request.form['song_uri']

        if request.form['song_id'] == "":
            return jsonify({"message": "Please enter a song id"})
        else:
            song_id = request.form['song_id']
        
        # create unique identifier for the user based on ip addred and song id
        user_id = ip_addr + song_id 
        # check if the user has already submitted feedback for this song
        user_song_feedback = UserSongFeedback.get_feedback_by_user_id(user_id)
        
        if user_song_feedback:
            return jsonify({"message": "You have already submitted feedback for this song"})
            
        if 'song_artist' in request.form:
            song_artist = request.form['song_artist']
        else:
            song_artist = ""

        if 'feedback' in request.form:
            feedback = int(request.form['feedback'])
        else:
            feedback = 0

        if 'song_name' in request.form:
            song_name = request.form['song_name']

        

        # Add feedback to database
        f = UserSongFeedback(song_uri, song_id, song_name, song_artist, user_id, feedback)
        f.save()

        return jsonify({"message": "Thank you for your feedback!"})



@app.route('/get_prediction_for_song', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        song_id = request.form['query']
        release_date =  request.form['release_date']

        song_features = get_data_for_new_song(song_id, release_date)
        prediction, flop_percent, hit_percent  = predict_value(song_features)
        
        flop_percent = round(flop_percent, 2)*100
        hit_percent = round(hit_percent, 2)*100
        # save_new_entry(release_date,  song_features, prediction) # Save the new entry in the database
        
        return jsonify(prediction=str(prediction), flop_percent=str(flop_percent), hit_percent=str(hit_percent))


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=5003)
    app.run()
