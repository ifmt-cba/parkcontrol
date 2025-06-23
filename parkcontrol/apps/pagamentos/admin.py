from django.contrib import admin
from apps.pagamentos.models import CobrancaDiaria, CobrancaMensalista

admin.site.register(CobrancaDiaria)
admin.site.register(CobrancaMensalista)  # Assuming the model is named CobrancaMensalista