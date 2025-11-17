from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return HttpResponse('<h2>Добро пожаловать в Food App!<br>Используйте <a href="/accounts/signup/">регистрацию</a> или <a href="/accounts/login/">вход</a>.</h2>')
