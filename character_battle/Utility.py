from character_battle.models import *
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from django.core.exceptions import ObjectDoesNotExist

from character_battle.forms import *
from character_battle.Utility import *

from django.http import HttpResponse, HttpResponseNotFound, Http404

from mimetypes import guess_type

from django.core import serializers

class Util(object):

    def get_five_random_attributes(self):
        return Attribute.objects.all().order_by('?')[:5]

    def handle_attribute_request(self, char_id, attr_id):
        character = Character.objects.get(pk=char_id)
        attributes = character.attributes.all()
        new_attribute = Attribute.objects.get(pk=attr_id)
        if(new_attribute in attributes):
            character.attributes.remove(new_attribute)
        elif(len(attributes) == 3):
            character.attributes.remove(attributes.last())
            character.attributes.add(new_attribute)
        elif(len(attributes) <  3):
            character.attributes.add(new_attribute)
        print attributes
        character.save()

    def get_attributes(self, char_id):
        attributes = []
        try:
            character = Character.objects.get(pk=char_id)
            attributes = character.attributes.all().order_by('-rating')
        except:
            pass
        return attributes

    def get_character_and_attributes(self, user):
        character = Character.objects.filter(owner=user)[0]
        attributes = character.attributes.all().order_by('-rating')
        return (character, attributes)

    def get_all_user_chars(self, user):
        return Character.objects.filter(owner=user)

    def validate_pick(self, request):
        if(not('attr_id' in request.POST and request.POST['attr_id'])):
            return False
        attr_id = request.POST['attr_id']
        attr = False
        try:
            attr = Attribute.objects.get(pk=int(attr_id))
        except:
            pass
        return attr

    def validate_save_attr(self, request):
        if(not('first' in request.POST and request.POST['first'])):
            return False
        if(not('second' in request.POST and request.POST['second'])):
            return False
        if(not('third' in request.POST and request.POST['third'])):
            return False
        if(not('char_id' in request.POST and request.POST['char_id'])):
            return False
        try:
            first = Attribute.objects.get(pk=request.POST['first'])
            second = Attribute.objects.get(pk=request.POST['second'])
            third = Attribute.objects.get(pk=request.POST['third'])
            char = Character.objects.get(pk=request.POST['char_id'])
            if(int(char.owner.pk) != int(request.user.pk)):
                return False
            if(char.picked_attr):
                return False
        except:
            return False
        char.attributes.add(first)
        char.attributes.add(second)
        char.attributes.add(third)
        char.picked_attr = True
        char.save()
        return True

############Challenge Methods##################################################
    #Gets all the onging battles the user is in
    def get_curr_battles(self, user):
        return Challenge.objects.filter((Q(user_challenger=user) | Q(user_challenging=user)) & Q(accept=True) & Q(finished=False))
        

    #Gets all the challenges the current user was challenged to
    def get_challengers(self, user):
        return Challenge.objects.filter(user_challenging=user, accept=False)

    #Gets all the challenges the current user initated
    def get_challenging(self, user):
        return Challenge.objects.filter(user_challenger=user, accept=False)

    #Checks whether request.user is valid and a Get request method
    def validate_char_display(self, request):
        print request
        if(request.method == 'POST'):
            raise Http404
        if not ('username' in request.GET and request.GET['username']):
            raise Http404
        user = get_object_or_404(User, username=request.GET['username'])
        if (not user) or (user == request.user):
            raise Http404
        return user

    #Checks whether id is a valid pk for Challenge object
    def validate_accept(self, id):
        challenge = get_object_or_404(Challenge, pk=int(id))
        if not challenge:
            raise Http404
        return challenge

    #Checks whether id is a valid pk for Challenge object
    def validate_decline(self, id):
        challenge = get_object_or_404(Challenge, pk=int(id))
        if not challenge:
            raise Http404
        return challenge

    #Checks whether a POST requets was made and valid pks were given
    def validate_challenge(self, request):
        if(request.method == 'GET'):
            raise Http404
        if not ('challenger' in request.POST and request.POST['challenger']):
            raise Http404
        if not ('challenging' in request.POST and request.POST['challenging']):
            raise Http404
        challenger = get_object_or_404(Character, pk=int(request.POST['challenger']))
        challenging = get_object_or_404(Character, pk=int(request.POST['challenging']))
        if not (challenger and challenging):
            raise Http404
        return (challenger, challenging)