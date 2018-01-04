import numpy as np
import os, errno, sys
from bs4 import BeautifulSoup
from requests import get
from textblob import TextBlob
import pandas as pd
from pyteaser import Summarize
from django.utils.encoding import smart_str, smart_unicode


proj_path = "/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manatwee.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from twttr.models import *
from critic.models import *

try:
    import hollywood_reporter
except:
    print 'hwr failed'
try:
    import NYT
except:
    print 'nyt failed'
try:
    import indiewire
except:
    print 'indiewire failed'
try:
    import variety
except:
    print 'variety failed'

try:
    import chicagotribune
except:
    print 'chicagotribune failed'
