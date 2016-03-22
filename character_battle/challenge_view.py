from character_battle.views import *

#Global variables
util = Util()

@login_required
def challenging(request):
	return render(request, 'challenging.json', {"challenges":util.get_challenging(request.user)}, content_type="application/json")

@login_required
def challenger(request):
	return render(request, 'challenger.json', {"challenges":util.get_challengers(request.user)}, content_type="application/json")

@login_required
def battles(request):
	return  render(request, 'battles.json', {"challenges":util.get_curr_battles(request.user)}, content_type="application/json")

@login_required
@transaction.atomic
def accept(request, id):
	challenge = util.validate_accept(id)
	challenge.accept = True
	new_battle = Battle(challenge=challenge, character1=challenge.challenger, character2=challenge.challenging, submitted1=False, submitted2=False , complete=False)
	challenge.save()
	new_battle.save()
	return HttpResponse(200)

@login_required
@transaction.atomic
def decline(request, id):
	challenge = util.validate_decline(id)
	challenge.delete()
	return HttpResponse(200)

@login_required
def stats(request):
	#TODO: the whole thing
	return  HttpResponse(0)

@login_required
def char_dropdown(request):
	return  render(request, 'char_dropdown.json', {"characters":util.get_all_user_chars(request.user)}, content_type="application/json")

@login_required
def char_display(request):
	user = util.validate_char_display(request)
	print user
	return  render(request, 'char_display.json', {"characters":util.get_all_user_chars(user)}, content_type="application/json")


@login_required
@transaction.atomic
def challenge(request):
  (challenger, challenging) = util.validate_challenge(request)
  (user_challenger, user_challenging) = (challenger.owner, challenging.owner)
  print user_challenger, user_challenging
  new_challenge = Challenge(challenger=challenger, challenging=challenging, user_challenger=user_challenger, user_challenging=user_challenging, accept=False)
  new_challenge.save()
  return HttpResponse(200)