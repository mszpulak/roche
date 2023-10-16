function getStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(json => {
            console.log(JSON.stringify(json));

            const power_status = document.getElementById('power_status');
            power_status.value = json['state'];
            const power = document.getElementById('power');
            power.value = json['power'];
            const time = document.getElementById('time');
            time.value = json['time'];
        })
}

function postPowerPlus() {
    fetch('/handle_button_push', {
        method: 'POST',
        body: JSON.stringify({"button": "PLUS_POWER"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if(!response.ok){
                return response.json().then(json => {throw new Error(json["detail"])});
            }
            return response.json();
        })
        .then(json => {
            console.log(JSON.stringify(json));
            const power_status = document.getElementById('power');
            power_status.value = json['power'];
        })
        .catch(error => {
            alert(error.message);
            console.log(error.message);
        })
}


function postPowerMinus() {
    fetch('/handle_button_push', {
        method: 'POST',
        body: JSON.stringify({"button": "MINUS_POWER"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response =>  {
            if(!response.ok){
                return response.json().then(json => {throw new Error(json["detail"])});
            }
            return response.json();
        })
        .then(json => {
            console.log(JSON.stringify(json));
            const power_status = document.getElementById('power');
            power_status.value = json['power'];
        })
        .catch(error => {
            alert(error.message);
            console.log(error.message);
        })
}


function postTimePlus() {
    fetch('/handle_button_push', {
        method: 'POST',
        body: JSON.stringify({"button": "PLUS_TIME"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response =>  {
            if(!response.ok){
                return response.json().then(json => {throw new Error(json["detail"])});
            }
            return response.json();
        })
        .then(json => {
            console.log(JSON.stringify(json));
            const power_status = document.getElementById('time');
            power_status.value = json['time'];
        })
        .catch(error => {
            alert(error.message);
            console.log(error.message);
        })
}


function postTimeMinus() {
    fetch('/handle_button_push', {
        method: 'POST',
        body: JSON.stringify({"button": "MINUS_TIME"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response =>  {
            if(!response.ok){
                return response.json().then(json => {throw new Error(json["detail"])});
            }
            return response.json();
        })
        .then(json => {
            console.log(JSON.stringify(json));
            const power_status = document.getElementById('time');
            power_status.value = json['time'];
        })
        .catch(error => {
            alert(error.message);
            console.log(error.message);
        })
}


function postPowerOn() {
    fetch('/handle_button_push', {
        method: 'POST',
        body: JSON.stringify({"button": "ON"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response =>  {
            if(!response.ok){
                return response.json().then(json => {throw new Error(json["detail"])});
            }
            return response.json();
        })
        .then(json => {
            const power_status = document.getElementById('power_status');
            power_status.value = json['state'];
        })
        .catch(error => {
            alert(error.message);
            console.log(error.message);
        })
}


function postPowerOff() {
    fetch('/handle_button_push', {
        method: 'POST',
        body: JSON.stringify({"button": "OFF"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response =>  {
            if(!response.ok){
                return response.json().then(json => {throw new Error(json["detail"])});
            }
            return response.json();
        })
        .then(json => {
            const power_status = document.getElementById('power_status');
            power_status.value = json['state'];
        })
        .catch(error => {
            alert(error.message);
            console.log(error.message);
        })
}


function postCancel() {
    fetch('/cancel', {
        method: 'POST',
        body: JSON.stringify({"button": "CANCEL"}),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ik1hcmNpbiBTenB1bGFrIiwiaWF0IjoxNjk3Mjc4OTE1LCJhdWQiOiJBWlVSRV9CQUNLRU5EX0NMSUVOVF9JRCIsImlzcyI6IkFaVVJFX0JBQ0tFTkRfVEVOQU5UIiwiZXhwIjoxNzI4OTAxMzE1fQ.GWkmndWeRXUR80p0uBRwC3iaK2kjZZ-Hmv67x5SpXUs'
        }
    })
        .then(response =>  {
            if(!response.ok){
                return response.json().then(json => {throw new Error(json["detail"])});
            }
            return response.json();
        })
        .then(json => {
            console.log(JSON.stringify(json));

            const power_status = document.getElementById('power_status');
            power_status.value = json['state'];
            const power = document.getElementById('power');
            power.value = json['power'];
            const time = document.getElementById('time');
            time.value = json['time'];
        })
        .catch(error => {
            alert(error.message);
            console.log(error.message);
        })
}


const ws_path = "ws://" + window.location.host +'/ws_status';
const websocket = new WebSocket(ws_path);

websocket.addEventListener("message", (event) => {
  console.log("Message from server ", JSON.parse(event.data));
  const power_status = document.getElementById('power_status_ws');
    power_status.value = JSON.parse(event.data)['state'];
    const power = document.getElementById('power_ws');
    power.value = JSON.parse(event.data)['power'];
    const time = document.getElementById('time_ws');
    time.value = JSON.parse(event.data)['time'];
});
