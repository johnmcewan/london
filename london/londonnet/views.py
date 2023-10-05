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
from utils.generaltools import *

# Create your views here.

############# Table of Contents ############

# index and blank

# information

# Discover

# Search
	# Actor

# Analyze

# Entity


#############################################

# index and blank 
def home(request):
	pagetitle = 'title'

	template = loader.get_template('londonnet/home.html')

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

#### ABOUT
def about(request):

	pagetitle = 'title'
	context = {
		'pagetitle': pagetitle,
	}
	template = loader.get_template('londonnet/about.html')					
	return HttpResponse(template.render(context, request))

### success
def success(request):
	pagetitle = 'title'
	context = {
		'pagetitle': pagetitle,
	}

	template = loader.get_template('londonnet/success.html')
	return HttpResponse(template.render(context, request))


### ajax
def ajax(request, digisig_entity_number):

	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		stuff = digisig_entity_number
		rdftext = rdf_generate(digisig_entity_number)
		print (rdftext)

		context = {
			'rdftext': rdftext,
			}
		return JsonResponse(context)
	return render(request, 'app/index.html')




######################### information ################################

def information(request, infotype):

	print (infotype)


########################### Discover ############################

def discover(request, discovertype):

	print (infotype)


#################### Search #########################
def search(request, searchtype):

	print(searchtype)

### Actor Search

	if searchtype == "actors":

		pagetitle = 'title'

		individual_object = Digisigindividualview.objects.all().order_by('group_name', 'descriptor_name')

		if request.method == "POST":
			form = PeopleForm(request.POST)
			if form.is_valid():
				qname = form.cleaned_data['name']	
				qpagination = form.cleaned_data['pagination']
				qgroup = form.cleaned_data['group']
				qclass = form.cleaned_data['personclass']
				qorder = form.cleaned_data['personorder']

				if qgroup.isdigit():
					qgroup = int(qgroup)
					if int(qgroup) == 2: individual_object = individual_object.filter(corporateentity=True)
					if int(qgroup) == 1: individual_object = individual_object.filter(corporateentity=False)

				if len(qname) > 0:
				 	individual_object = individual_object.filter(
				 		Q(group_name__icontains=qname) | Q(descriptor_name__icontains=qname) | Q(descriptor1__icontains=qname) | Q(descriptor2__icontains=qname) | Q(descriptor3__icontains=qname)
				 		)

				if qclass.isdigit():
					if int(qclass) > 0:
						qclass = int(qclass)
						individual_object = individual_object.filter(fk_group_class=qclass)

				if qorder.isdigit():
					if int(qorder) > 0:
						qorder = int(qorder)
						individual_object = individual_object.filter(fk_group_order=qorder)

				form = PeopleForm(request.POST)

		else:
			form = PeopleForm()
			qpagination = 1


	# preparing the data for individual_object
		qpaginationend = int(qpagination) * 10
		qpaginationstart = int(qpaginationend) -9 
		totalrows = len(individual_object)

		# if the dataset is less than the page limit
		if qpaginationend > totalrows:
			qpaginationend = totalrows

		if totalrows > 1:
			if qpaginationend < 10:
				print(totalrows)
			else:
				individual_object = individual_object[qpaginationstart:qpaginationend]
		totaldisplay = str(qpaginationstart) + " - " + str(qpaginationend)

		pagecountercurrent = qpagination
		pagecounternext = int(qpagination)+1
		pagecounternextnext = int(qpagination)+2

	# this code prepares the list of links to associated seals for each individual
		sealindividual = []
		for e in individual_object:
			testvalue = e.id_individual
			testseal = Seal.objects.filter(
				fk_individual_realizer=testvalue)

			for f in testseal:
				current_id_seal = f.id_seal
				sealindividual.append((testvalue, current_id_seal))

		context = {
			'pagetitle': pagetitle,
			'individual_object': individual_object,
			'sealindividual': sealindividual,
			'totalrows': totalrows,
			'totaldisplay': totaldisplay,
			'form': form,
			'pagecountercurrent': pagecountercurrent,
			'pagecounternext': pagecounternext,
			'pagecounternextnext': pagecounternextnext,
			}

		template = loader.get_template('londonnet/search_actor.html')
		return HttpResponse(template.render(context, request))


############################ Analyze #############################

def analyze(request, analysistype):

	print (analysistype)



############################## ENTITY #########################

def entity(request, digisig_entity_number):

	print(digisig_entity_number)

	#create flag that this is a view operation....
	operation = 1

	#item = 0, seal=1, manifestation=2, sealdescription=3, etc...
	targetphrase = redirectgenerator(digisig_entity_number, operation)

	print (targetphrase)

	return redirect(targetphrase)


def entity_fail(request, entity_phrase):
	pagetitle = 'title'

	print(entity_phrase)
	return HttpResponse("%s is not an entity I know about." % entity_phrase)


############################## actor #############################

def actor_page(request, digisig_entity_number):
	individual_object = get_object_or_404(Digisigindividual2view, id_individual=digisig_entity_number)

	pagetitle= namecompiler(digisig_entity_number)

	seal_objectset = Seal.objects.filter(
		Q(fk_individual_realizer=individual_object.id_individual) | Q(fk_actor_group=individual_object.id_individual)
	). order_by('fk_individual_office', 'fk_individual_realizer')

	sealnumber = len(seal_objectset)
	seal_object = []
	sealdescriptionset = []

	if (sealnumber > 0):
		for s in seal_objectset:
			current_id_seal = s.id_seal
			current_id_actor = s.fk_individual_realizer
			manifestation_instance = DigisigManifestationview.objects.filter(fk_seal = current_id_seal).order_by('id_representation')[:1]

			for c in manifestation_instance:
				representationid = c.id_representation
				if representationid is None:
					seal_object.append((s.id_seal, 'Null', 'Null', 'Null', 'Null', 'Null', s.fk_individual_realizer, s.datestart_seal, s.dateend_seal, s.fk_individual_office))
				else:
					seal_object.append((s.id_seal, c.thumb, c.representation_thumbnail, c.id_representation, c.medium, c.representation_filename, s.fk_individual_realizer, s.datestart_seal, s.dateend_seal, s.fk_individual_office))

			# this code prepares the list of descriptions associated to each seal

			sealdescription_object = Digisigsealdescriptionview.objects.filter(fk_seal=current_id_seal)
			for g in sealdescription_object:
				sealdescriptionset.append((current_id_seal, g.id_sealdescription, g.collection_shorttitle, g.sealdescription_identifier))	
				
	# list of relationships for each individual
	relationship_object = Digisigrelationshipview.objects.filter(fk_individual = digisig_entity_number)
	relationshipnumber = len(relationship_object)

	template = loader.get_template('londonnet/actor.html')
	context = {
		'pagetitle': pagetitle,
		'individual_object': individual_object,
		'seal_object': seal_object,
		'sealnumber': sealnumber,
		'relationship_object': relationship_object,
		'relationshipnumber' : relationshipnumber,
		'sealdescriptionset': sealdescriptionset,
		}

	return HttpResponse(template.render(context, request))



############################# edit operations ##############################

def edit(request, digisig_entity_number):

	print(digisig_entity_number)

	#create flag that this is an edit operation....
	operation = 2

	#item = 0, seal=1, manifestation=2, sealdescription=3, etc...
	targetphrase = redirectgenerator(digisig_entity_number, operation)

	print ("targetphrase", targetphrase)

	return redirect(targetphrase)


############## edit ACTOR from Seal Description
def edit_actor(request, digisig_entity_number):
	#some temp default data
	pagetitle = 'title'
	context = {
		'pagetitle': pagetitle,
	}
	template = loader.get_template('londonnet/index.html')


	if request.user.is_authenticated:
		authenticationstatus = "authenticated"

	if request.user.is_superuser == True:	
		finalcharacter = digisig_entity_number[7:]

		if finalcharacter == '3':

			### data for info screen -- template assumes drawing from view (copied from other template)-- retaining until get time to clean up
			sealdescription_object1 = get_object_or_404(Digisigsealdescriptionview, id_sealdescription=digisig_entity_number)
			sealdescription_object = get_object_or_404(Sealdescription, id_sealdescription=digisig_entity_number)
			pagetitle = sealdescription_object.fk_collection
			seal_object = sealdescription_object.fk_seal
			actor_object = seal_object.fk_individual_realizer

			#next record
			nextdescription = sealdescription_object1
			if sealdescription_object.catalogue_orderingnumber !=None:
				nextdescription= nextdescriptionget(sealdescription_object)

			# list of relationships for each individual
			relationship_object = Digisigrelationshipview.objects.filter(fk_individual = actor_object.id_individual)
			relationshipnumber = len(relationship_object)

			# events in question
			eventset = []
			manifestation_object = Manifestation.objects.filter(fk_face__fk_seal=sealdescription_object.fk_seal, fk_face__fk_faceterm=1)
			for m in manifestation_object:
				event1 = Event.objects.filter(part__support__manifestation__fk_support=m.fk_support)
				for e in event1:
					relatedparts = Part.objects.filter(fk_event=e.pk_event)
					for r in relatedparts:
						eventset.append([e.pk_event, e.startdate, e.enddate, r.pk_part, r.fk_item.id_item, r.reference_full])


			if request.method == 'POST':
				form = Sealdescription_actorForm(request.POST)
				if form.is_valid():
					print(form.cleaned_data)

					### revision to sealdescription title
					if len(form.cleaned_data['sealdescriptiontitle']) > 0:
						print ("revise title")
						sealdescription_object.sealdescription_title = form.cleaned_data['sealdescriptiontitle']
						sealdescription_object.save()

					### revision to actor identified with seal
					if form.cleaned_data['sealactor'] !=None:
						print ("revise actor")
						seal_object.fk_individual_realizer = Individual.objects.get(id_individual = form.cleaned_data['sealactor'])
						seal_object.save()

					#### add an actor
					newactor = form.cleaned_data['newactor']

					if newactor == True:
						i = Individual()
						if form.cleaned_data['newactortitle'].isdigit():
							i.fk_descriptor_title = Descriptor.objects.get(pk_descriptor = form.cleaned_data['newactortitle'])
						if form.cleaned_data['newactorname'].isdigit():
							i.fk_descriptor_name = Descriptor.objects.get(pk_descriptor = form.cleaned_data['newactorname'])
						if form.cleaned_data['newactorpref1'].isdigit():
							i.fk_descriptor_prefix1 = Prefix.objects.get(pk_prefix = form.cleaned_data['newactorpref1'])
						if form.cleaned_data['newactordescr1'].isdigit():
							i.fk_descriptor_descriptor1 = Descriptor.objects.get(pk_descriptor = form.cleaned_data['newactordescr1']) 
						if form.cleaned_data['newactorpref2'].isdigit():
							i.fk_descriptor_prefix2 = Prefix.objects.get(pk_prefix = form.cleaned_data['newactorpref2'])
						if form.cleaned_data['newactordescr2'].isdigit():
							i.fk_descriptor_descriptor2 = Descriptor.objects.get(pk_descriptor = form.cleaned_data['newactordescr2']) 
						if form.cleaned_data['newactorpref3'].isdigit():
							i.fk_descriptor_prefix3 = Prefix.objects.get(pk_prefix = form.cleaned_data['newactorpref3'])
						if form.cleaned_data['newactordescr3'].isdigit():
							i.fk_descriptor_descriptor3 = Descriptor.objects.get(pk_descriptor = form.cleaned_data['newactordescr3'])

						print("add individual")
						i.save()
						i.fullname_original = namecompiler(i.id_individual) 
						i.save()
						seal_object.fk_individual_realizer = Individual.objects.get(id_individual = i.id_individual)
						i.save()

						##associated new actor with the seal 
						seal_object.fk_individual_realizer = i
						seal_object.save()

						#### add a relationship -- but only if also adding a new actor!
						newrelationship = form.cleaned_data['addrelationship']

						if newrelationship == True:
							if form.cleaned_data['eventtarget'] !=None:
								print("add node")
								n = RelationshipNode()
								n.fk_event = Event.objects.get(pk_event=form.cleaned_data['eventtarget'])
								n.save()
								b1 = RelationshipBranch()
								b1.fk_relationshiprole = RelationshipRole.objects.get(pk_role=form.cleaned_data['roleactor1']) 
								b1.fk_individual = actor_object
								b1.fk_relationshipnode = n	
								b1.save()
								b2 = RelationshipBranch()
								b2.fk_relationshiprole = RelationshipRole.objects.get(pk_role=form.cleaned_data['roleactor2']) 
								b2.fk_individual = i
								b2.fk_relationshipnode = n
								b2.save()

					####Calling these again to refresh values after updates
					sealdescription_object1 = get_object_or_404(Digisigsealdescriptionview, id_sealdescription=digisig_entity_number)
					seal_object = sealdescription_object.fk_seal
					actor_object = seal_object.fk_individual_realizer

			##always blanking form so it does not carry over....		
			form = Sealdescription_actorForm()	

			### data for info screen -- template assumes drawing from view (copied from other template)-- retaining until get time to clean up
			### calling here to include updates from form
			sealdescription_object1 = get_object_or_404(Digisigsealdescriptionview, id_sealdescription=digisig_entity_number)

			template = loader.get_template('londonnet/edit_actor.html')
			context = {
			'pagetitle': pagetitle,
			'authenticationstatus': authenticationstatus,
			'sealdescription_object': sealdescription_object1,
			'seal_object': seal_object,
			'actor_object': actor_object,
			'relationship_object': relationship_object,
			'relationshipnumber' : relationshipnumber,
			'eventset': eventset,
			'nextdescription': nextdescription,
			'form': form,
			}

	return HttpResponse(template.render(context, request))



############################# data ##############################

def data(request, digisig_entity_number):
	filename = "digisig_" + str(digisig_entity_number) + ".txt"
	content = rdf_generate(digisig_entity_number)
	response = HttpResponse(content, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
	return response
