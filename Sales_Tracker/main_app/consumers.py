import json
from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer

# EVENTS #
# 0

# CONSUMERS #
consumers = {}

class Consumer(JsonWebsocketConsumer):
	http_user = True

	def connect(self, message, **kwargs):
		if message.user.username:
			message.reply_channel.send({'accept': True})
			Group('ALL').add(message.reply_channel)

			consumers[message.user.username] = message.reply_channel
			
			self.group_send('ALL', {
				'event': "User Entered",
				'username': message.user.username
			})
		else:
			message.reply_channel.send({'close': True})

	def disconnect(self, message, **kwargs):
		if message.user.username:
			message.reply_channel.send({'close': True})
			Group('ALL').discard(message.reply_channel)
	
	def recieve(self, content, **kwargs):
		event = content.get('event')

		print()
		print(event)
		print()

		if event == 0:
			username = content.get('username')

			print()
			print(consumers[username])
			print()

			consumers[username].send({
				'text': json.dumps({
					'event': 1,
					'userFor': username,
					'userFrom': self.user.username
				})
			})