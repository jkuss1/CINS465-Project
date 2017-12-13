import json
from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer

# EVENTS #
# 0:		Start Chat
# 1:		Send Alert to User
# 10:		User Closed Chat
# 11:		Alert User of Closed Chat
# 100:		Send Alert of Chat Accept
# 101:		Send Alert that Chat was Accepted
# 200:		User Sent Message
# 201:		Alert User of Message
# 1000:		User Left
# 1100:		User Already in Chat
# 1101:		User Already in Chat Reply
# 1200:		User Does not Wish to Chat

# CONSUMERS #
consumers = {}

class Consumer(JsonWebsocketConsumer):
	http_user = True

	def connect(self, message, **kwargs):
		if message.user.username:
			message.reply_channel.send({'accept': True})
			Group('ALL').add(message.reply_channel)
			
			message.user.settings.online = True
			message.user.settings.save()

			consumers[message.user.username] = {
				'reply_channel': message.reply_channel,
				'deny_chat': message.user.settings.deny_chat
			}
		else:
			message.reply_channel.send({'close': True})

	def disconnect(self, message, **kwargs):
		if message.user.username:
			message.reply_channel.send({'close': True})
			Group('ALL').discard(message.reply_channel)

			message.user.settings.online = False
			message.user.settings.save()
			
			self.group_send('ALL', {
				'event': 1000,
				'username': message.user.username
			})
	
	def receive(self, content, **kwargs):
		if self.message.user.username:
			event = content.get('event')
			
			if event == 0:
				user_for = content.get('userFor')
				consumer = consumers.get(user_for)
				
				if consumer and not consumer.get('deny_chat'):
					consumer.get('reply_channel').send({
						'text': json.dumps({
							'event': 1,
							'userFor': user_for,
							'userFrom': self.message.user.username
						})
					})
			
			elif event == 10:
				user_for = content.get('userFor')
				consumer = consumers.get(user_for)
				
				if consumer:
					consumer.get('reply_channel').send({
						'text': json.dumps({
							'event': 11,
							'userFor': user_for,
							'userFrom': self.message.user.username
						})
					})
			
			elif event == 100:
				user_for = content.get('userFor')
				consumer = consumers.get(user_for)

				if consumer:
					consumer.get('reply_channel').send({
						'text': json.dumps({
							'event': 101,
							'userFor': user_for,
							'userFrom': self.message.user.username
						})
					})
			
			elif event == 200:
				user_for = content.get('userFor')
				consumer = consumers.get(user_for)

				if consumer:
					consumer.get('reply_channel').send({
						'text': json.dumps({
							'event': 201,
							'userFor': user_for,
							'userFrom': self.message.user.username,
							'text': content.get('text')
						})
					})
			
			elif event == 1100:
				user_for = content.get('userFor')
				consumer = consumers.get(user_for)

				if consumer:
					consumer.get('reply_channel').send({
						'text': json.dumps({
							'event': 1101,
							'userFor': user_for,
							'userFrom': self.message.user.username
						})
					})