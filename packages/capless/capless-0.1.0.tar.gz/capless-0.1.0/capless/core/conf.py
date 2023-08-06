from envs import env
from cappy.utils import import_mod


class Settings(object):

    INSTALLED_APPS = env('INSTALLED_APPS',[],var_type='list')
    DATABASES = env('DATABASES',{},var_type='dict')
    DEBUG = env('DEBUG',False,var_type='boolean')

    AUTH_BACKENDS = env('AUTH_BACKENDS',
        ['cappy.auth.backends.CognitoUserPoolAuth'],var_type='list')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

    def __init__(self):
        self.settings_mod = import_mod(
            env('CAPPY_SETTINGS_MODULE'))
        self.parse_settings_mod()

    def list_commands(self):
        pass


    def parse_settings_mod(self):
        for k, v in self.settings_mod.__dict__.items():
            if k not in ('__builtins__', '__file__',
                         '__package__', '__name__', '__doc__'):
                setattr(self,k,v)


settings = Settings()