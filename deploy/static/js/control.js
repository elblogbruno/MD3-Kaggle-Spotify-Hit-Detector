// document ready event

$( document ).ready(function() {
    console.log( "ready!" );
    subscribe_event();
});

function subscribe_event(){
    document.getElementById("query-input").addEventListener("change", function(){
        // api request to flask server to get the possible song list for the query
        console.log("searching for " + this.value);
    
        $.ajax({
            url: '/get_spotify_query_result',
            dataType: "json",
            type: "Post",
            async: true,
            data: {'query': this.value},
            success: function (data) {
                console.log(data);
                if (data['error'])
                {
                    document.getElementById('error-message-text').style.display = 'block';
                    document.getElementById('error-message-text').textContent = data['result'];
                }else{
                    writeResults(data['result']);
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
            if (data == '0')
                document.getElementById(song_id+"-predict-result-text").innerHTML = "This song will be a flop! ):";
            else
                document.getElementById(song_id+"-predict-result-text").innerHTML = "This song will be a hit! :)";
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
