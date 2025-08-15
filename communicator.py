import requests
import os
import asyncio
from proxy_manager import ProxyManager

class Comunicador:
    def __init__(self):
        self.proxy_manager = ProxyManager()

    async def enviar_email(self, destino, asunto, cuerpo):
        try:
            respuesta = await asyncio.to_thread(
                requests.post,
                url=f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
                auth=("api", os.getenv("MAILGUN_API_KEY")),
                data={
                    "from": f"no-reply@{os.getenv('MAILGUN_DOMAIN')}",
                    "to": destino,
                    "subject": asunto,
                    "text": cuerpo
                },
                proxies=self.proxy_manager.next(),
                timeout=15
            )
            return respuesta.status_code == 200
        except:
            return False

    async def enviar_sms(self, numero, mensaje):
        # Implementación Twilio básica con proxy opcional
        from twilio.rest import Client
        client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))
        try:
            mensaje = await asyncio.to_thread(
                client.messages.create,
                body=mensaje,
                from_=os.getenv("TWILIO_NUMBER"),
                to=numero
            )
            return True
        except:
            return False

