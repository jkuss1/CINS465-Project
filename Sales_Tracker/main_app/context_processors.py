def processors(request):
    deny_chat = "false"

    if request.user.username:
        if request.user.settings.deny_chat:
            deny_chat = "true"
    
    return {
        'website_name': "Sales Tracker",
        'username': request.user.username,
        'deny_chat': deny_chat
    }