from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Entrada(models.Model):
	titulo = models.CharField(max_length = 100)
	cuerpo = models.TextField()
	fecha = models.DateTimeField(default = datetime.now, blank=True)

	def __str__(self):
			return self.titulo


class Comentario(models.Model):
		date = models.DateTimeField(default= datetime.now)
		author = models.ForeignKey(User)
		Texto_Comentario = models.TextField()
		id_message = models.ForeignKey(Entrada)

		def __str__(self):
			return "%s %s " % (self.id_message, self.Texto_Comentario[:60])

class UserProfile(models.Model):
	usuario = models.OneToOneField(settings.AUTH_USER_MODEL)

	def __unicode__(self):
		return self.usuario.username