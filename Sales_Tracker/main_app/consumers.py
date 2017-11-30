import json
from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer

class Consumer(JsonWebsocketConsumer):
	http_user = True

	def connect(self, message, **kwargs):
		message.reply_channel.send({'accept': True})
		Group('TEST').add(message.reply_channel)
		
		self.group_send('TEST', {
			'event': "User Entered",
			'username': message.user.username
		})

	def disconnect(self, message, **kwargs):
		message.reply_channel.send({'close': True})
		Group('TEST').discard(message.reply_channel)

		self.group_send('TEST', {
			'event': "User Left",
			'username': message.user.username
		})
	
	def recieve(self, content, **kwargs):
		return
