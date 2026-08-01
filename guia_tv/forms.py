from django import forms

from guia_tv.domain.value_objects.license_status import LicenseStatus
from guia_tv.models import Category, Channel, Country, Language

# Solo se ofrecen estos dos estados en el formulario: "rejected" no tiene
# sentido elegirlo a mano, y "pending" no aplica porque este formulario
# es exclusivamente para publicar un canal ya revisado.
_choice_labels = dict(LicenseStatus.choices())

_PUBLISHABLE_CHOICES = [
    (status.value, _choice_labels[status.value])
    for status in LicenseStatus
    if status.is_publishable
]


class AddChannelForm(forms.Form):

    name = forms.CharField(
        label="Nombre del canal",
        max_length=200,
    )

    stream_url = forms.URLField(
        label="URL del stream (.m3u8, etc.)",
        max_length=1000,
    )

    website = forms.URLField(
        label="Sitio web oficial del canal",
        required=False,
        help_text="Ayuda a verificar que el stream sea legítimo.",
    )

    logo_url = forms.URLField(
        label="URL del logo",
        required=False,
    )

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="País",
    )

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        required=False,
        label="Idioma",
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Categoría",
    )

    quality = forms.ChoiceField(
        choices=Channel.QUALITY_CHOICES,
        initial="HD",
        label="Calidad",
    )

    license_status = forms.ChoiceField(
        choices=_PUBLISHABLE_CHOICES,
        label="Estado de licencia",
        help_text=(
            "Elegí 'Oficial' si el stream lo publica el propio canal/"
            "organismo, o 'Dominio público' si el contenido tiene "
            "licencia abierta (Creative Commons u equivalente)."
        ),
    )

    license_note = forms.CharField(
        label="Justificación de la licencia",
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=(
            "Obligatorio. Ej: 'Stream oficial embebible publicado en "
            "canaltal.cl/en-vivo' o 'Transmisión de TV Senado, canal "
            "estatal de acceso público'."
        ),
    )

    skip_url_check = forms.BooleanField(
        label="Omitir verificación automática de la URL",
        required=False,
        help_text=(
            "Marcalo solo si sabés que el servidor bloquea peticiones "
            "HEAD y por eso la verificación da un falso negativo."
        ),
    )
