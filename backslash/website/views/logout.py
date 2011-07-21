from website import codejar

def handle(request):
    return codejar.auth.logout(request)
