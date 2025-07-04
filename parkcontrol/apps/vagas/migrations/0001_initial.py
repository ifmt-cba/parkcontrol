# Generated by Django 4.2.23 on 2025-06-15 23:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EntradaVeiculo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                (
                    "tipo_cliente",
                    models.CharField(
                        choices=[
                            ("Mensalista", "Mensalista"),
                            ("Diarista", "Diarista"),
                        ],
                        max_length=12,
                    ),
                ),
                (
                    "placa",
                    models.CharField(
                        max_length=10,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[A-Z]{3}[0-9][A-Z][0-9]{2}$",
                                "Placa no formato inválido (ex: ABC1D23 - padrão Mercosul)",
                            )
                        ],
                    ),
                ),
                (
                    "tipo_veiculo",
                    models.CharField(
                        choices=[("Carro", "Carro"), ("Moto", "Moto")], max_length=10
                    ),
                ),
                (
                    "horario_entrada",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vaga",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Livre", "Livre"),
                            ("Manutenção", "Manutenção"),
                            ("Ocupada", "Ocupada"),
                        ],
                        default="Livre",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SolicitacaoManutencao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero_vaga", models.CharField(max_length=10)),
                ("descricao", models.TextField()),
                ("data_solicitacao", models.DateTimeField(auto_now_add=True)),
                ("resolvido", models.BooleanField(default=False)),
                (
                    "solicitante",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SaidaVeiculo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "placa",
                    models.CharField(
                        max_length=10,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[A-Z]{3}[0-9][A-Z][0-9]{2}$",
                                "Placa no formato inválido (ex: ABC1D23 - padrão Mercosul)",
                            )
                        ],
                    ),
                ),
                (
                    "tipo_veiculo",
                    models.CharField(
                        choices=[("Carro", "Carro"), ("Moto", "Moto")], max_length=10
                    ),
                ),
                (
                    "tipo_cliente",
                    models.CharField(
                        choices=[
                            ("Mensalista", "Mensalista"),
                            ("Diarista", "Diarista"),
                        ],
                        max_length=12,
                    ),
                ),
                ("tempo_permanencia", models.DurationField(blank=True, null=True)),
                (
                    "horario_saida",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "valor_total",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0, max_digits=8, null=True
                    ),
                ),
                (
                    "entrada",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="saidas",
                        to="vagas.entradaveiculo",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="entradaveiculo",
            name="vaga",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="entradas",
                to="vagas.vaga",
            ),
        ),
    ]
