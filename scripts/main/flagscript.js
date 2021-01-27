alert("NO ABUSE PLEASE ! Abusa have flagged the abusive words and Highlighted the content.")

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

fetch("https://abusa.herokuapp.com/getAbusiveData").then(r => {
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
                document.getElementById(arr[i].id).firstChild.nodeValue = document.getElementById(arr[i].id).firstChild.nodeValue.replace(arr[i].data[j], arr[i].data[j]+" ⚑");
        }
    }
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: JSON.stringify(data)
    });

    return response.json();
}

data_value = '';
var intervalID;

function final_data(data = []) {
    console.log(data);
    //Play With Your Data
    for (var i = 0; i < data.length; i++)
    {
        max_key = 'Hate';
        for (const [key, value] of Object.entries(data[i].predictions)) {
            max_key = data[i].predictions[max_key] > value? max_key: (key == 'Toxic' && data[i].predictions[max_key] > 0.6? max_key: key);
        }

        switch (max_key) {
            case 'Hate':
                document.getElementById(data[i].id).setAttribute('style', 'color: purple');
                break;
            case 'Insult':
                document.getElementById(data[i].id).setAttribute('style', 'color: lightblue');
                break;
            case 'Obscene':
                document.getElementById(data[i].id).setAttribute('style', 'color: red');
                break;
            case 'Threat':
                document.getElementById(data[i].id).setAttribute('style', 'color: brown');
                break;
            default:
                document.getElementById(data[i].id).setAttribute('style', 'color: yellow');
                break;
        }
    }
}

function responce_handeler(res) {
    res.then(data => {
        console.log(data);
        if (data.response === "success") {
            clearInterval(intervalID);
            final_data(data.data);
        }
    });
}

async function getData(url = '') {
    const response = await fetch(url);

    responce_handeler(response.json());
}

function ticData() {
    intervalID = setInterval(getData, 10000, 'https://abusa.herokuapp.com/getModelOutput' + '?threadnum=' + data_value)
}

postData("https://abusa.herokuapp.com/modelData", arr)
    .then(data => {
        console.log(data);
        data_value = data.threadnum;
        ticData();
    });
