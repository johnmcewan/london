from django import forms
from django.db.models import Count
from django.db.models import Q

from .models import * 

# #Form for querying seal impressions
# repositories_options = [('','None')]
# series_options = [('', 'None')]
# location_options = []
# nature_options = []
# representation_options = [('', 'None')]
timegroup_options = [('', 'None')]
shape_options = [('', 'None')]
classname_options = [('', 'None')]

# for e in Digisigrepositoriesview.objects.order_by('repository_fulltitle'):
# 	repositories_options.append((e.fk_repository, e.repository_fulltitle))

# for e in DigisigManifestationview.objects.order_by('series_name').distinct('series_name'):
# 	appendvalue = e.repository + " : " + e.series_name
# 	series_options.append((e.fk_series, appendvalue))

# for e in DigisigManifestationview.objects.order_by('region_label').distinct('region_label'):
# 	location_options.append((e.fk_region, e.region_label))

# for e in DigisigManifestationview.objects.order_by('nature_name').distinct('nature_name'):
# 	nature_options.append((e.fk_nature, e.nature_name))

# for e in RepresentationType.objects.order_by('representation_type').distinct('representation_type').exclude(pk_representation_type=5):
# 	representation_options.append((e.pk_representation_type, e.representation_type))
	
for e in TimegroupC.objects.order_by('pk_timegroup_c'):
	timegroup_options.append((e.timegroup_c, e.timegroup_c_range))

for e in DigisigManifestationview.objects.order_by('shape').distinct('shape'):
	shape_options.append((e.fk_shape, e.shape))

for e in DigisigManifestationview.objects.order_by('class_name').distinct('class_name'):
	classname_options.append((e.fk_class, e.class_name))

# class ManifestationForm(forms.Form):
# 	repository = forms.ChoiceField(choices=repositories_options, required=False)
# 	series = forms.ChoiceField(choices=series_options, required=False, initial={'': 'None'})	
# 	location = forms.ChoiceField(choices=location_options, required=False)
# 	nature = forms.ChoiceField(label='Object', choices=nature_options, required=False)
# 	representation = forms.ChoiceField(choices=representation_options, required=False, initial={'': 'None'})
# 	timegroup = forms.ChoiceField(label='Period', choices=timegroup_options, required=False)
# 	shape = forms.ChoiceField(choices=shape_options, required=False, initial={'': 'None'})
# 	name = forms.CharField(label='Identifier', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Example: BA 867 box 21'}))
# 	classname = forms.ChoiceField(label='Digisig Class', choices=classname_options, required=False)
# 	pagination = forms.IntegerField(initial=1, widget=forms.HiddenInput)


# #Form for quering seal descriptions

collections_options = [('30000287', 'All Collections')]

for e in Collection.objects.order_by('collection_shorttitle').annotate(numdescriptions=Count('sealdescription')):
	if (e.numdescriptions > 0):
		collections_options.append((e.id_collection, e.collection_shorttitle))

# class SealdescriptionForm(forms.Form):
# 	pagination = forms.IntegerField(initial=1, widget=forms.HiddenInput)
# 	collection = forms.ChoiceField(choices=collections_options, required=False)
# 	cataloguecode = forms.CharField(label='Entry', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Example: P281'}))
# 	#cataloguedescription = forms.CharField(label='Description', max_length=100, required=False)
# 	cataloguemotif = forms.CharField(label='Motif Description', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Example: lily'}))
# 	cataloguename = forms.CharField(label='Person/Entity', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Example: John son of Robert'}))


#Form for contact details

class ContactForm(forms.Form):
    from_email = forms.EmailField(label="Email", required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


# #Form for advanced analysis

# dataset_options = []
# region_options = [('0', 'All')]

# for e in Region.objects.filter(fk_locationtype=12).order_by('pk_region'):
# 	region_options.append((e.pk_region, e.region_label))

# for e in Dataset.objects.order_by('id_dataset'):
# 	dataset_options.append((e.id_dataset, e.dataset))

# class AdvancedForm(forms.Form):	
# 	# region = forms.ChoiceField(choices=region_options, required=False)
# 	collection = forms.ChoiceField(choices=collections_options, required=False)
# 	classname = forms.ChoiceField(label='Digisig Class', choices=classname_options, required=False)

#Form for london analysis

sigillantgroup_options = [('0', 'All')]

for e in Printgroup.objects.order_by('printgroup_order'):
	sigillantgroup_options.append((e.pk_printgroup, e.printgroup_london))

class LondonForm(forms.Form):
	shape = forms.ChoiceField(choices=shape_options, required=False, initial={'': 'None'})
	classname = forms.ChoiceField(choices=classname_options, required=False)
	sigillantgroup = forms.ChoiceField(choices=sigillantgroup_options, required=False)

#Form for ML date prediction analysis

# classification_options = []
# collection2_options = []

# ## this is a very bad way of selecting the classifications in use -- 2023_9_23
# for e in Classification.objects.exclude(class_name__startswith="z").exclude(class_name__startswith="Z").order_by('class_sortorder'):
# 	classification_options.append((e.id_class, e.class_name))

# for e in Collection.objects.filter(id_collection=30000047).order_by('id_collection'):
# 	collection2_options.append((e.id_collection, e.collection_title))
# 	#### forcing addition of Linenthal --- 2023_9_26
# 	collection2_options.append((30000337, 'Linenthal, Schoyen Collection'))

# class MLpredictionForm(forms.Form):
# 	classification = forms.ChoiceField(choices=classification_options, required=False)
# 	collection2 = forms.ChoiceField(choices=collection2_options, required=False)


#Form for collections, map and time analysis

graphchoices = [('1', 'Seal Descriptions'), ('2', 'Seal Impressions, Matrices and Casts')]
mapchoices = [('1', 'Places'), ('2', 'Counties'), ('3', 'Regions')]
sealtype_options = [('', 'None')]
period_options = [('', 'None')]
timegroup_options2 = []

for e in Sealtype.objects.order_by('sealtype_name'):
	sealtype_options.append((e.id_sealtype, e.sealtype_name))

for e in TimegroupC.objects.order_by('pk_timegroup_c'):
	timegroup_options2.append((e.pk_timegroup_c, e.timegroup_c_range))

class CollectionForm(forms.Form):
	collection = forms.ChoiceField(choices=collections_options, required=False)
	#graphchoice = forms.ChoiceField(choices=graphchoices, required=False)
	mapchoice = forms.ChoiceField(choices=mapchoices, required=False)
	timechoice = forms.ChoiceField(choices=timegroup_options2, required=False)
	# classname = forms.ChoiceField(label='Digisig Class', choices=classname_options, required=False)
	sealtypechoice = forms.ChoiceField(choices=sealtype_options, required=False)

# #Form for seal type search

# sealtype_options = []

# for e in Sealtype.objects.order_by('sealtype_name'):
# 	sealtype_options.append((e.id_sealtype, e.sealtype_name))

# class TypeForm(forms.Form):
# 	type = forms.ChoiceField(choices=sealtype_options, required=True, initial={'1': 'Hare on Hound'})


#Form for Actor search

Choices = [('0', 'None'), ('1', 'Individual'), ('2', 'Corporate')]

personclass_options = []
personorder_options = []

for e in Digisigindividualview.objects.order_by('groupclass').distinct('groupclass'):
	personclass_options.append((e.fk_group_class, e.groupclass))

for e in Digisigindividualview.objects.order_by('grouporder').distinct('grouporder'):
	personorder_options.append((e.fk_group_order, e.grouporder))

class PeopleForm(forms.Form):
	name = forms.CharField(label='id_name', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Example: John'}))
	group = forms.ChoiceField(choices=Choices, required=False)
	pagination = forms.IntegerField(initial=1, widget=forms.HiddenInput)
	personclass = forms.ChoiceField(choices=personclass_options, required=False)
	personorder = forms.ChoiceField(choices=personorder_options, required=False) 

# # Form for Date search

# class DateForm(forms.Form):
# 	classname = forms.ChoiceField(label='Digisig Class', choices=classname_options, required=True)
# 	shape = forms.ChoiceField(choices=shape_options, required=True, initial={'': 'None'})
# 	face_vertical = forms.IntegerField(label='vertical',required=True)
# 	face_horizontal = forms.IntegerField(label='horizontal',required=True)	

# # Form for place search
# county_options = [('0', 'None')]
# regionoptions = [('0', 'None')]

# for e in Region.objects.filter(location__isnull=False).filter(fk_locationtype=4).order_by('region_label').distinct('region_label'):
# 	county_options.append((e.pk_region, e.region_label))

# for e in Regiondisplay.objects.filter(region__location__isnull=False).order_by('regiondisplay_label').distinct('regiondisplay_label'):
# 	regionoptions.append((e.id_regiondisplay, e.regiondisplay_label))

# class PlaceForm(forms.Form):
# 	county = forms.ChoiceField(choices=county_options, required=False)
# 	region = forms.ChoiceField(choices=regionoptions, required=False)
# 	location_name = forms.CharField(label='location_name', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Example: Bruges'}))	
# 	pagination = forms.IntegerField(initial=1, widget=forms.HiddenInput)


class PageCycleForm(forms.Form):
	pagination = forms.IntegerField(initial=1, widget=forms.HiddenInput)

# Form for item search

# #Nb: a search seal form uses a limited number of series and repositories -- but need all for this form
# series_all_options = [('', 'None')]
# repositories_all_options = [('', 'None')]

# for e in Series.objects.order_by('fk_repository'):
# 	repository = e.fk_repository
# 	appendvalue = repository.repository + " : " + e.series_name
# 	series_all_options.append((e.pk_series, appendvalue))

# for e in Repository.objects.order_by('repository_fulltitle'):
# 	repositories_options.append((e.fk_repository, e.repository_fulltitle))

# class ItemForm(forms.Form):
# 	series_all = forms.ChoiceField(label='series', choices=series_all_options, required=False, initial={'': 'None'})
# 	repositories = forms.ChoiceField(label='repositories', choices=repositories_options, required=False, initial={'': 'None'})
# 	shelfmark = forms.CharField(label='shelfmark', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Example: 867'}))
# 	pagination = forms.IntegerField(initial=1, widget=forms.HiddenInput)

# ######################## Edit forms ########################

#Form for editing sealdescriptionpeople
descriptor_options = [('', 'None')]
prefix_options = [('', 'None')]
role_options = [('', 'None')]

for e in Descriptor.objects.order_by('descriptor_original'):
	descriptorphrase = str(e.descriptor_original) + "/" + str(e.descriptor_modern)
	#descriptor_options.append((e.pk_descriptor, e.descriptor_original))
	descriptor_options.append((e.pk_descriptor, descriptorphrase))

for e in Prefix.objects.order_by('prefix'):
	prefix_options.append((e.pk_prefix, e.prefix))

for e in RelationshipRole.objects.order_by('relationship_role'):
	role_options.append((e.pk_role, e.relationship_role))


class Sealdescription_actorForm(forms.Form):
	sealdescriptiontitle = forms.CharField(label='id_name', max_length=200, required=False, widget=forms.TextInput())
	sealactor = forms.IntegerField(required=False)
	newactor = forms.BooleanField(required=False)
	newactortitle = forms.ChoiceField(choices=descriptor_options, required=False)
	newactorname = forms.ChoiceField(choices=descriptor_options, required=False)
	newactordescr1 = forms.ChoiceField(choices=descriptor_options, required=False)
	newactordescr2 = forms.ChoiceField(choices=descriptor_options, required=False)
	newactordescr3 = forms.ChoiceField(choices=descriptor_options, required=False)
	newactorpref1 = forms.ChoiceField(choices=prefix_options, required=False)
	newactorpref2 = forms.ChoiceField(choices=prefix_options, required=False)
	newactorpref3 = forms.ChoiceField(choices=prefix_options, required=False)

	addrelationship = forms.BooleanField(required=False)
	eventtarget = forms.IntegerField(required=False)
	roleactor1 = forms.ChoiceField(choices=role_options, required=False, initial=1729)
	roleactor2  = forms.ChoiceField(choices=role_options, required=False)



# #Form for editing PAS

# class Sealdescription_pasForm(forms.Form):
# 	sealdescriptiontitle = forms.CharField(label='title',max_length=200, required=False, widget=forms.TextInput())
# 	motif_obverse = forms.CharField(label='motif_obverse', max_length=400, required=False, widget=forms.TextInput())
# 	legend_obverse = forms.CharField(label='legend_obverse', max_length=300, required=False, widget=forms.TextInput())
# 	shape = forms.ChoiceField(label='shape',choices=shape_options, required=False, initial={'': 'None'})
# 	classname = forms.ChoiceField(label='class',choices=classname_options, required=False)
# 	face_vertical = forms.IntegerField(label='vertical',required=False)
# 	face_horizontal = forms.IntegerField(label='horizontal',required=False) 
# 	image_file_alt = forms.CharField(label='image_file_alt', max_length=200, required=False, widget=forms.TextInput())
# 	reverse = forms.BooleanField(required=False) 
# 	sealsize_horizontal_inch = forms.IntegerField(label='sealsize_horizontal_inch',required=False) 
# 	sealsize_vertical_inch = forms.IntegerField(label='sealsize_vertical_inch',required=False) 
# 	sealsize_inch_horiz_frac_p1 = forms.IntegerField(label='sealsize_inch_horiz_frac_p1',required=False)
# 	sealsize_inch_horiz_frac_p2 = forms.IntegerField(label='sealsize_inch_horiz_frac_p2',required=False)
# 	sealsize_inch_vert_frac_p1 = forms.IntegerField(label='sealsize_inch_vert_frac_p1',required=False)
# 	sealsize_inch_vert_frac_p2 = forms.IntegerField(label='sealsize_inch_vert_frac_p2',required=False)
# 	deleteentry = forms.BooleanField(required=False) 


# #Form for editing representations


# ## Note there is a DIFFERENT collections_options above, for use in the collections public page
# collection_options = [('', 'None')]
# contributor_options = [('', 'None')]
# representationtype_options = [('', 'None')]
# rightsholder_options = [('', 'None')]
# access_options = [('', 'None')] 


# for e in Contributor.objects.order_by('name_last'):
# 	contributorphrase = (str(e.name_last) + ", " +  str(e.name_first) + " " + str(e.name_middle))
# 	contributor_options.append((e.pk_contributor, contributorphrase))

# for e in RepresentationType.objects.order_by('representation_type'):
# 	representationtype_options.append((e.pk_representation_type, e.representation_type))

# for e in Rightsholder.objects.order_by('rightsholder'):
# 	rightsholder_options.append((e.pk_rightsholder, e.rightsholder))

# for e in Access.objects.order_by('access_level'):
# 	access_options.append((e.pk_access, e.access_level))

# for e in Collection.objects.order_by('collection_shorttitle'):
# 	collection_options.append((e.id_collection, e.collection_shorttitle))


# class Representationedit_Form(forms.Form):
# 	creator = forms.ChoiceField(label='creator',choices=contributor_options, required=False, initial={'': 'None'})
# 	contributor = forms.ChoiceField(label='contributor',choices=contributor_options, required=False, initial={'': 'None'})
# 	rightsholder = forms.ChoiceField(label='rightsholder',choices=rightsholder_options, required=False, initial={'': 'None'})
# 	representationtype = forms.ChoiceField(label='representationtype',choices=representationtype_options, required=False, initial={'': 'None'})
# 	access = forms.ChoiceField(label='access',choices=access_options, required=False, initial={'': 'None'})
# 	dateimage = forms.CharField(label='dateimage',max_length=200, required=False, widget=forms.TextInput())
# 	primacy = forms.BooleanField(label='primacy', required=False)
# 	image_file_location = forms.CharField(label='image_file_location', max_length=200, required=False, widget=forms.TextInput())
# 	collection = forms.ChoiceField(label='collection', choices=collection_options, required=False, initial={'': 'None'})


# #Form for editing manifestations
# attachment_options = [('', 'None')]
# position_options = [('', 'None')]
# supportstatus_options = [('', 'None')]
# material_options = [('', 'None')]

# for e in Attachment.objects.order_by('pk_attachment'):
# 	attachment_options.append((e.pk_attachment, e.attachment))

# for e in Position.objects.order_by('pk_position'):
# 	position_options.append((e.pk_position, e.position))

# for e in Supportstatus.objects.order_by('id_supportstatus'):
# 	supportstatus_options.append((e.id_supportstatus, e.supportstatus))

# for e in Material.objects.order_by('pk_material'):
# 	material_options.append((e.pk_material, e.material))

# class Manifestationedit_Form(forms.Form):
# 	#fields specific to manifestation
# 	attachment = forms.ChoiceField(label='attachment',choices=attachment_options, required=False, initial={'': 'None'})
# 	position = forms.ChoiceField(label='position',choices=position_options, required=False, initial={'': 'None'})
# 	support = forms.IntegerField(label='support',required=False)
# 	supportstatus = forms.ChoiceField(label='supportstatus',choices=supportstatus_options, required=False, initial={'': 'None'})
# 	shape = forms.ChoiceField(choices=shape_options, required=False, initial={'': 'None'})
# 	dimensionsvert = forms.IntegerField(label='dimensionsvert',required=False)
# 	dimensionshoriz = forms.IntegerField(label='dimensionshoriz',required=False)
# 	classname = forms.ChoiceField(label='Digisig Class', choices=classname_options, required=False)
# 	material = forms.ChoiceField(label='Material', choices=material_options, required=False)
# 	#fields specific to representation
# 	creator = forms.ChoiceField(label='creator',choices=contributor_options, required=False, initial={'': 'None'})
# 	contributor = forms.ChoiceField(label='contributor',choices=contributor_options, required=False, initial={'': 'None'})
# 	rightsholder = forms.ChoiceField(label='rightsholder',choices=rightsholder_options, required=False, initial={'': 'None'})
# 	representationtype = forms.ChoiceField(label='representationtype',choices=representationtype_options, required=False, initial={'': 'None'})
# 	access = forms.ChoiceField(label='access',choices=access_options, required=False, initial={'': 'None'})
# 	dateimage = forms.CharField(label='dateimage',max_length=200, required=False, widget=forms.TextInput())
# 	primacy = forms.BooleanField(label='primacy', required=False)
# 	image_file_location = forms.CharField(label='image_file_location', max_length=200, required=False, widget=forms.TextInput())
# 	collection = forms.ChoiceField(label='collection', choices=collection_options, required=False, initial={'': 'None'})

# #Form for editing supports

# number_options = [('', 'None')]

# for e in Number.objects.order_by('number'):
# 	number_options.append((e.pk_number, e.number))

# class Supportedit_Form(forms.Form):
# 	attachment = forms.ChoiceField(label='attachment',choices=attachment_options, required=False, initial={'': 'None'})
# 	supportstatus = forms.ChoiceField(label='supportstatus',choices=supportstatus_options, required=False, initial={'': 'None'})
# 	material = forms.ChoiceField(label='Material', choices=material_options, required=False)
# 	number_support = forms.ChoiceField(label='number_support', choices=number_options, required=False)


# #Form for editing items

# class Itemedit_Form(forms.Form):
# 	series_all = forms.ChoiceField(label='series', choices=series_all_options, required=False, initial={'': 'None'})
# 	repositories = forms.ChoiceField(label='repositories', choices=repositories_options, required=False, initial={'': 'None'})
# 	# prefix_alpha1 = forms.CharField(label='p_alpha1',max_length=40, required=False, widget=forms.TextInput())
#     # prefix_number1 = forms.IntegerField(label='p_number1',required=False)
#     # prefix_alpha2 = forms.CharField(label='p_alpha2',max_length=40, required=False, widget=forms.TextInput())
#     # prefix_number2 = forms.IntegerField(label='p_number2',required=False)
#     # prefix_alpha3 = forms.CharField(label='p_alpha3',max_length=40, required=False, widget=forms.TextInput())
#     # prefix_number3 = forms.IntegerField(label='p_number3',required=False)
# 	# classmark_alpha1 = forms.CharField(label='c_alpha1',max_length=40, required=False, widget=forms.TextInput())
#     # classmark_number1 = forms.IntegerField(label='c_number1',required=False)
#     # classmark_alpha2 = forms.CharField(label='c_alpha2',max_length=40, required=False, widget=forms.TextInput())
#     # classmark_number2 = forms.IntegerField(label='c_number2',required=False)
#     # classmark_alpha3 = forms.CharField(label='c_alpha3',max_length=40, required=False, widget=forms.TextInput())
#     # classmark_number3 = forms.IntegerField(label='c_number3',required=False)
	
# 	#fields specific to representation
# 	creator = forms.ChoiceField(label='creator',choices=contributor_options, required=False, initial={'': 'None'})
# 	contributor = forms.ChoiceField(label='contributor',choices=contributor_options, required=False, initial={'': 'None'})
# 	rightsholder = forms.ChoiceField(label='rightsholder',choices=rightsholder_options, required=False, initial={'': 'None'})
# 	representationtype = forms.ChoiceField(label='representationtype',choices=representationtype_options, required=False, initial={'': 'None'})
# 	access = forms.ChoiceField(label='access',choices=access_options, required=False, initial={'': 'None'})
# 	dateimage = forms.CharField(label='dateimage',max_length=200, required=False, widget=forms.TextInput())
# 	primacy = forms.BooleanField(label='primacy', required=False)
# 	image_file_location = forms.CharField(label='image_file_location', max_length=200, required=False, widget=forms.TextInput())
# 	collection = forms.ChoiceField(label='collection', choices=collection_options, required=False, initial={'': 'None'})

# #Form for editing parts

# class Partedit_Form(forms.Form):
# 	number_support = forms.ChoiceField(label='number_support', choices=number_options, required=False)
# 	addsupport = forms.BooleanField(label='addsupport', required=False)

# 	#fields specific to representation
# 	creator = forms.ChoiceField(label='creator',choices=contributor_options, required=False, initial={'': 'None'})
# 	contributor = forms.ChoiceField(label='contributor',choices=contributor_options, required=False, initial={'': 'None'})
# 	rightsholder = forms.ChoiceField(label='rightsholder',choices=rightsholder_options, required=False, initial={'': 'None'})
# 	representationtype = forms.ChoiceField(label='representationtype',choices=representationtype_options, required=False, initial={'': 'None'})
# 	access = forms.ChoiceField(label='access',choices=access_options, required=False, initial={'': 'None'})
# 	dateimage = forms.CharField(label='dateimage',max_length=200, required=False, widget=forms.TextInput())
# 	primacy = forms.BooleanField(label='primacy', required=False)
# 	image_file_location = forms.CharField(label='image_file_location', max_length=200, required=False, widget=forms.TextInput())
# 	collection = forms.ChoiceField(label='collection', choices=collection_options, required=False, initial={'': 'None'})


#Form for analysing government office holders

office_options = [('', 'None')]

# for e in Position.objects.order_by('pk_position'):
# 	position_options.append((e.pk_position, e.position))

class Government_Form)forms.Form):
	timegroupC = forms.ChoiceField(label='Period', choices=timegroup_options, required=False)
	office_type = forms.ChoiceField(label='office_options', choices=office_options, required=False)