var currentColumn = 0,
    iosocket = io.connect(),
    columns = [document.getElementById("left-column"),
            document.getElementById("right-column")];

function dataToDescriptionList(data)
{
    var dl = document.createElement("dl");
    for (var key in data)
    {
        if (data.hasOwnProperty(key))
        {
            var dt = document.createElement("dt"),
                dd = document.createElement("dd");
            
            dt.innerHTML = key;
            dd.innerHTML = data[key];
            
            dl.appendChild(dt);
            dl.appendChild(dd);
        }
    }
    return dl;
}

function flipCard(cardId)
{ 
    front = document.getElementById("frontImage-" + cardId);
    back = document.getElementById("backData-" + cardId);
   
    // zIndex & opacity replace the lack of rotateY() support in mobile.

    flipped = "rotateY(180deg)";
    isFlipped = front.style.transform == flipped; 
    if (isFlipped)
    {
        degrees = 0;
        opacity = 1;
    }
    else
    {
        degrees = 180;
        opacity = 0.4;
    }
    front.style.transform = flipped.replace("180", degrees);
    front.style.opacity = opacity;

    flipped = "rotateY(0deg)";
    isFlipped = back.style.transform == flipped;
    if (isFlipped)
    {
        degrees = 180;
        opacity = 0;
        zindex = -1;
    }
    else
    {
        degrees = 0;
        opacity = 1;
        zindex = 0.6;
    }
    back.style.transform = flipped.replace("0", degrees);
    back.style.opacity = opacity;
    back.style.zIndex = zindex;
}

function buildCardFace(content, isfront, cardId, cardFace)
{
    var a = document.createElement("a");
    a.addEventListener("click", function()
    {
        back = document.getElementById("backData-" + cardId);
        if (back.firstChild.childNodes.length == 1) // get once
        {
            iosocket.emit('getData', cardId);
        }
        flipCard(cardId);
    });

    if (isfront)
    {
        a.appendChild(content);
    }
    else
    {
        a.innerHTML = content;       
    }

    var container = document.createElement("div");
    container.id = cardFace + "-" + cardId;
    container.className = cardFace;
    container.appendChild(a);
    
    return container;
}

function buildNewImageContainer(filename, url)
{
    var image = new Image();
    image.id = filename;
    image.src = url + filename;
    
    front = buildCardFace(image, true, filename, "frontImage"); 
    back = buildCardFace("<dl></dl>", false, filename, "backData");
    
    var container = document.createElement("div");
    container.className = "container-" + filename; 
    container.appendChild(back);
    container.appendChild(front);
    
    return container;
}

function insertImageAtFirst(filename, url)
{
    newContainer = buildNewImageContainer(filename, url);
    referenceElement = columns[currentColumn].firstChild;

    columns[currentColumn].insertBefore(newContainer, referenceElement);
    currentColumn = (currentColumn == 0) ? 1 : 0;
};

function removeImage(filename)
{
    document.getElementById(filename).remove();
};

iosocket.on('addImages', function(filenames, url)
{
    for (i = 0; i < filenames.length; i++)
    {
        insertImageAtFirst(filenames[i], url, false);
    }
});

iosocket.on('addImage', function(filename, url)
{
    insertImageAtFirst(filename, url);
});

iosocket.on('removeImage', function(filename)
{
    removeImage(filename);
});


iosocket.on("setBackData", function(cardId, data)
{
    back = document.getElementById("backData-" + cardId);
    a = back.firstChild;
    a.appendChild(dataToDescriptionList(data));
});

