from django.urls import path, re_path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('robots.txt', TemplateView.as_view(template_name="londonnet/robots.txt", content_type="text/plain")),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('success', views.success, name='success'),
    path('search/<str:searchtype>', views.search, name='search'),
    path('analyze/<str:analysistype>', views.analyze, name='analyze'),
    path('information/<str:infotype>', views.information, name='information'),
    path('discover/<str:discovertype>', views.discover, name='discover'),
    # re_path(r'discover/exhibit/(?P<digisig_entity_number>[0-9]{8})', views.rti_exhibit, name='rti_exhibit'),

    re_path(r'ajax/(?P<digisig_entity_number>[0-9]{8})', views.ajax, name='ajax'),

    re_path(r'edit/actor/(?P<digisig_entity_number>[0-9]{8})', views.edit_actor, name='edit_actor'),
    # re_path(r'edit/pas/(?P<digisig_entity_number>[0-9]{8})', views.edit_pas, name='edit_pas'),
    # re_path(r'edit/birch/(?P<digisig_entity_number>[0-9]{8})', views.edit_birch, name='edit_birch'),    
    # re_path(r'edit/manifestation/(?P<digisig_entity_number>[0-9]{8})', views.edit_manifestation, name='edit_manifestation'),
    re_path(r'edit/item/(?P<digisig_entity_number>[0-9]{8})', views.edit_item, name='edit_item'),
    # re_path(r'edit/support/(?P<digisig_entity_number>[0-9]{8})', views.edit_support, name='edit_support'),
    # re_path(r'edit/part/(?P<digisig_entity_number>[0-9]{8})', views.edit_part, name='edit_part'),

    # re_path(r'edit/description/(?P<digisig_entity_number>[0-9]{8})', views.edit_description, name='edit_description'),

    re_path(r'page/item/(?P<digisig_entity_number>[0-9]{8})', views.item_page, name='item_page'),
    re_path(r'data/item/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    re_path(r'page/record/(?P<digisig_entity_number>[0-9]{8})', views.part_page, name='part_page'),
    re_path(r'data/record/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    # re_path(r'page/seal/(?P<digisig_entity_number>[0-9]{8})', views.seal_page, name='seal_page'),
    # re_path(r'data/seal/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    # re_path(r'page/manifestation/(?P<digisig_entity_number>[0-9]{8})', views.manifestation_page, name='manifestation_page'),
    # re_path(r'data/manifestation/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    # re_path(r'page/sealdescription/(?P<digisig_entity_number>[0-9]{8})', views.sealdescription_page, name='sealdescription_page'),
    # re_path(r'data/sealdescription/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    # re_path(r'page/representation/(?P<digisig_entity_number>[0-9]{8})', views.representation_page, name='representation_page'),
    # re_path(r'data/representation/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    re_path(r'page/actor/(?P<digisig_entity_number>[0-9]{8})', views.actor_page, name='actor_page'),
    re_path(r'data/actor/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    # re_path(r'page/place/(?P<digisig_entity_number>[0-9]{8})', views.place_page, name='place_page'),
    # re_path(r'data/place/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    # re_path(r'page/term/(?P<digisig_entity_number>[0-9]{8})', views.term_page, name='term_page'),
    # re_path(r'data/term/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    # re_path(r'page/collection/(?P<digisig_entity_number>[0-9]{8})', views.collection_page, name='collection_page'),
    # re_path(r'data/collection/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    # re_path(r'page/machinelearning/(?P<digisig_entity_number>[0-9]{8})', views.machinelearning_page, name='machinelearning_page'),
    # re_path(r'data/machinelearning/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    re_path(r'entity/(?P<digisig_entity_number>[0-9]{8})', views.entity, name='entity'),
    re_path(r'edit/(?P<digisig_entity_number>[0-9]{8})', views.edit, name='edit'),  
    re_path(r'data/(?P<digisig_entity_number>[0-9]{8})', views.data, name='data'),

    path('entity/<str:entity_phrase>', views.entity_fail, name='entity_fail'),
    ]


