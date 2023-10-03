from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.db.models import Count
from django.db.models import Exists
from django.conf import settings
# from pyproj import Proj, transform
from django.core import serializers
from decimal import Decimal
# from rdflib import Graph, Literal, RDF, URIRef, Namespace
# from rdflib.namespace import FOAF, XSD
import math

from django.core.files import File 
# import urllib.request
import os
# from PIL import Image

from .forms import * 
from .models import *

# import json
# import statistics
# import math

# import pickle
# import numpy as np
# import pandas as pd 
# from sklearn.tree import DecisionTreeRegressor

# from utils.mltools import * 
# from utils.generaltools import *

# Create your views here.

############# Table of Contents ############

# index and blank 
def index(request):
	pagetitle = 'title'

	template = loader.get_template('londonnet/index.html')

	manifestation_total = DigisigManifestationview.objects.count()
	seal_total = DigisigManifestationview.objects.distinct('fk_seal').count()
	item_total = DigisigManifestationview.objects.distinct('fk_item').count()
	catalogue_total = Digisigsealdescriptionview.objects.count()

	context = {
		'pagetitle': pagetitle,
		'manifestation_total': manifestation_total,
		'seal_total': seal_total,
		'item_total': item_total,
		'catalogue_total': catalogue_total, 
		}

	return HttpResponse(template.render(context, request))