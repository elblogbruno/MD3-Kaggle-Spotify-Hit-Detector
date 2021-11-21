// document ready event

$( document ).ready(function() {
    console.log( "ready!" );
    subscribe_event();
});

function subscribe_event(){
    document.getElementById("query-input").addEventListener("input", function(){
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
                // var song_list = data;
                // var song_list_html = "";
                // for (var i = 0; i < song_list.length; i++) {
                //     // if song is the first one, as a default, select it
                //     if (i == 0)
                //         song_list_html += "<option value='" + song_list[i]['uri'] + "' selected>" + song_list[i]['name'] + "</option>";
                //     else
                //         song_list_html += "<option value='" + song_list[i]['uri'] + "'>" + song_list[i]['name'] + "</option>";
                //     // add image to the list
                //     song_list_html += "<img src='" + song_list[i]['album']['images'][0]['url'] + "'>";

                // }
                // document.getElementById("results").innerHTML = song_list_html;

                writeResults(data);
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
               
            }
        }); 
    });
}

function predict(song_uri){
    // api request to flask server to get the possible song list for the query
    console.log("Predicting for " + song_uri);
    
    // get the song uri
    // var song_uri = document.getElementById("song_list").value;

    $.ajax({
        url: '/get_prediction_for_song',
        dataType: "json",
        type: "Post",
        async: true,
        data: {'query': song_uri},
        success: function (data) {
            console.log(data);
            if (data == 0)
                document.getElementById("prediction-result").innerHTML = "This song will be a flop! ):";
            else
                document.getElementById("prediction-result").innerHTML = "This song will be a hit! :)";
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
            
        }
    }); 
}
