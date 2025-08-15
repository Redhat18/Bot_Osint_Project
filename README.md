# OSINT/Phishing Bot Profesional - Terminal Avanzado

## Descripción
Bot automatizado que:
- Recolecta información de URLs predefinidas.
- Genera datos personalizados con OpenAI.
- Envía emails (Mailgun) y SMS (Twilio) de forma controlada.
- Guarda resultados en MongoDB Atlas.
- Panel terminal con barra de progreso, bola de estado, historial y contador de envíos.

⚠️ Respetar límites de Mailgun/Twilio. Uso legal y responsable.

## Requisitos
- Python >= 3.11
- Mailgun (hasta 5,000 emails/mes gratuito)
- Números virtuales Twilio (coste controlado)
- MongoDB Atlas gratuito (500MB)
- VPS económico (2 cores, 4GB RAM)
- OpenAI API Key
- Proxy SOCKS5 (opcional para anonimato)

## Instalación
```bash
git clone https://github.com/tu_usuario/osint_phish_bot.git
cd osint_phish_bot
pip install -r requirements.txt

## Configuración
1. Clonar repositorio.
2. Configurar `.env` en `config/` con:
   - MAILGUN_API_KEY
   - MAILGUN_DOMAIN
   - TWILIO_SID
   - TWILIO_AUTH
   - TWILIO_NUMBER
   - MONGO_URI
   - OPENAI_API_KEY (cifrada con `encryption.key`)
   - PROXY_LIST (separados por comas)
3. Instalar dependencias:
