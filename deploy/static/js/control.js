// document ready event

$( document ).ready(function() {
    console.log( "ready!" );
    subscribe_event();
});

function subscribe_event(index=0){
    document.getElementById("query-input").addEventListener("change", function()
    {
         getQuery(this.value, index);
    });
}

function getQuery(value, index)
{
    console.log(index);
    if (index == 0)
    {
        data = {'query': value }
    }
    else
    {
        data = {'query': value, 'index': index}
    }
    // api request to flask server to get the possible song list for the query
    console.log("searching for " + value);

    $.ajax({
        url: '/get_spotify_query_result',
        dataType: "json",
        type: "Post",
        async: true,
        data: data,
        success: function (data) {
            console.log(data);
            if (data['error'])
            {
                document.getElementById('error-message-text').style.display = 'block';
                document.getElementById('error-message-text').textContent = data['result'];
            }else{
                writeResults(data['result'], data['index']);
            }
        },
        error: function (xhr, exception) {
            var msg = "";
            if (xhr.status === 0) {
                msg = "Not connect.\n Verify Network." + xhr.responseText;
            } else if (xhr.status == 404) {
                msg = "Requested page not found. [404]" + xhr.responseText;
            } else if (xhr.status == 500) {
                msg = "Internal Server Error [500]." +  xhr.responseText;
            } else if (exception === "parsererror") {
                msg = "Requested JSON parse failed.";
            } else if (exception === "timeout") {
                msg = "Time out error." + xhr.responseText;
            } else if (exception === "abort") {
                msg = "Ajax request aborted.";
            } else {
                msg = "Error:" + xhr.status + " " + xhr.responseText;
            }
           
            document.getElementById('error-message-text').style.display = 'block';
            document.getElementById('error-message-text').textContent = msg;
        }
    });
}

function predict(song_uri, song_id, release_date){
    // api request to flask server to get the possible song list for the query
    console.log("Predicting for " + song_uri + " " + song_id + " " + release_date);
    
    // get the song uri
    // var song_uri = document.getElementById("song_list").value;

    $.ajax({
        url: '/get_prediction_for_song',
        dataType: "json",
        type: "Post",
        async: true,
        data: {'query': song_uri, 'release_date': release_date},
        success: function (data) {
            document.getElementById('error-message-text').style.display = 'none';

            console.log(data);
            console.log(song_id);
            if (data['prediction'] == '0')
                document.getElementById(song_id+"-predict-result-text").innerHTML = "This song will be a flop! ):"; 
            else
                document.getElementById(song_id+"-predict-result-text").innerHTML = "This song will be a hit! :)";

            document.getElementById(song_id+"-predict-result-text").innerHTML += " Flop Probability: " + data['flop_percent'] + "%"+ " Hit Probability: " + data['hit_percent'] + "%"; 
            
            document.getElementById(song_id+"-agree-button").style.display = 'inline';
            document.getElementById(song_id+"-disagree-button").style.display = 'inline';
            document.getElementById(song_id+"-predict-button").style.display = 'none';
            

        },
        error: function (xhr, exception) {
            var msg = "";
            if (xhr.status === 0) {
                msg = "Not connect.\n Verify Network." + xhr.responseText;
            } else if (xhr.status == 404) {
                msg = "Requested page not found. [404]" + xhr.responseText;
            } else if (xhr.status == 500) {
                msg = "Internal Server Error [500]." +  xhr.responseText;
            } else if (exception === "parsererror") {
                msg = "Requested JSON parse failed.";
            } else if (exception === "timeout") {
                msg = "Time out error." + xhr.responseText;
            } else if (exception === "abort") {
                msg = "Ajax request aborted.";
            } else {
                msg = "Error:" + xhr.status + " " + xhr.responseText;
            }
            document.getElementById('error-message-text').style.display = 'block';
            document.getElementById('error-message-text').textContent = msg;
        }
    }); 
}

function add_feedback(song_uri, song_id, song_name, song_artist, like_dislike){
    // api request to flask server to get the possible song list for the query
    console.log("Adding feedback for " + song_uri + " " + song_id + " " + song_name + " " + song_artist + " " + like_dislike);
    $.ajax({
        url: '/get_user_song_feedback',
        dataType: "json",
        type: "Post",
        async: true,
        data: {'song_id': song_id, 'song_uri': song_uri, 'song_artist': song_artist,'feedback': like_dislike, 'song_name': song_name},
        success: function (data) {
            document.getElementById('error-message-text').style.display = 'none';
            console.log(data);
            
            document.getElementById(song_id+"-predict-result-text").innerHTML = data['message'];

            // document.getElementById(song_id+"-predict-result-text").innerHTML += " Flop Probability: " + data['flop_percent'] + "%"+ " Hit Probability: " + data['hit_percent'] + "%"; 
            
            document.getElementById(song_id+"-agree-button").style.display = 'none';
            document.getElementById(song_id+"-disagree-button").style.display = 'none';
            document.getElementById(song_id+"-predict-button").style.display = 'none';
        },
        error: function (xhr, exception) {
            var msg = "";
            if (xhr.status === 0) {
                msg = "Not connect.\n Verify Network." + xhr.responseText;
            } else if (xhr.status == 404) {
                msg = "Requested page not found. [404]" + xhr.responseText;
            } else if (xhr.status == 500) {
                msg = "Internal Server Error [500]." +  xhr.responseText;
            } else if (exception === "parsererror") {
                msg = "Requested JSON parse failed.";
            } else if (exception === "timeout") {
                msg = "Time out error." + xhr.responseText;
            } else if (exception === "abort") {
                msg = "Ajax request aborted.";
            } else {
                msg = "Error:" + xhr.status + " " + xhr.responseText;
            }
            document.getElementById('error-message-text').style.display = 'block';
            document.getElementById('error-message-text').textContent = msg;
        }
    }); 
}