from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def redirect_to_streamlit(request):
    if request.user.is_authenticated:
        username = request.user.username
        return redirect(f'http://localhost:8501/?username={username}')
    else:
        return redirect('/')
