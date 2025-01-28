from tamarcado.settings.base import *


DEBUG = True
ALLOWED_HOSTS=[]
LOGGING ={
    **LOGGING,
    'loggers':{
      '':{
          'level':'DEBUG',
          'handlers':['console','file']
      }      
    }
}
