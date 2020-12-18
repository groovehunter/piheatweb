
import os
import sys
PIHEAT='/home/pi/piheat/piheatweb'
sys.path.append(PIHEAT)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "piheatweb.settings")

application = get_wsgi_application()
