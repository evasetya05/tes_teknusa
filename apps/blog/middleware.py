import datetime
import time
from ipware import get_client_ip
from teknusa.utils import cache
from blog.documents import ELASTICSEARCH_ENABLED, ElapsedTimeDocumentManager


class OnlineMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)

        # Ambil User-Agent
        http_user_agent = request.META.get('HTTP_USER_AGENT', [])

        # Abaikan spider/crawler
        if 'Spider' in http_user_agent or 'spider' in http_user_agent:
            return response

        try:
            # Hitung waktu response
            cast_time = time.time() - start_time

            # Ambil IP client
            client_ip, is_routable = get_client_ip(request)
            # client_ip bisa None jika tidak ditemukan

            if ELASTICSEARCH_ENABLED:
                time_taken = round((cast_time) * 1000, 2)
                url = request.path
                from django.utils import timezone

                ElaspedTimeDocumentManager.create(
                    url=url,
                    time_taken=time_taken,
                    log_datetime=timezone.now(),
                    type='blog',
                    useragent=http_user_agent
                    # Bisa tambahkan IP jika mau
                    # ip=client_ip
                )

            response.content = response.content.replace(
                b'<!!LOAD_TIMES!!>',
                str.encode(str(cast_time)[:5])
            )

        except Exception as e:
            # Bisa log error jika perlu
            pass

        return response
