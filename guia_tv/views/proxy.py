import requests
from django.http import StreamingHttpResponse, Http404
from django.shortcuts import get_object_or_404
from guia_tv.models import Channel  # Ajusta según la ubicación de tu modelo de canales


def stream_proxy(request, channel_id):
    """
    Actúa como un túnel (proxy) entre el navegador y el servidor de origen M3U8/HLS.
    Inyecta cabeceras CORS y permite transmitir streams HTTP sobre conexiones HTTPS.
    """
    # 1. Recuperar el canal desde la base de datos
    channel = get_object_or_404(Channel, pk=channel_id)
    
    # Obtener la URL (ajusta 'stream_url' si en tu modelo el campo se llama distinto)
    stream_url = getattr(channel, 'stream_url', None)
    if not stream_url and hasattr(channel, 'streams'):
        active_stream = channel.streams.filter(is_online=True).first()
        stream_url = active_stream.url if active_stream else None

    if not stream_url:
        raise Http404("El canal no tiene una URL de transmisión válida.")

    # 2. Simular un navegador para evitar bloqueos del servidor de origen
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    try:
        # 3. Petición en streaming hacia la fuente original IPTV
        r = requests.get(stream_url, headers=headers, stream=True, timeout=8)
        r.raise_for_status()

        # 4. Transmitir el contenido por fragmentos (chunks)
        response = StreamingHttpResponse(
            r.iter_content(chunk_size=8192),
            content_type=r.headers.get('Content-Type', 'application/x-mpegURL'),
            status=r.status_code
        )

        # 5. Inyectar cabeceras CORS permisivas para Video.js / HLS.js
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "*"

        return response

    except requests.RequestException as e:
        # Si la fuente de origen no responde o da timeout
        raise Http404(f"No se pudo conectar con el servidor del canal: {e}")