import asyncio
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from ai_processor import AIProcessor
from communicator import Comunicador
from database import BaseDatos
from proxy_manager import ProxyManager
from usage_monitor import UsageMonitor
from key_manager import KeyManager

console = Console()

class BotOSINTPhish:
    def __init__(self):
        # Inicializamos gestores
        self.keys = KeyManager()
        self.ai = AIProcessor(self.keys.openai_key)
        self.com = Comunicador()
        self.db = BaseDatos()
        self.proxy_manager = ProxyManager()
        self.usage_monitor = UsageMonitor()
        self.running = True

    def mostrar_menu(self):
        console.print(Panel.fit("[bold red]BOT OSINT/PHISHING - PANEL ADMIN[/bold red]", border_style="red"))
        console.print("1. Iniciar ciclo automático")
        console.print("2. Generar identidades ficticias (GPT-4)")
        console.print("3. Ver estado del bot")
        console.print("4. Borrar base de datos")
        console.print("5. Auto-destrucción")
        console.print("0. Salir")

    async def iniciar_ciclo(self):
        console.print("[bold green]Iniciando ciclo automático...[/bold green]")
        while self.running:
            try:
                # Obtener URLs desde DB
                urls = self.db.obtener_urls()
                if not urls:
                    console.print("No hay URLs para procesar.")
                else:
                    tasks = []
                    for url_obj in urls:
                        tasks.append(self.procesar_objetivo(url_obj))
                    await asyncio.gather(*tasks)

            except Exception as e:
                console.print(f"[bold red]Error en ciclo:[/bold red] {e}")
            console.print("[bold yellow]Durmiendo 30 minutos...[/bold yellow]")
            await asyncio.sleep(1800)

    async def procesar_objetivo(self, objetivo):
        # Generar datos ficticios
        datos = await self.ai.generar_datos_ficticios(objetivo)
        guardado = self.db.guardar_datos_colectados({"url": objetivo['url'], "datos": datos})
        if not guardado:
            console.print(f"[yellow]No se pudo guardar datos de {objetivo['url']}[/yellow]")
            return

        # Enviar emails
        for email in datos.get("emails", []):
            if not self.usage_monitor.email_permitido():
                console.print(f"[red]Límite mensual de emails alcanzado.[/red]")
                break
            asunto, cuerpo = f"Actualización importante {objetivo['url']}", datos[email]
            await self.com.enviar_email(email, asunto, cuerpo)
            self.usage_monitor.email_enviado()

        # Enviar SMS
        for telefono in datos.get("telefonos", []):
            if not self.usage_monitor.sms_permitido():
                console.print(f"[red]Límite de SMS alcanzado.[/red]")
                break
            cuerpo = datos[telefono]
            await self.com.enviar_sms(telefono, cuerpo)
            self.usage_monitor.sms_enviado()

    def ver_estado(self):
        estado = "🟢 Activo" if self.running else "🔴 Detenido"
        console.print(Panel(f"[bold green]Estado del bot:[/bold green] {estado}", border_style="green"))
        console.print(f"Emails enviados este mes: {self.usage_monitor.emails_enviados}")
        console.print(f"SMS enviados este mes: {self.usage_monitor.sms_enviados}")

    def autodestruccion(self):
        console.print("[bold red]🚨 ACTIVANDO AUTODESTRUCCIÓN...[/bold red]")
        self.db.borrar_todo()
        if os.path.exists("logs/"):
            os.system("shred -u logs/*")
        sys.exit(0)

if __name__ == "__main__":
    bot = BotOSINTPhish()
    while bot.running:
        bot.mostrar_menu()
        opcion = input("> ")
        if opcion == "1":
            asyncio.run(bot.iniciar_ciclo())
        elif opcion == "2":
            console.print("Generación de identidades en progreso...")
            # Aquí podríamos pedir la URL de prueba y generar con AI
        elif opcion == "3":
            bot.ver_estado()
        elif opcion == "4":
            bot.db.borrar_todo()
        elif opcion == "5":
            bot.autodestruccion()
        elif opcion == "0":
            bot.running = False

