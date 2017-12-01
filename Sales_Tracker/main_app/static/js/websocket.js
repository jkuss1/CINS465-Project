var ws = new WebSocket("ws://" + window.location.host);

ws.onopen = function(message)
{
	ws.send(JSON.stringify({
		'event': 0,
		'username': "test"
	}));
}

ws.onmessage = function(message)
{
	var json = JSON.parse(message.data);

	console.log(json);

	if (json.event == 1) {
		if (username == json.userFor) {
			alert(json.userFrom);
		}
	}
}