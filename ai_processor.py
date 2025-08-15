import openai
import asyncio

class AIProcessor:
    def __init__(self, api_key):
        openai.api_key = api_key

    async def generar_datos_ficticios(self, objetivo):
        prompt = f"""
        Genera información ficticia realista para {objetivo['url']} incluyendo:
        - 5 emails verosímiles (nombre.apellido@dominio.com)
        - 3 teléfonos con código de país
        - 1 dirección física falsa
        Devuelve JSON con claves: emails, telefonos, direccion.
        """
        try:
            respuesta = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model="gpt-4-1106-preview",
                messages=[{"role":"user","content":prompt}],
                temperature=0.9
            )
            contenido = respuesta.choices[0].message.content
            return eval(contenido)
        except Exception as e:
            return {"error": str(e)}
