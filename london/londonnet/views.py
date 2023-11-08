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
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD
import math

from django.core.files import File 
# import urllib.request
import os
from PIL import Image

from .forms import * 
from .models import *

import json
import statistics
import math

# import pickle
# import numpy as np
# import pandas as pd 
# from sklearn.tree import DecisionTreeRegressor

# from utils.mltools import * 
from utils.generaltools import *

# Create your views here.

############# Table of Contents ############

# index and blank
# about
# success
# Ajax

# information
	# Government
	# Alderman

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

	# individual_set = Individual.objects.filter(
	# 	fk_individual_event__Event__Location_reference__Locationname__Location__fk_region=87).count()	

	actor_total = Individual.objects.filter(
		fk_individual_event__fk_event__locationreference__fk_locationname__fk_location__fk_region=87).distinct('id_individual').count()	

	references = Referenceindividual.objects.filter(fk_event__locationreference__fk_locationname__fk_location__fk_region=87).exclude(fk_individual=10000019)
	reference_total = references.count()

	event_total = Referenceindividual.objects.filter(fk_event__locationreference__fk_locationname__fk_location__fk_region=87).exclude(fk_individual=10000019).distinct('fk_event').count()

	references_events = references.values("fk_event")
	eventset = Event.objects.filter(pk_event__in=references_events)
	record_total = Item.objects.filter(part__fk_event__in=eventset).distinct().count()


	context = {
		'pagetitle': pagetitle,
		'actor_total': actor_total,
		'reference_total': reference_total,
		'event_total': event_total,
		'record_total': record_total
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
	return render(request, 'app/home.html')


######################### information ################################

def information(request, infotype):

	print (infotype)


########################### Civic Government #########################
	if infotype == "info_government":

		pagetitle = 'Government'

		#default
		groupnumber= 927
		timegroupCnumber= 4

		#adjust values if form submitted
		if request.method == 'POST':
			form = GovernmentForm(request.POST)
			
			if form.is_valid():
				groupnumber = form.cleaned_data['group_name']
				timegroupCnumber = form.cleaned_data['timegroupC']

		group_name = get_object_or_404(Groupname, id_group=groupnumber)
		individual = get_object_or_404(Individual, fk_group=group_name.id_group)
		officialreferenceset = Referenceindividual.objects.filter(fk_individual2=individual.id_individual)

		#print("Length", len(officialreferenceset))
		
		## List of office holders -- find nodes then branches		
		#nodeofficeholderset = RelationshipNode.objects.filter(relationshipbranch__fk_individual=individual)
		# branchofficeholderset = RelationshipBranch.objects.filter(
		# 	fk_relationshipnode__in=nodeofficeholderset).exclude(
		# 	fk_individual=individual).order_by(
		# 	# 'fk_individual__fullname_modern')
		# 	'fk_relationshipnode__start_year')

		branchofficeholderset = officeholders(individual)

		data1 = []
		labels1 = []

		## temp function to see how many cases we have per year
		for b in branchofficeholderset:

			try:
				start = b.fk_relationshipnode.start_year
				end = b.fk_relationshipnode.end_year + 1
				labels = b.fk_individual.id_individual

				if (end > 1199 and start < 1230):
					data1.append([start, end])
					labels1.append(labels)

			except:
				miss = 1
				#print ("no value", b.fk_individual.fullname_original)

		yearreport = {}

		for y in range(1200, 1300):
			count = 0
			report = {}
			people = ""
			
			for b in branchofficeholderset:
				try:
					start = b.fk_relationshipnode.start_year
					end = b.fk_relationshipnode.end_year
					if (y >= start and y <= end):
						count = count +1
						people = people + "\n" + str(b.fk_individual.fullname_original)
						report = {
							"count": count,
							"people": people
						}

				except:
					miss= 1
					#print ("no value", b.fk_individual.fullname_original)
			

			yearreport[y] = report

		# print ("here is the report", yearreport)

		# officer_report = []

		# for i in branchofficeholderset:
		#  	officereferences = Referenceindividual.objects.filter(fk_individual=i.fk_individual, fk_individual2=individual.id_individual).exclude(fk_referencerole=5).order_by('fk_event__startdate')

	 	# 	firstdate, firstdateprecision, finaldate, finaldateprecision = dateactive(officereferences)

	 	# 	#print (i.fk_individual.fullname_original, firstdate, finaldate)
	 	# 	officer_report.append(str(firstdate) + " " + str(finaldate))

	 		# # print (i.fk_individual.fullname_original, o.fk_event.startdate)
		 	# report.append(str(i.fk_individual.fullname_original) + " " + str(o.fk_event.startdate) + " " + str(o.fk_event.enddate))



		form = GovernmentForm()		
		context = {
			'pagetitle': pagetitle,
			'group_name': group_name,
			# 'nodeofficeholderset': nodeofficeholderset, 
			'branchofficeholderset': branchofficeholderset,
			# 'officer_report': officer_report,
			'data1': data1,
			'labels1': labels1,
		}
			
		template = loader.get_template('londonnet/info_government.html')					
		return HttpResponse(template.render(context, request))

################### Alderman ############################
	if infotype == "info_aldermen":

		pagetitle = 'Aldermen'

		#default
		groupnumber= 927
		timegroupCnumber= 4
		alderman_selected = 10000029

		#adjust values if form submitted
		if request.method == 'POST':
			form = GovernmentForm(request.POST)
			
			if form.is_valid():
				groupnumber = form.cleaned_data['group_name']
				timegroupCnumber = form.cleaned_data['timegroupC']
				alderman_selected = form.cleaned_data['alderman_name']

		individual_info = get_object_or_404(Individual, id_individual=alderman_selected)
		print (individual_info)

		references_set = Referenceindividual.objects.filter(fk_individual=alderman_selected)
		references_count = references_set.count()

		references_alderman = references_set.filter(Q(fk_individual2 = 10140149) | Q(fk_individual3 = 10140149))
		references_alderman_count = references_alderman.count()

		references_alderman_event = references_alderman.values("fk_event")

		# for r in references_alderman:
		# 	print (r.fk_event)

		eventset = Event.objects.filter(pk_event__in=references_alderman_event)

		print ("eventsetcount", (eventset.count()))
		# for event in eventset:
		# 	print (event)

		locationset1 = Locationreference.objects.filter(fk_event__in=eventset).order_by("fk_event__startdate")

		#map points
		#data for location map
		locationset = Location.objects.filter(
			Q(locationname__locationreference__fk_event__in=eventset)).annotate(count=Count('locationname__locationreference__fk_event'))
		location_dict, center_long, center_lat = mapgenerator2(locationset)

		#data for region map 
		regiondisplayset = Regiondisplay.objects.filter( 
			region__location__locationname__locationreference__fk_locationstatus=1, 
			region__location__locationname__locationreference__fk_event__in=eventset
			).annotate(numregions=Count('region__location__locationname__locationreference'))

		region_dict = mapgenerator3(regiondisplayset)
 
		# print (location_dict)


		form = GovernmentForm()
		context = {
			'pagetitle': pagetitle,
			'individual_info': individual_info,
			'references_set': references_set, 
			'references_count': references_count,
			'references_alderman': references_alderman,
			'references_alderman_count': references_alderman_count,
			'region_dict': region_dict,
			'location_dict': location_dict,
			'locationset1': locationset1,
			# # 'officer_report': officer_report,
			# 'data1': data1,
			# 'labels1': labels1,
			'form': form,
		}
			
		template = loader.get_template('londonnet/info_aldermen.html')					
		return HttpResponse(template.render(context, request))

########################### Discover ############################

def discover(request, discovertype):

	print (infotype)


#################### Search #########################
def search(request, searchtype):

	print(searchtype)

	############### Actor Search

	if searchtype == "actors":

		pagetitle = 'title'

		actor_object = Individual.objects.filter(
		fk_individual_event__fk_event__locationreference__fk_locationname__fk_location__fk_region=87).order_by(
		'fk_descriptor_name__descriptor_modern', 'fk_descriptor_descriptor1__descriptor_modern', 'fk_descriptor_descriptor2__descriptor_modern','fk_descriptor_descriptor3__descriptor_modern','id_individual').distinct(
		'fk_descriptor_name__descriptor_modern', 'fk_descriptor_descriptor1__descriptor_modern', 'fk_descriptor_descriptor2__descriptor_modern','fk_descriptor_descriptor3__descriptor_modern','id_individual')

		if request.method == "POST":
			form = PeopleForm(request.POST)
			if form.is_valid():
				qname = form.cleaned_data['name']	
				qpagination = form.cleaned_data['pagination']
				# qgroup = form.cleaned_data['group']
				# qclass = form.cleaned_data['personclass']
				# qorder = form.cleaned_data['personorder']

				# if qgroup.isdigit():
				# 	qgroup = int(qgroup)
				# 	if int(qgroup) == 2: individual_object = actor_object.filter(corporateentity=True)
				# 	if int(qgroup) == 1: individual_object = actor_object.filter(corporateentity=False)

				if len(qname) > 0:
				 	actor_object = actor_object.filter(
				 		Q(fk_descriptor_name__descriptor_original__icontains=qname) | Q(fk_descriptor_descriptor1__descriptor_original__icontains=qname) | Q(fk_descriptor_descriptor2__descriptor_original__icontains=qname) | Q(fk_descriptor_descriptor3__descriptor_original__icontains=qname)
				 		)

				# if qclass.isdigit():
				# 	if int(qclass) > 0:
				# 		qclass = int(qclass)
				# 		actor_object = actor_object.filter(fk_group_class=qclass)

				# if qorder.isdigit():
				# 	if int(qorder) > 0:
				# 		qorder = int(qorder)
				# 		actor_object = actor_object.filter(fk_group_order=qorder)

				form = PeopleForm(request.POST)

		else:
			form = PeopleForm()
			qpagination = 1


	# preparing the data for individual_object
		# pagecountercurrent, pagecounternext, pagecounternextnext, totaldisplay, actor_object= pagination(qpagination, actor_object)

		pagecountercurrent, pagecounternext, pagecounternextnext, totaldisplay, totalrows, actor_object = paginator(qpagination, actor_object)


		# qpaginationend = int(qpagination) * 10
		# qpaginationstart = int(qpaginationend) -9 
		# totalrows = len(actor_object)

		# # if the dataset is less than the page limit
		# if qpaginationend > totalrows:
		# 	qpaginationend = totalrows

		# if totalrows > 1:
		# 	if qpaginationend < 10:
		# 		print(totalrows)
		# 	else:
		# 		actor_object = actor_object[qpaginationstart:qpaginationend]
		# totaldisplay = str(qpaginationstart) + " - " + str(qpaginationend)

		# pagecountercurrent = qpagination
		# pagecounternext = int(qpagination)+1
		# pagecounternextnext = int(qpagination)+2


	# this code prepares the list of links to associated seals for each individual
		sealindividual = []
		for e in actor_object:
			testvalue = e.id_individual
			testseal = Seal.objects.filter(
				fk_individual_realizer=testvalue)

			for f in testseal:
				current_id_seal = f.id_seal
				sealindividual.append((testvalue, current_id_seal))

		context = {
			'pagetitle': pagetitle,
			'actor_object': actor_object,
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

	############# Record Search ##############

	if searchtype == "records":

		pagetitle = 'title'
		part_object = Part.objects.filter(
		fk_event__locationreference__fk_locationname__fk_location__fk_region=87).order_by("fk_item__fk_repository", "fk_item__fk_series")

		if request.method == "POST":
			form = ItemForm(request.POST)
			if form.is_valid():
				qrepository = form.cleaned_data['repositories']	
				qseries = form.cleaned_data['series_all']
				qshelfmark = form.cleaned_data['shelfmark']
				qpagination = form.cleaned_data['pagination']

				if qrepository.isdigit():
					if int(qrepository) > 0:
						part_object = part_object.filter(
							fk_item__fk_repository=qrepository)

				if qseries.isdigit():
					if int(qseries) > 0:
						part_object = part_object.filter(
							fk_item__fk_series=qseries)

				if len(qshelfmark) > 0:
				 	part_object = part_object.filter(
				 		fk_item__shelfmark__icontains=qshelfmark)

		else:
			form = ItemForm()
			qpagination = 1

		pagecountercurrent, pagecounternext, pagecounternextnext, totaldisplay, totalrows, part_object = paginator(qpagination, part_object)

		context = {
			'pagetitle': pagetitle,
			'part_object': part_object,
			'totalrows': totalrows,
			'totaldisplay': totaldisplay,
			'form': form,
			'pagecountercurrent': pagecountercurrent,
			'pagecounternext': pagecounternext,
			'pagecounternextnext': pagecounternextnext,
			}

		template = loader.get_template('londonnet/search_part.html')
		return HttpResponse(template.render(context, request))


	############# Event Search ##############

	if searchtype == "events":

		pagetitle = 'title'

		context = {
			'pagetitle': pagetitle,
			# 'actor_object': actor_object,
			# 'sealindividual': sealindividual,
			# 'totalrows': totalrows,
			# 'totaldisplay': totaldisplay,
			# 'form': form,
			'pagecountercurrent': pagecountercurrent,
			'pagecounternext': pagecounternext,
			'pagecounternextnext': pagecounternextnext,
			}

		template = loader.get_template('londonnet/search_event.html')
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

	# References for each individual
	reference_object = Referenceindividual.objects.filter(fk_individual = digisig_entity_number).order_by(
		'fk_event__startdate')

	reference_set = referencecollector(reference_object)
	print ("referenceset", len(reference_set))

	template = loader.get_template('londonnet/actor.html')
	context = {
		'pagetitle': pagetitle,
		'actor_object': individual_object,
		'seal_object': seal_object,
		'sealnumber': sealnumber,
		'reference_object': reference_object,
		'reference_set': reference_set,
		'relationship_object': relationship_object,
		'relationshipnumber' : relationshipnumber,
		'sealdescriptionset': sealdescriptionset,
		}

	return HttpResponse(template.render(context, request))


############## Item ####################

def item_page(request, digisig_entity_number):
	item_object = get_object_or_404(Item, id_item=digisig_entity_number)

	pagetitle= item_object.shelfmark


	template = loader.get_template('londonnet/item.html')
	context = {
		'pagetitle': pagetitle,
		'item_object': item_object,
		# 'seal_object': seal_object,
		# 'sealnumber': sealnumber,
		# 'reference_object': reference_object,
		# 'reference_set': reference_set,
		# 'relationship_object': relationship_object,
		# 'relationshipnumber' : relationshipnumber,
		# 'sealdescriptionset': sealdescriptionset,
		}

	return HttpResponse(template.render(context, request))

############## Part (record) ####################

def part_page(request, digisig_entity_number):
	part_object = get_object_or_404(Part, id_part=digisig_entity_number)

	reference_set = Referenceindividual.objects.filter(fk_event=part_object.fk_event).exclude(fk_individual=10000019)
	manifestation_set = Manifestation.objects.filter(fk_support__fk_part=part_object)

	pagetitle= part_object.reference_full
	template = loader.get_template('londonnet/part.html')

	context = {
		'pagetitle': pagetitle,
		'part_object': part_object,
		'reference_set': reference_set,
		'manifestation_set': manifestation_set,
		# 'seal_object': seal_object,
		# 'sealnumber': sealnumber,
		# 'reference_object': reference_object,
		# 'reference_set': reference_set,
		# 'relationship_object': relationship_object,
		# 'relationshipnumber' : relationshipnumber,
		# 'sealdescriptionset': sealdescriptionset,
		}

	return HttpResponse(template.render(context, request))


############## Event ####################

def event_page(request, digisig_entity_number):
	#event_object = get_object_or_404(Event, pk_event=digisig_entity_number)

	pagetitle= "Page Title"


	template = loader.get_template('londonnet/event.html')
	context = {
		'pagetitle': pagetitle,
		# 'actor_object': individual_object,
		# 'seal_object': seal_object,
		# 'sealnumber': sealnumber,
		# 'reference_object': reference_object,
		# 'reference_set': reference_set,
		# 'relationship_object': relationship_object,
		# 'relationshipnumber' : relationshipnumber,
		# 'sealdescriptionset': sealdescriptionset,
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


def edit_item(request, digisig_entity_number):
	#some temp default data
	pagetitle = 'title'
	context = {
		'pagetitle': pagetitle,
	}
	template = loader.get_template('londonnet/index.html')


def edit_event(request, digisig_entity_number):
	#some temp default data
	pagetitle = 'title'
	context = {
		'pagetitle': pagetitle,
	}
	template = loader.get_template('londonnet/index.html')


############################# data ##############################

def data(request, digisig_entity_number):
	filename = "digisig_" + str(digisig_entity_number) + ".txt"
	content = rdf_generate(digisig_entity_number)
	response = HttpResponse(content, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
	return response
