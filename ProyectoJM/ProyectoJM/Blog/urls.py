from django.conf.urls import url

from . import views


app_name= 'appJM'
urlpatterns = [ 
	url(r'^$', views.ListadoHome.as_view(), name = 'home'),
	url(r'^entrada/(?P<pk>.*)$', views.VistaEntradaCompleta.as_view(), name='VistaEntradaCompleta'),
	url(r'^sobreMi/$', views.VistaSobreMi.as_view(), name = 'sobreMi'),
	url(r'^crear/$', views.VistaCrearEntrada.as_view(), name = 'crear'),
	url(r'^editar/(?P<pk>.*)$', views.VistaEntradaActualizar.as_view(), name= 'editar'),
	url(r'^eliminar/(?P<pk>.*)$', views.VistaEntradaEliminar.as_view(), name= 'eliminar'),
	url(r'^registro/$', views.newUser, name = 'registro'),
	url(r'^login/$', views.acceso, name = 'login'),
	url(r'^logout/$', views.VistaLogout, name = 'logout'),
	url(r'^comentario/(?P<pk>.*)$', views.comentario, name = 'comentario'),
	]