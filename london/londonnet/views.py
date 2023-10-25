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

	# individual_set = Individual.objects.filter(
	# 	fk_individual_event__Event__Location_reference__Locationname__Location__fk_region=87).count()	

	actor_total = Individual.objects.filter(
		fk_individual_event__fk_event__locationreference__fk_locationname__fk_location__fk_region=87).distinct('id_individual').count()	

	reference_total = Referenceindividual.objects.filter(fk_event__locationreference__fk_locationname__fk_location__fk_region=87).exclude(fk_individual=10000019).count()

	event_total = Referenceindividual.objects.filter(fk_event__locationreference__fk_locationname__fk_location__fk_region=87).exclude(fk_individual=10000019).distinct('fk_event').count()

	context = {
		'pagetitle': pagetitle,
		'actor_total': actor_total,
		'reference_total': reference_total,
		'event_total': event_total,
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

		pagetitle = 'Civic Government'

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

		print("Length", len(officialreferenceset))
				
		nodeofficeholderset = RelationshipNode.objects.filter(relationshipbranch__fk_individual=individual)
		branchofficeholderset = RelationshipBranch.objects.filter(fk_relationshipnode__in=nodeofficeholderset).exclude(fk_individual=individual).order_by('fk_individual__fullname_modern')
		print (len(nodeofficeholderset), len(branchofficeholderset))

		report = []

		for i in branchofficeholderset:
		 	officereferences = Referenceindividual.objects.filter(fk_individual=i.fk_individual, fk_individual2=individual.id_individual).order_by('fk_event__startdate')

	 		dateactive = dateactive(officereferences)



		 		# print (i.fk_individual.fullname_original, o.fk_event.startdate)
			 	report.append(str(i.fk_individual.fullname_original) + " " + str(o.fk_event.startdate) + " " + str(o.fk_event.enddate))

		### This code prepares collection info box and the data for charts on the collection page

		#defaults
		# qcollection = int(digisig_entity_number)
		data = []
		labels = []
		# pagetitle = 'All Collections'
		# collectioninfo= []
		# collection = get_object_or_404(Collection, id_collection=qcollection)
		# collectioncontributors = Collectioncontributor.objects.filter(fk_collection=qcollection)

		# contributorset = contributorgenerate(collectioncontributors)

		#if collection is set then limit the scope of the dataset
		# if (qcollection == 30000287):
		# 	sealdescriptionset = Sealdescription.objects.filter(fk_seal__gt=1)
		# 	sealset = Seal.objects.all()
		# 	faceset = Face.objects.filter(fk_faceterm=1)

		# 	#total count to enable calculation of portion of entries with place info
		# 	# placecount = Manifestation.objects.filter(
		# 	# 	fk_support__fk_part__fk_event__locationreference__fk_locationstatus__isnull=False).values().distinct().count()

		# 	#total number cases that have NOT been assigned to a location (yet) --- 7042 = not assigned --- location status =2 is a secondary location
		# 	casecount = Locationname.objects.exclude(
		# 		pk_locationname=7042).exclude(
		# 		locationreference__fk_locationstatus=2).filter(
		# 		locationreference__fk_event__part__fk_part__fk_support__gt=1).count()

		# 	#total portion of entries with place info
		# 	placecount = Locationname.objects.exclude(
		# 		locationreference__fk_locationstatus=2).filter(
		# 		locationreference__fk_event__part__fk_part__fk_support__gt=1).count()

		# 	#data for map counties
		# 	# placeset = Region.objects.filter(fk_locationtype=4).annotate(numplaces=Count('location__locationname__locationreference', 
		# 	# 	filter=Q(location__locationname__locationreference__fk_locationstatus=1)))
		# 	placeset = Region.objects.filter(fk_locationtype=4, 
		# 		location__locationname__locationreference__fk_locationstatus=1
		# 		).annotate(numplaces=Count('location__locationname__locationreference__fk_event__part__fk_part__fk_support')) 

		# 	#data for map regions -- not active?
		# 	# regiondisplayset = Regiondisplay.objects.annotate(numregions=Count('region__location__locationname__locationreference', 
		# 	# 	filter=Q(region__location__locationname__locationreference__fk_locationstatus=1)))
		# 	regiondisplayset = Regiondisplay.objects.filter(region__location__locationname__locationreference__fk_locationstatus=1
		# 		).annotate(numregions=Count('region__location__locationname__locationreference__fk_event__part__fk_part__fk_support')) 

		# else:
		# 	sealdescriptionset = Sealdescription.objects.filter(fk_collection=qcollection)
		# 	sealset = Seal.objects.filter(sealdescription__fk_collection=qcollection)
		# 	faceset = Face.objects.filter(fk_seal__sealdescription__fk_collection=qcollection).filter(fk_faceterm=1)
		# 	pagetitle = collection.collection_title

		# 	#total count to enable calculation of portion of entries with place info
		# 	# placecount = Manifestation.objects.filter(
		# 	# 	fk_face__fk_seal__sealdescription__fk_collection=qcollection).filter(
		# 	# 	fk_support__fk_part__fk_event__locationreference__fk_locationstatus__isnull=False).values().distinct().count()

		# 	#total number cases that have NOT been assigned to a location (yet) --- 7042 = not assigned
		# 	casecount = Locationname.objects.exclude(
		# 		pk_locationname=7042).exclude(
		# 		locationreference__fk_locationstatus__isnull=True).filter(
		# 		locationreference__fk_event__part__fk_part__fk_support__fk_face__fk_seal__sealdescription__fk_collection=qcollection).count()

		# 	#total portion of entries with place info
		# 	placecount = Locationname.objects.exclude(
		# 		locationreference__fk_locationstatus__isnull=True).filter(
		# 		locationreference__fk_event__part__fk_part__fk_support__fk_face__fk_seal__sealdescription__fk_collection=qcollection).count()

		# 	#data for map counties
		# 	#original
		# 	# placeset = Region.objects.filter(fk_locationtype=4).annotate(numplaces=Count('location__locationname__locationreference', 
		# 	# 	filter=Q(location__locationname__locationreference__fk_locationstatus=1) & 
		# 	# 	Q(location__locationname__locationreference__fk_event__part__support__manifestation__fk_face__fk_seal__sealdescription__fk_collection=qcollection)))
		# 	#revised
		# 	placeset = Region.objects.filter(fk_locationtype=4, 
		# 		location__locationname__locationreference__fk_locationstatus=1, 
		# 		location__locationname__locationreference__fk_event__part__fk_part__fk_support__fk_face__fk_seal__sealdescription__fk_collection=qcollection
		# 		).annotate(numplaces=Count('location__locationname__locationreference'))

		# 	# #data for region map 
		# 	# regiondisplayset = Regiondisplay.objects.annotate(numregions=Count('region__location__locationname__locationreference', 
		# 	# 	filter=Q(region__location__locationname__locationreference__fk_locationstatus=1) & 
		# 	# 	Q(region__location__locationname__locationreference__fk_event__part__support__manifestation__fk_face__fk_seal__sealdescription__fk_collection=qcollection)))

		# 	#data for region map 
		# 	regiondisplayset = Regiondisplay.objects.filter( 
		# 		region__location__locationname__locationreference__fk_locationstatus=1, 
		# 		region__location__locationname__locationreference__fk_event__part__fk_part__fk_support__fk_face__fk_seal__sealdescription__fk_collection=qcollection
		# 		).annotate(numregions=Count('region__location__locationname__locationreference'))

		# sealcount = sealset.count()
		# facecount = faceset.count()
		# classcount = faceset.filter(fk_class__isnull=False).exclude(fk_class=10000367).exclude(fk_class=10001007).count()

		# placecounttotal = 0
		# for i in placeset:
		# 	placecounttotal = placecounttotal + i.numplaces

		# collectioninfo = collectiondata(qcollection, sealcount)

		### generate the collection info data for chart 1 'Percentage of complete entries',
		# sealdescriptioncount = sealdescriptionset.count()
		# sealdescriptiontitle = sealdescriptionset.filter(sealdescription_title__isnull=False).count()
		# sealdescriptionmotif = sealdescriptionset.filter(motif_obverse__isnull=False).count()
		# sealdescriptionidentifier = sealdescriptionset.filter(sealdescription_identifier__isnull=False).count()

		# actorscount = sealset.filter(fk_individual_realizer__gt=10000019).count()
		# datecount =sealset.filter(date_origin__gt=1).count()

		# title = calpercent(sealdescriptioncount, sealdescriptiontitle)
		# motif = calpercent(sealdescriptioncount, sealdescriptionmotif)
		# identifier = calpercent(sealdescriptioncount, sealdescriptionidentifier)
		# actors = calpercent(sealcount, actorscount)
		# date = calpercent(sealcount, datecount)
		# fclass = calpercent(facecount, classcount)
		# #place = calpercent(placecount, placecounttotal)
		# place = calpercent(placecount, casecount)


		# #9/9/2022 -- decided to limit the info to actor, date, class, place
		# # data1 = [title, motif, identifier, actors, date, fclass, place]
		# # labels1 = ["title", "description", "identifier", "actor", "date", "class", "place"]

		# data1 = [actors, date, fclass, place]
		# labels1 = ["actor", "date", "class", "place"]



		# ### generate the collection info data for chart 2 -- 'Percentage of seals per class',

		# if (qcollection == 30000287):
		# 	classset = Classification.objects.order_by('-level').annotate(numcases=Count('face')).exclude(id_class=10001007).exclude(id_class=10000367)
		# else:
		# 	classset = Classification.objects.order_by('-level').filter(face__fk_seal__sealdescription__fk_collection=qcollection).annotate(numcases=Count('face')).exclude(id_class=10001007).exclude(id_class=10000367)

		# data2, labels2 = classdistribution(classset, facecount)



		# ### generate the collection info data for chart 3  -- 'Percentage of seals by period',

		# data3, labels3 = datedistribution(sealset)



		# ### generate the collection info data for chart 4 -- seals per region,

		# ## data for colorpeth map
		# maplayer1 = get_object_or_404(Jsonstorage, id_jsonfile=1)
		# maplayer = json.loads(maplayer1.jsonfiletxt)

		# for i in maplayer:
		# 	if i == "features":
		# 		for b in maplayer[i]:
		# 			j = b["properties"]
		# 			countyvalue = j["HCS_NUMBER"]
		# 			countyname = j["NAME"]

		# 			numberofcases = placeset.filter(fk_his_countylist=countyvalue)

		# 			for i in numberofcases:
		# 				j["cases"] = i.numplaces


		# ## data for region map
		# # make circles data -- defaults -- note that this code is very similar to the function mapdata2
		# region_dict = mapgenerator3(regiondisplayset)

		# ### generate the collection info data for chart 5 --  'Percentage of actors per class',

		# #for print group totals (legacy)
		# if (qcollection == 30000287):
		# 	printgroupset = Printgroup.objects.annotate(numcases=Count('fk_printgroup', filter=Q(fk_printgroup__sealdescription__fk_collection__gte=0))).order_by('printgroup_order')

		# else: printgroupset = Printgroup.objects.annotate(numcases=Count('fk_printgroup', filter=Q(fk_printgroup__sealdescription__fk_collection=qcollection))).order_by('printgroup_order')

		# #for modern group system
		# if (qcollection == 30000287):
		# 	groupset = Groupclass.objects.annotate(numcases=Count('id_groupclass', filter=Q(fk_group_class__fk_group__fk_actor_group__sealdescription__fk_collection__gte=0))).order_by('id_groupclass')

		# else:
		# 	groupset = Groupclass.objects.annotate(numcases=Count('id_groupclass', filter=Q(fk_group_class__fk_group__fk_actor_group__sealdescription__fk_collection=qcollection))).order_by('id_groupclass')

		# data5 = []
		# labels5 = []
		# for g in groupset:
		# 	if (g.numcases > 0):
		# 		percentagedata = (g.numcases/sealcount)*100 
		# 		# if percentagedata > 1:
		# 		data5.append(percentagedata)
		# 		labels5.append(g.groupclass)

		form = GovernmentForm()		
		context = {
			'pagetitle': pagetitle,
			'group_name': group_name,
			'nodeofficeholderset': nodeofficeholderset, 
			'branchofficeholderset': branchofficeholderset,
			'report': report,
			
			# 'collectioninfo': collectioninfo,
			# 'collection': collection,
			# 'contributorset': contributorset,
		# 	'labels1': labels1,
		# 	'data1': data1,
		# 	'labels2': labels2,
		# 	'data2': data2,
		# 	'labels3': labels3,
		# 	'data3': data3,
		# 	# 'labels4': labels4,
		# 	# 'data4': data4,
		# 	'region_dict': region_dict,
		# 	'maplayer': maplayer,
		# 	'labels5': labels5,
		# 	'data5': data5,
		# 	'form': form,
		}
			
		template = loader.get_template('londonnet/info_government.html')					
		return HttpResponse(template.render(context, request))



########################### Discover ############################

def discover(request, discovertype):

	print (infotype)


#################### Search #########################
def search(request, searchtype):

	print(searchtype)

### Actor Search

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
		qpaginationend = int(qpagination) * 10
		qpaginationstart = int(qpaginationend) -9 
		totalrows = len(actor_object)

		# if the dataset is less than the page limit
		if qpaginationend > totalrows:
			qpaginationend = totalrows

		if totalrows > 1:
			if qpaginationend < 10:
				print(totalrows)
			else:
				actor_object = actor_object[qpaginationstart:qpaginationend]
		totaldisplay = str(qpaginationstart) + " - " + str(qpaginationend)

		pagecountercurrent = qpagination
		pagecounternext = int(qpagination)+1
		pagecounternextnext = int(qpagination)+2

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
