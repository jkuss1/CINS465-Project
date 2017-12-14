from .models import *

def processors(request):
    if request.user.username and not AccountSettings.objects.filter(user=request.user):
        AccountSettings.objects.create(
            user = request.user,
            deny_chat = False,
            online = True,
        )
    
    deny_chat = "false"

    if request.user.username:
        if request.user.settings.deny_chat:
            deny_chat = "true"
    
    return {
        'website_name': "Sales Tracker",
        'username': request.user.username,
        'deny_chat': deny_chat
    }