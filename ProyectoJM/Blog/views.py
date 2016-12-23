from django.shortcuts import render

from Blog.models import Noticia, Categoria, Comentario #para utilizar los modelos de blog
from django.contrib.auth.models import User	#para porder usar los datos del modelo usuario
from django.shortcuts impor render_to_response, get_object_or_404 #1- para plantillas y 2- lanzar un error
from django.http import HttpResponse



# Create your views here.

def index(request):
	return HttpResponse("Hola, soy tu primera vista")


#def insertar_noticia(request):


#def insertar_categoria(request):


