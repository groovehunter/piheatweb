import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) 
sys.path.append(BASE_DIR+'/sensors')
from piheatweb import settings as s  
dbs = s.DATABASES
from django.conf import settings
settings.configure(
    DATABASES=dbs,
    INSTALLED_APPS=(
        'sensors.apps.SensorsConfig', 
        )
    )
django.setup()
