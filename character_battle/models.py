from django.db import models

from django.contrib.auth.models import User
import datetime
from django.template import loader, Context

# Model for a user's profile since we need more data than the Django User model provides
class UserProfile(models.Model):

	# Attach to a single User
	user = models.OneToOneField(User)


# Model for a possible character attribute
class Attribute(models.Model):

	# A title for this particular attribute
	title = models.CharField(max_length=42)

	# A description of this attribute
	description = models.CharField(max_length=255)

	# The rating of this particular attribute
	rating = models.IntegerField()

	# An image of this character as created by the user in HTML5 Canvas
	image = models.ImageField(blank=True)

	def __unicode__(self):
		return self.title

# Model for a character created by a user
class Character(models.Model):
	# The owner of this character
	owner = models.ForeignKey(User)

	# Attributes that this character can have
	attributes = models.ManyToManyField(Attribute, blank=True, related_name="attributes")

	given_attributes = models.ManyToManyField(Attribute, blank=True, related_name="given_attributes")

	# The name of this character.
	name = models.CharField(max_length=42)

	# A user defined description of this character
	description = models.CharField(max_length=255)

	# The rating of this character as rated by other users
	rating = models.IntegerField()

	# The creation date of this character
	created = models.DateTimeField(default=datetime.datetime.now)

	# An image of this character as created by the user in HTML5 Canvas
	image = models.TextField(default="")

	# SVG HTML representation of the image drawn on Canvas
	svg_html = models.TextField(default="", blank=True)

	# Literally Canvas JSON object
	lc_json = models.TextField(default="", blank=True)

	picked_attr = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

	@property
	def dropdown_html(self):
		itemTemplate = loader.get_template('char_dropdown.html')
		context = Context({'character':self})
		return itemTemplate.render(context).replace('\n','')

	@property
	def display_html(self):
		itemTemplate = loader.get_template('char_display.html')
		context = Context({'character':self})
		return itemTemplate.render(context).replace('\n','')


class Challenge(models.Model):
	challenger = models.ForeignKey(Character, related_name="initiliazer")
	challenging = models.ForeignKey(Character, related_name="accepter")
	user_challenger = models.ForeignKey(User, related_name="init")
	user_challenging = models.ForeignKey(User, related_name="accept")
	accept = models.BooleanField()
	finished = models.BooleanField(default=False)

	@property
	def challenging_html(self):
		itemTemplate = loader.get_template('challenging.html')
		context = Context({'challenge':self})
		return itemTemplate.render(context).replace('\n','')

	@property
	def challenger_html(self):
		itemTemplate = loader.get_template('challenger.html')
		context = Context({'challenge':self})
		return itemTemplate.render(context).replace('\n','')

	@property
	def battles_html(self):
		itemTemplate = loader.get_template('battles.html')
		context = Context({'challenge':self})
		return itemTemplate.render(context).replace('\n','')

	def __unicode__(self):
		return self.challenger.name + ' vs. ' + self.challenging.name



# Model for a battle between two characters
class Battle(models.Model):
	challenge = models.ForeignKey(Challenge)

	# The two characters engaged in this battle
	character1 = models.ForeignKey(Character, related_name="first")
	character2 = models.ForeignKey(Character, related_name="second")

	# The two arguments from each side for this battle
	argument1 = models.CharField(max_length=1024, blank=True)
	argument2 = models.CharField(max_length=1024, blank=True)

	# The votes for each side of this argument
	votes1 = models.IntegerField(default=0)
	votes2 = models.IntegerField(default=0)

	submitted1 = models.BooleanField()
	submitted2 = models.BooleanField()

	ready_to_vote = models.BooleanField(default=False)
	complete = models.BooleanField(default=False)

	users_voted = models.ManyToManyField(User)
