from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Para formularios:
from django.forms import ModelForm
from .forms import ComentForm
#from django.core.context_processors import csrf #--> para versiones < django 1.10
from django.views.decorators import csrf

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Blog.models import Entrada, UserProfile, Comentario
# Create your views here.

def ListadoTitulos():
    listadoTitulos = Entrada.objects.all()[:10]
    return listadoTitulos


class ListadoHome(ListView):
	context_object_name = 'listadoEntradas'
	model = Entrada
	template_name = 'home.html'
	paginate_by = 4	#cuatro objetos por pagina

 	# En este formato, las palabras se acortan en el html con entrada.cuerpo|slice:":140"
	def get_context_data(self, **kwargs):
		context = super(ListadoHome, self).get_context_data(**kwargs)
		context['listadoTitulos'] = ListadoTitulos()
		return context

class VistaEntradaCompleta(DetailView):
	model = Entrada
	template_name = 'entradaCompleta.html'
	

	def get_context_data(self, **kwargs):
		context = super(VistaEntradaCompleta, self).get_context_data(**kwargs)
		context['listadoTitulos'] = ListadoTitulos()
		context['listadoComentarios'] = Comentario.objects.filter(id_message=self.kwargs['pk'])
		return context


class VistaSobreMi(TemplateView):
	template_name = 'sobreMi.html'

	def get_context_data(self, **kwargs):
		context = super(VistaSobreMi, self).get_context_data(**kwargs)
		context['listadoTitulos'] = ListadoTitulos()
		return context

class VistaCrearEntrada(CreateView):
	template_name = 'entradaForm.html'
	model = Entrada
	fields = ('titulo', 'cuerpo')
	success_url = '/' 

	def get_context_data(self, **kwargs):
		# Obtenemos el contexto de la clase base
		context = super(VistaCrearEntrada, self).get_context_data(**kwargs)
		# anyadimos nuevas variables de contexto al diccionario
		context['titulo'] = 'Crear articulo'
		context['nombre_btn'] = 'Crear'
		context['listadoTitulos'] = ListadoTitulos()
		# devolvemos el contexto
		return context

	def dispatch(self, request, *args, **kwargs):
		# obtenemos el contexto de la calse base
		# si no los tiene lo redirecciona a login 
		if not request.user.has_perms('blog.add_entrada'):
			return redirect(settings.LOGIN_URL)
		return super(VistaCrearEntrada, self).dispatch(request, *args, **kwargs)

	#def form_valid(self, form):
	#	messages.success(self.request, 'Entrada enviada correctamente')
	#	return super(VistaCrearEntrada, self).form_valid(form)


class VistaEntradaActualizar(UpdateView):
	template_name = 'entradaForm.html'
	model = Entrada
	fields = ('titulo', 'cuerpo')
	success_url = '/'

	def get_context_data(self, **kwargs):	
		# Obtenemos el contexto de la clase base
		context = super(VistaEntradaActualizar, self).get_context_data(**kwargs)
	    	# anyadimos nuevas variables de contexto al diccionario
		context['title'] = 'Editar articulo'
		context['nombre_btn'] = 'Editar'
		context['listadoTitulos'] = ListadoTitulos()
		# devolvemos el contexto
		return context

	def dispatch(self, request, *args, **kwargs):
    		if not request.user.has_perms('blog.change_entrada'):
        		return redirect(settigns.LOGIN_URL)
    		return super(VistaEntradaActualizar, self).dispatch(request, *args, **kwargs)

class VistaEntradaEliminar(DeleteView):
    template_name = 'confirmarEliminacion.html'
    success_url = '/'
    model = Entrada

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms('blog.delete_entrada'):
            return redirect(settings.LOGIN_URL)
        return super(VistaEntradaEliminar, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VistaEntradaEliminar, self).get_context_data(**kwargs)
        context['listadoTitulos'] = ListadoTitulos()
        # devolvemos el contexto
        return context


def comentario(request, pk):
	if  request.user.is_authenticated():
		if request.method == 'POST':
			form = ComentForm(request.POST)
			if form.is_valid():
				coment = form.save(commit=False)
				coment.author = request.user
				coment.published_date = datetime.now()
				coment.id_message = Entrada.objects.get(pk=pk)
				coment.save()
				return redirect('home:VistaEntradaCompleta', pk=pk)
		else:
			form = ComentForm()
		return render(request, 'comentario.html', {'form':form, 'listadoTitulos': ListadoTitulos()})
	else:
		return redirect('home:login')

###########################################################################################
##									USUARIO

def newUser(request):
	if request.method == 'POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			usuario = User.objects.get(username=form.cleaned_data['username'])
			user = UserProfile(usuario=usuario)
			user.save()
			return render(request, 'gracias.html', {'usuario': usuario})
	else:
		#si el method es GET, instanciamos un objeto RegistroUsuario vacio
		form=UserCreationForm()
	# Y mostramos los datos
	return render(request, 'registro.html', {'form':form, 'listadoTitulos': ListadoTitulos})



def acceso(request):
	if  request.user.is_authenticated():
		return redirect('/')
	mensaje=''
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			usuario = request.POST['username']
			password=request.POST['password']
			acceso=authenticate(username=usuario, password=password)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return redirect('/')
				else:
					return render(request, 'no_activo.html')
			else:
				return render(request, 'no_usuario.html')
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form, 'listadoTitulos': ListadoTitulos})

@login_required(login_url= 'login')
def VistaLogout(request):
	logout(request)
	return render(request, 'logout.html', {'listadoTitulos': ListadoTitulos})

	