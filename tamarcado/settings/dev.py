from tamarcado.settings.base import *

DEBUG = True
ALLOWED_HOSTS = []
LOGGING = {
    **LOGGING,
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}
# Configuração para MailHog (desenvolvimento)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '127.0.0.1'  # Ou 'localhost', dependendo de como está configurado
EMAIL_PORT = 1025
EMAIL_USE_TLS = False  # MailHog não exige TLS
EMAIL_HOST_USER = 'apikey'



