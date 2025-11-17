import os
import sys

# Add the parent directory (project root) to the sys.path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Add the apps directory to sys.path
apps_path = os.path.join(project_root, 'apps')
sys.path.insert(0, apps_path)

# Set the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teknusa.settings.production")

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()
