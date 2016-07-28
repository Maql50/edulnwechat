import os  
import sys  
HERE_PATH_ABS = os.path.dirname(os.path.abspath(__file__))  
sys.path.append('%s/../' % HERE_PATH_ABS)  
os.environ['DJANGO_SETTINGS_MODULE'] = 'edulnwechat.settings'  
#import django.core.handlers.wsgi                          below django1.6  
#application = django.core.handlers.wsgi.WSGIHandler()  
from django.core.wsgi import get_wsgi_application         #upper django1.7  
application = get_wsgi_application()  
