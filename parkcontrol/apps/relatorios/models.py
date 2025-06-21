from django.db import models
from django.conf import settings

class RelatorioFinanceiro(models.Model):
    STATUS_CHOICES = [
        ('Rascunho', 'Rascunho'),
        ('Finalizado', 'Finalizado'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome do Relatório")
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="relatorios_criados")
    data_inicio = models.DateField(verbose_name="Data Inicial")
    data_fim = models.DateField(verbose_name="Data Final")
    data_criacao = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Rascunho")

    total_emitido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_inadimplente = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    arquivo_pdf = models.FileField(upload_to="relatorios_pdfs/", null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.status}) - {self.data_criacao.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = "Relatório Financeiro"
        verbose_name_plural = "Relatórios Financeiros"
