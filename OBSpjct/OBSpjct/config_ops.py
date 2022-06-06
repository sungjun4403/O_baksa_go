from pydoc import classname


class ConfigDEV():
    def __init__ (self):
        self.SECRET_KEY = 'django-insecure-uzu67ue$sed=%%($@-xisko&j4jgmk%!71%^48xdf*_e%&dtcr'
        self.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'database1',
                'USER' : 'root',
                'PASSWORD' : 'S!j3033212',
                'HOST' : '127.0.0.1',
                'PORT' : '3306',
                'OPTIONS': {
                            'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'"
                            },
            }
        }