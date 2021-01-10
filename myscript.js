
alert("WE GOTTA PROBLEM HERE DUDE!!?? NO ABUSE PLZZ...")
arr = []
id = "abusarandomid";
idNum = 0;
var startElem = document.getElementsByTagName('body')[0];
var items = startElem.getElementsByTagName("*");

for (var i = 0; i < items.length; i++) {
    if (items[i].childNodes.length === 1)
    {
        if (items[i].innerText !== null && items[i].innerText !== "" && items[i].innerText !== undefined && items[i].getAttribute('id') !== 'style' && items[i].getAttribute('id') !== 'script')
        {
            if (items[i].getAttribute('id') === null)
                items[i].setAttribute('id', id + idNum++);

            data = {
                "id": items[i].getAttribute('id'),
                "data": items[i].innerText.split(" ")
            }

            arr.push(data)
        }
    }
}

const url = "https://abusa.herokuapp.com/getAbusiveData";

fetch(url).then(r => {
    if (r.ok) {
        printData(r.json());
    }
});

function printData(data) {
    data.then(r => {
        checkData(r);
    });
}

function checkData(data) {
    for (var i = 0; i < arr.length; i++) {
        for (var j = 0; j < arr[i].data.length; j++) {
            if (arr[i].data[j].toLowerCase() in data && document.getElementById(arr[i].id).firstChild.nodeValue !== null)
                document.getElementById(arr[i].id).firstChild.nodeValue = document.getElementById(arr[i].id).firstChild.nodeValue.replace(arr[i].data[j], arr[i].data[j]+"⚑");
        }
    }
}