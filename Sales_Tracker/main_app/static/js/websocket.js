var wsURL = "ws://" + window.location.host;
var slug = window.location.pathname;

var ws = new WebSocket(wsURL);

ws.onopen = function(message){}

ws.onmessage = function(message)
{
	var json = JSON.parse(message.data);

	console.log(json);
}