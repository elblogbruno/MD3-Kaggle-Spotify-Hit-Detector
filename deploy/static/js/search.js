/* Functional, Memoized, cached, and object-oriented spotify search. written in vanilla js.
 */
  
function writeResults(results, index) {
    console.log(results);
    var output = document.getElementById("results");
    output.innerHTML = "";
    
    // this.search_query = document.getElementById("query-input");
    console.log("Index writeresults: " + index);
    var items = results['tracks']['items'];
    var update = new resultList('track', items, index).render();
    // var domElement = document.getElementsByClassName(resultType);
    output.appendChild(update);
}
  
function listItem() {
    this.render = function() {
        var li = document.createElement("li");
        li.className = "list-item";
        var divImage = document.createElement("figure");
        divImage.style.gridArea = "image";
        var divImageWrap = document.createElement("div");
        var divDesc = document.createElement("div");
        divDesc.style.gridArea = "description";
        var img = document.createElement("img");
        var title = document.createElement("p");
        var subtitle = document.createElement("p");
        var anchor = document.createElement("a");
        var imgAnchor = document.createElement("a");

        var butDiv = document.createElement("div");
        butDiv.classList.add("ui-prediction-div");
        butDiv.style.gridArea = "prediction";

        /* predict buttons and result*/
        var predictButton = document.createElement("button");
        var predictResultText = document.createElement("p");
        predictResultText.textContent = 'No result';
        predictResultText.id = this.id+'-predict-result-text';        
        predictButton.className = "ui-prediction-button";
        predictButton.id = this.id+"-predict-button";
        predictButton.textContent = "Predict";

        var href = this.href;
        var id = this.id;
        var release_date = this.release_date;
        predictButton.onclick = function() { predict(href, id, release_date); }
        
        var agreeButton = document.createElement("button");
        agreeButton.style.display = "none";
        agreeButton.className = "ui-prediction-button";
        agreeButton.id = this.id+"-agree-button";
        agreeButton.innerHTML = "<i class='fa fa-thumbs-up'> Agree</i>";
        agreeButton.onclick = function() { like(href, id); }

        var disagreeButton = document.createElement("button");
        disagreeButton.style.display = "none";
        disagreeButton.className = "ui-prediction-button";
        disagreeButton.id = this.id+"-disagree-button";
        disagreeButton.innerHTML = "<i class='fa fa-thumbs-down'> Disagree</i>";
        disagreeButton.onclick = function() { dislike(href, id); }




        img.src = this.src === 0 ? "https://samratcliffe.github.io/images/placeholder.jpg" : this.src;
        anchor.href = imgAnchor.href = this.href;
        anchor.target = imgAnchor.target = "_blank";
        title.classList.add("item-title");
        subtitle.classList.add("item-subtitle");
        title.innerHTML = this.title;
        subtitle.innerHTML = this.subtitle;
        imgAnchor.appendChild(img);
        divImageWrap.appendChild(imgAnchor);
        divDesc.appendChild(title);
        divDesc.appendChild(subtitle);
        divDesc.appendChild(anchor);
        divImage.appendChild(divImageWrap);
        
        div1 = document.createElement("div");
        div1.classList.add("ui-description-div");
        div1.style.gridArea = "info-panel";
        div1.appendChild(divImage);
        div1.appendChild(divDesc);
        
        li.appendChild(div1);

        // li.appendChild(divImage);
        // li.appendChild(divDesc);
        butDiv.appendChild(predictResultText);
        butDiv.appendChild(predictButton);
        butDiv.appendChild(agreeButton);
        butDiv.appendChild(disagreeButton);
        li.appendChild(butDiv);
        return li;
    }
}
  
function resultListItem(resultItem) {
this.title = "<a target='_blank' href='" + resultItem.external_urls.spotify + "'>" + (resultItem.name.length > 45 ? resultItem.name.substr(0, 45) + "…" : resultItem.name) + "</a>";
this.href = resultItem.external_urls.spotify;
this.id = resultItem.id;
this.release_date = resultItem.album.release_date;
switch (resultItem.type) {
    case "artist":
    this.subtitle = Number(resultItem.followers.total).toLocaleString() + " listeners";
    this.src = resultItem.images.length && resultItem.images.slice(-1)[0].url;
    break;
    case "album":
    this.subtitle = resultItem.album_type;
    this.src = resultItem.images.length && resultItem.images.slice(1)[0].url;
    break;
    case "track":
    this.subtitle = "<a target='_blank'  href='" + resultItem.artists[0].external_urls.spotify + "'>" + resultItem.artists[0].name + "</a>" + " • " + "<a target='_blank' href='" + resultItem.album.external_urls.spotify + "'>" + resultItem.album.name + "</a>";
    this.src = resultItem.album.images.length && resultItem.album.images.slice(-1)[0].url;
    break;
    case "playlist":
    this.subtitle = resultItem.type;
    this.src = 0;
    break;
    default:
    this.subtitle = resultItem.type;
    break;
}
}
resultListItem.prototype = new listItem();

function resultList(name, results, index) {
    this.name = name;
    this.results = results;
    this.index = index;
    console.log('result ' + this.index);

    //render
    this.render = function() {
        var ul = document.createElement("ul");
        var headerWrap = document.createElement("div");
        var titleWrap = document.createElement("div");
        var showMoreWrap = document.createElement("div");
        titleWrap.classList.add("title-wrap");
        showMoreWrap.classList.add("show-more-wrap");
        ul.classList.add(this.name);
        var showMore = document.createElement("button");
        showMore.className = "ui-prediction-button";
        showMore.innerHTML = "SHOW MORE";
        showMore.onclick = function() { console.log('showing more: ' + index); getQuery(document.getElementById("query-input").value, index); }
        var header = document.createElement("p");
        header.innerHTML = this.name;
        titleWrap.appendChild(header);
        showMoreWrap.appendChild(showMore);
        headerWrap.appendChild(titleWrap);
        headerWrap.appendChild(showMoreWrap);
        ul.appendChild(headerWrap)
        this.results.map(function(item) {
        var li = new resultListItem(item);
        ul.appendChild(li.render());
        });
        return ul;
    }
}

var search = document.getElementsByClassName("query-input")[0];

search.addEventListener("keyup", function(e) {
    var query = e.target.value;
    var results = document.getElementById("results");
    results.classList = query === "" ? "" : "active";
    //searchLibrary(query);
    // alert(query);
});
search.addEventListener("focus", function(e) {
    var main = document.getElementsByClassName("main")[0];
    main.classList = "main";
});

//cancel on X click or ESC
var cancel = document.getElementsByClassName("cancel")[0];
cancel.addEventListener("click", cancelInput);

document.onkeydown = function(e) {
    e = e || window.event;
    var isEscape = false;
    if ("key" in e) {
        isEscape = e.key == "Escape";
    } else {
        isEscape = e.keyCode == 27;
    }
    if (isEscape) cancelInput();
};

function cancelInput() {
    var main = document.getElementsByClassName("main")[0];
    main.classList.add("inactive");
    search.value = '';
    document.getElementById("results").classList = "";
    document.getElementById("results").innerHTML = "";
    search.blur();
}