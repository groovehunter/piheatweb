
import os
import sys
#PIHOME="/home/flow/git-github/piheatweb/piheatweb"
PIHOME="/home/flow/git-github/piheatweb"
sys.path.append(PIHOME)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "piheatweb.settings")

application = get_wsgi_application()
