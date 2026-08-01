# Generado a mano siguiendo el formato de las migraciones anteriores
# (Django 5.0.3). Agrega el sistema de licencias: license_status /
# license_note en Channel e IPTVSource, con default "pending" para no
# publicar automáticamente lo ya existente en la base sin revisión.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guia_tv', '0006_channel_audio_codec_channel_bitrate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='license_note',
            field=models.TextField(
                blank=True,
                help_text='De dónde sale la autorización para transmitir este canal.',
            ),
        ),
        migrations.AddField(
            model_name='channel',
            name='license_status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pendiente de revisión'),
                    ('official', 'Oficial del canal/organismo'),
                    ('public_domain', 'Dominio público / licencia abierta'),
                    ('rejected', 'Rechazado (posibles derechos de autor)'),
                ],
                default='pending',
                help_text="Solo los canales 'official' o 'public_domain' deberían quedar visibles públicamente.",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='iptvsource',
            name='license_note',
            field=models.TextField(
                blank=True,
                help_text='Justificación de por qué esta fuente es confiable.',
            ),
        ),
        migrations.AddField(
            model_name='iptvsource',
            name='license_status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pendiente de revisión'),
                    ('official', 'Oficial del canal/organismo'),
                    ('public_domain', 'Dominio público / licencia abierta'),
                    ('rejected', 'Rechazado (posibles derechos de autor)'),
                ],
                default='pending',
                help_text="Una fuente nueva arranca en 'pending' y NO se sincroniza automáticamente hasta que alguien confirme que sus canales están autorizados (official/public_domain).",
                max_length=20,
            ),
        ),
        migrations.AddIndex(
            model_name='channel',
            index=models.Index(fields=['license_status'], name='guia_tv_cha_license_9f6f39_idx'),
        ),
    ]
