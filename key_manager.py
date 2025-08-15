class UsageMonitor:
    def __init__(self):
        self.email_limit = 5000
        self.sms_limit = 2000
        self.emails_enviados = 0
        self.sms_enviados = 0

    def email_permitido(self):
        return self.emails_enviados < self.email_limit

    def sms_permitido(self):
        return self.sms_enviados < self.sms_limit

    def email_enviado(self):
        self.emails_enviados += 1

    def sms_enviado(self):
        self.sms_enviados += 1
