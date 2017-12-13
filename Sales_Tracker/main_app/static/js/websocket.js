var ws = new WebSocket("ws://" + window.location.host);

var chatCont = document.getElementById("chat-cont");
var chatHeader = document.getElementById("chat-header");
var chatBody = document.getElementById("chat-body");
var chatHeaderBtns =
	"<button id=\"chat-accept\" class=\"button\" onclick=\"showChat()\">Y</button>" +
	"<button id=\"chat-decline\" class=\"button bg-red\" onclick=\"closeChat()\">N</button>";

var acceptedChat = false;
var inChat = false;
var chattingWith;

ws.onmessage = function(message)
{
	var json = JSON.parse(message.data);

	console.log(json);
	
	if (json.event == 1) {
		if (curUsername == json.userFor) {
			if (!inChat) {
				chatCont.style.display = "inline";
				chatCont.classList.add("chat-small");
				chatHeader.innerHTML = json.userFrom + " would like to chat.&nbsp;" + chatHeaderBtns;
				inChat = true;
				chattingWith = json.userFrom;
			}
			else {
				ws.send(JSON.stringify({
					"event": 1100,
					"userFor": json.userFrom,
					"userFrom": curUsername
				}));
			}
		}
	}
	else if (json.event == 11) {
		if (curUsername == json.userFor) {
			if (acceptedChat) {
				alert(json.userFrom + " has exited chat.");
			}
			
			clearChat();
		}
	}
	else if (json.event == 101) {
		if (curUsername == json.userFor) {
			chatCont.style.display = "inline";
			chatCont.classList.add("chat-large");
			chatHeader.innerHTML = "Chatting with " + json.userFrom;
		}
	}
	else if (json.event == 201) {
		if (curUsername == json.userFor) {
			createNewChatMsg(false, json.userFrom, json.text);
		}
	}
	else if (json.event == 1000) {
		if (chattingWith == json.username) {
			if (acceptedChat) {
				alert(json.username + " has exited chat.");
			}
			
			clearChat();
		}
	}
	else if (json.event == 1101) {
		if (curUsername == json.userFor) {
			alert(json.userFrom + " is already in chat.\nPlease try again later.");
			clearChat();
		}
	}
}

function showChat()
{
	chatCont.classList.remove("chat-small");
	chatCont.classList.add("chat-large");
	chatHeader.innerHTML = "Chatting with " + chattingWith;

	acceptedChat = true;
	
	ws.send(JSON.stringify({
		"event": 100,
		"userFor": chattingWith
	}));

	inChat = true;
}

function closeChat()
{
	ws.send(JSON.stringify({
		"event": 10,
		"userFor": chattingWith
	}));

	clearChat();
}

function startChat(username)
{
	if (!inChat) {
		chatCont.style.display = "inline";
		chatCont.classList.add("chat-small");
		chatHeader.innerHTML = "Waiting for Reply from " + username;

		acceptedChat = true;
		inChat = true;
		chattingWith = username;

		ws.send(JSON.stringify({
			"event": 0,
			"userFor": username,
			"userFrom": curUsername
		}));
	}
	else {
		alert("You're already in a chat.\nClose your current chat and try again.");
	}
}

function sendMsg()
{
	var chatMsgInput = document.getElementById("chat-msg-input");

	if (chatMsgInput.value != "") {
		ws.send(JSON.stringify({
			"event": 200,
			"userFor": chattingWith,
			"userFrom": curUsername,
			"text": chatMsgInput.value
		}));
		
		createNewChatMsg(true);
		
		chatMsgInput.value = "";
	}
}

function createNewChatMsg(fromCurUser, user, messageText)
{
	var chatMsgDiv = document.createElement("div");
	chatMsgDiv.classList.add("chat-msg");
	if (fromCurUser) {chatMsgDiv.classList.add("chat-msg-user");}
	chatBody.appendChild(chatMsgDiv);
	
	var chatMsgText = document.createElement("div");
	chatMsgText.classList.add("chat-msg-text");

	if (fromCurUser) {
		chatMsgText.innerHTML = document.getElementById("chat-msg-input").value;
	}
	else {
		chatMsgText.innerHTML = messageText;
	}

	chatMsgDiv.appendChild(chatMsgText);

	var chatMsgName = document.createElement("div");
	chatMsgName.classList.add("chat-msg-name");

	if (fromCurUser) {
		chatMsgName.innerHTML = curUsername;
	}
	else {
		chatMsgName.innerHTML = user;
	}
	
	chatMsgDiv.appendChild(chatMsgName);

	chatBody.scrollTop = chatBody.scrollHeight;
}

function clearChat()
{
	chatCont.classList.remove("chat-large");
	chatCont.style.display = "none";
	chatHeader.innerHTML = "";
	chatBody.innerHTML = "";
	acceptedChat = false;
	inChat = false;
	chattingWith = null;
}