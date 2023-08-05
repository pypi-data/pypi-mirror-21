====
django-grafico-db
====

Para poder ejecutar la aplicacion deberas instalar django-extensions y grafico-db
en INSTALLED_APPS en tu archivo settings.py

INSTALLED_APPS = (
    ...
    'django_extensions',
	'grafico-db',
	...
)

Escribe el siguiente codigo en settings.py

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

Incluye la url de la aplicacion en tu archivo urls.py

url(r'^myblog/', include('grafico_db.urls'))
