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
	
	def receive(self, content, **kwargs):
		if self.message.user.username:
			event = content.get('event')
			
			if event == 0:
				user_for = content.get('userFor')
				
				consumers.get(user_for).send({
					'text': json.dumps({
						'event': 1,
						'userFor': user_for,
						'userFrom': self.message.user.username
					})
				})
			
			elif event == 100:
				user_for = content.get('userFor')

				consumers.get(user_for).send({
					'text': json.dumps({
						'event': 101,
						'userFor': user_for,
						'userFrom': self.message.user.username
					})
				})
			
			elif event == 110:
				username = content.get('username')
				
				consumers.get(username).send({
					'text': json.dumps({
						'event': 111,
						'userFor': username,
						'userFrom': self.message.user.username
					})
				})