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


util = Util()

@transaction.atomic
def register(request):
  context = {}

  # User requested registration page
  if request.method == 'GET':

    # Build register form
  	context['form'] = RegisterForm()

    # Render register template with form
  	return render(request, "register.html", context)

  # User submitting registration
  form = RegisterForm(request.POST)
  context['form'] = form

  # Django Forms validation
  if not form.is_valid():
    return render(request, "register.html", context)

  # Create a new user from cleaned data from form
  new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                      password=form.cleaned_data['password1'])

  # Save new user to database
  new_user.save()

  # Authenticate the new user
  new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

  # Login the new user
  login(request, new_user)

  # Redirect the user to create the character
  return create_character(request)

@login_required
def home(request):
  context = {'user': request.user}
  return render(request, "home.html", context)

@login_required
def create_character(request):
  context = {}
  context['edit'] = False
  context['header'] = 'Create Character'
  context['title'] = 'Create Character and save!'
  return render(request, "create.html", context)

@login_required
def edit_character(request, index):
  context = {}
  context['edit'] = True
  context['header'] = 'Edit Character'
  context['title'] = 'Edit Character and save!'
  if request.method == 'GET':
    try:
      chars = Character.objects.filter(owner=request.user)
      length = len(chars)
      index = int(index)
      context['next'] = (index + 1) % length
      context['prev'] = (index - 1) % length
      context['character'] = chars[index]
      return render(request, "create.html", context)
    except ObjectDoesNotExist:
      pass

    # User has no characters, give them option to create one
    except ZeroDivisionError:
      context['edit'] = False
      context['header'] = 'Create Character'
      context['title'] = 'Create Character and save!'
      return render(request, "create.html", context)
  return redirect('home')

@login_required
@transaction.atomic
def save_new_character(request):

  form = UpdateCharacterForm(request.POST)

  if not form.is_valid():
    return 'error'

  # Create a new character with the form data
  new_char = Character(owner=request.user, 
              name=form.cleaned_data['char_name'],
              description=form.cleaned_data['description'],
              rating=0,
              image=form.cleaned_data['img'],
              svg_html=form.cleaned_data['svg_text'],
              lc_json=form.cleaned_data['snap_json'])

  # Save new character data
  new_char.save()

  # Response to the ajax call with key of new character
  return HttpResponse(new_char.pk)

@login_required
@transaction.atomic
def update_character(request, id):

  # Try to get character with this ID
  char_to_update = get_object_or_404(Character, pk=id)

  # No valid character with ID, return 404
  if not char_to_update:
    raise Http404

  # Create our form
  form = UpdateCharacterForm(request.POST)

  # Check that form is valid
  if not form.is_valid():
    return 'error'

  # Update character with cleaned parameters
  char_to_update.name = form.cleaned_data['char_name']
  char_to_update.description = form.cleaned_data['description']
  char_to_update.image = form.cleaned_data['img']
  char_to_update.svg_html = form.cleaned_data['svg_text']
  char_to_update.lc_json = form.cleaned_data['snap_json']

  # Save updated character to database
  char_to_update.save()

  # Redirect user to home page
  return redirect('home')

# Sorts the rankings page
@login_required
def ranking_sort(request):

  if request.method == 'POST':

    # Put POST data into a Django Form
    form = SortRankingsForm(request.POST)

    # Perform form validation on POST data
    if not form.is_valid():
      raise Http404

    if form.cleaned_data['ascending'] == 'false':
      if form.cleaned_data['data'] == 'name':
        all_chars = Character.objects.all().order_by('-name')
      elif form.cleaned_data['data'] == 'owner':
        all_chars = Character.objects.all().order_by('-owner__username')
      else:
        all_chars = Character.objects.all().order_by('rating')
    else:
      if form.cleaned_data['data'] == 'name':
        all_chars = Character.objects.all().order_by('name')
      elif form.cleaned_data['data'] == 'owner':
        all_chars = Character.objects.all().order_by('owner__username')
      else:
        all_chars = Character.objects.all().order_by('-rating')

    context = {'characters': all_chars}

    return render(request, 'characters.json', context, content_type='application/json')

  return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def ranking(request):

  # Get request to rankings page
  if request.method == 'GET':
    # Order characters by descending rating
    all_chars = Character.objects.all().order_by('-rating')

    # Render ranking template with character data
    return render(request, "ranking.html", {'characters': all_chars, 'form': SearchForm()})

  # Grab form data in post
  form = SearchForm(request.POST)

  # Check for valid form
  if not form.is_valid():
    # Default action: Just order all characters by rating
    all_chars = Character.objects.all().order_by('-rating')

    # Render template of all character data
    return render(request, "ranking.html", {'characters': all_chars, 'form': SearchForm()})

  # Grab search text from cleaned form
  search_text = form.cleaned_data['search_text']

  # Filter searched characters by name or name of owner
  searched_chars_name = Character.objects.filter(name__icontains=search_text).order_by('-rating')
  searched_chars_owner = Character.objects.filter(owner__username__icontains=search_text).order_by('-rating')

  # Get union of two searched sets
  searched_chars = searched_chars_name | searched_chars_owner;

  # Return ranking template with results of search
  return render(request, "ranking.html", {'characters': searched_chars, 'form': SearchForm()})

@login_required
@transaction.atomic
def choose(request, char_id):
  character = get_object_or_404(Character, pk=char_id)
  if not character:
    raise Http404
  if character.picked_attr is True:
    raise Http404
  if request.user.id != character.owner.pk:
    raise Http404
  context = {}
  util = Util()
  context['char_id'] = char_id

  if not character.given_attributes or character.given_attributes.count() == 0:
    rand_attrs = util.get_five_random_attributes()
    character.given_attributes = rand_attrs
    character.save()
  else:
    rand_attrs = character.given_attributes.all()

  context['attributes'] = rand_attrs
  context['picked'] = util.get_attributes(char_id)
  return render(request, "choose.html", context)

@login_required
def save_attr(request):
  if(request.method == 'GET'):
    raise Http404
  if(not util.validate_save_attr(request)):
    raise Http404
  return HttpResponse(200)

@login_required
def pick(request):
  if request.method == 'GET':
    raise Http404
  util = Util()
  attr = util.validate_pick(request)
  if(attr):
    data = serializers.serialize("json", [attr])
    return HttpResponse(data, content_type="application/json")
  raise Http404

@login_required
def attr_media(request, id):
  # Get attribute with this ID
  attribute = get_object_or_404(Attribute, pk=id)

  # Invalid attribute ID, raise 404
  if not attribute:
    raise Http404

  # Guess content type of attribute image
  content_type = guess_type(attribute.image.name)
  return HttpResponse(attribute.image, content_type)

@login_required
def char_media(request, id):
  # Try to get character with this ID
  character = get_object_or_404(Character, pk=id)

  # Invalid ID, raise 404
  if not character:
    raise Http404

  # Guess content type of character image
  content_type = guess_type(character.image.name)
  return HttpResponse(character.image, content_type)

@login_required
def profile(request, id):
  context = {}

  user = get_object_or_404(User, pk=int(id))
  if not user:
    raise Http404

  chars = Character.objects.filter(owner=user)
  context['chars'] = chars
  return render(request, "user_profile.html", context)

@login_required
def char_profile(request, id):
  context = {}

  # Get character associated with this ID
  char = get_object_or_404(Character, pk=id)

  # Invalid ID submitteed to URL, raise 404
  if not char:
    raise Http404

  # Grab context information to render template
  context['user_profile'] = False
  context['character'] = char
  context['attributes'] = char.attributes.all().order_by('-rating')

  # Render profile template
  return render(request, "profile.html", context)

@login_required
def battle(request):
  return render(request, "battle.html", {})

@login_required
def write(request):
  context = {}

  if 'challenge' in request.GET and request.GET['challenge']:
    try:
      context['challenge'] = Challenge.objects.get(pk=request.GET['challenge'])
    except:
      redirect('battle')
  return render(request, 'write.html', context)

@login_required
@transaction.atomic
def submit_battle(request):

  if request.method == 'POST':
    form = WriteBattleForm(request.POST)

    if not form.is_valid():
      return render(request, 'write.html', {})

    submitted_text = form.cleaned_data['html']
    try:
      battle = Battle.objects.get(challenge__pk=int(form.cleaned_data['challenge']))
      challenge = battle.challenge
      if request.user.id == battle.character1.owner.pk:
        battle.argument1 = submitted_text
        battle.submitted1 = True
      else:
        battle.argument2 = submitted_text
        battle.submitted2 = True

      if battle.submitted1 is True and battle.submitted2 is True:
        battle.ready_to_vote = True
        challenge.finished = True
        challenge.save()

      battle.save()
    except:
      pass

    return render(request, 'write.html', {})
  else:
    return redirect('home')

@login_required
@transaction.atomic
def vote(request):
  context = {}

  # Grab current battles that are ready to be voted, not complete, and haven't been voted on by this user
  current_battles = Battle.objects.filter(ready_to_vote=True, complete=False).exclude(users_voted__pk=request.user.pk)

  # Grab battles that this user has already voted in
  voted_battles = Battle.objects.filter(users_voted__pk=request.user.pk)

  # Build our context object
  context['current_battles'] = current_battles
  context['voted_battles'] = voted_battles

  if request.method == 'POST':

    # Django form validation for POST
    form = VoteForm(request.POST)

    if not form.is_valid():
      raise Http404

    # Try to get battle from ID and character from ID
    try:
      # Exclude battles that this user has voted in, battles which are complete, and battles not yet ready to vote
      battle = Battle.objects.exclude(users_voted__pk=request.user.pk, complete=True, ready_to_vote=False).get(pk=form.cleaned_data['battle'])
      character = Character.objects.get(pk=form.cleaned_data['character'])
    except:
      return render(request, 'vote.html', context)

    # Increment vote count
    if character == battle.character1:
      battle.votes1 = battle.votes1 + 1
    elif character == battle.character2:
      battle.votes2 = battle.votes2 + 1
    else:
      return render(request, 'vote.html', context)

    # Battle completion
    if battle.votes1 + battle.votes2 == 3:
      battle.complete = True

      # Check who has more votes, increase rating of character with more votes
      if battle.votes1 > battle.votes2:
        battle.character1.rating = battle.character1.rating + 1
        battle.character1.save()
      else:
        battle.character2.rating = battle.character2.rating + 1
        battle.character2.save()

    # Add this user to the list of users who voted on this battle already
    battle.users_voted.add(request.user)

    # Save our battle object to database
    battle.save()

  return render(request, 'vote.html', context)

@login_required
def history(request):
  context = {}

  context['battles'] = Battle.objects.filter(complete=True)

  return render(request, 'history.html', context)