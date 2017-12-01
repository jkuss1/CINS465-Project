var ws = new WebSocket("ws://" + window.location.host);
var chatCont = document.getElementById("chat-cont");
var chatHeader = document.getElementById("chat-header");
var chatHeaderBtns =
	"<button id=\"chat-accept\" class=\"button\" onclick=\"showChat()\">Y</button>" +
	"<button id=\"chat-decline\" class=\"button bg-red\" onclick=\"closeChat()\">N</button>";
var userFrom;

ws.onopen = function() {}

ws.onmessage = function(message)
{
	var json = JSON.parse(message.data);

	console.log(json);
	
	if (json.event == 1) {
		if (curUsername == json.userFor) {
			userFrom = json.userFrom;
			
			chatCont.style.display = "inline";
			chatCont.classList.add("chat-small");
			chatHeader.innerHTML = json.userFrom + " would like to chat.&nbsp;" + chatHeaderBtns;
		}
	}
	else if (json.event == 101) {
		if (curUsername == json.userFor) {
			chatCont.style.display = "inline";
			chatCont.classList.add("chat-large");
			alert("You are now chatting with " + json.userFrom);
		}
	}
	else if (json.event == 111) {
		if (curUsername == json.userFor) {
			chatCont.style.display = "none";
			chatHeader.innerHTML = "";
			alert(json.userFrom + " has exited chat.");
		}
	}
}

function showChat()
{
	chatCont.classList.remove("chat-small");
	chatCont.classList.add("chat-large");

	chatHeader.innerHTML = "Chatting with " + userFrom;
	
	ws.send(JSON.stringify({
		'event': 100,
		'userFor': userFrom
	}));
}

function closeChat()
{
	chatCont.style.display = "none";
	chatCont.classList.remove("chat-large");
	
	ws.send(JSON.stringify({
		'event': 110,
		'username': userFrom
	}));
}

function startChat(username)
{
	ws.send(JSON.stringify({
		'event': 0,
		'userFor': username,
		'userFrom': curUsername
	}));
}