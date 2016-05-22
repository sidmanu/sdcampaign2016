from django.core.validators import RegexValidator
from django.db import models


class struct_unit(models.Model):
	name = models.CharField(max_length=60)
	dialogue_count = models.BigIntegerField(null=True)
	home_visit_count = models.BigIntegerField(null=True)


class Region(struct_unit):
	def __str__(self):
		return "Region: %s"%self.name

class GA(struct_unit):
	parent = models.ForeignKey(Region)
	def __str__(self):
		return "GA: %s"%self.name

class Area(struct_unit):
	parent = models.ForeignKey(GA)
	def __str__(self):
		return "Area: %s"%self.name

class Chapter(struct_unit):
	parent = models.ForeignKey(Area)
	def __str__(self):
		return "Chapter: %s"%self.name

class District(struct_unit):
	parent = models.ForeignKey(Chapter)
	def __str__(self):
		return "District: %s in Chapter %s"%(self.name, self.parent.name)

class Dialogue(models.Model):
	member_name = models.CharField(max_length=60)
	friend_name = models.CharField(max_length=60)
	member_email = models.CharField(max_length=60)
	district = models.ForeignKey(District)
	dialogue_date = models.DateField()
	my_story = models.TextField()

	def __str__(self):
		return "Diag in %s district: %s spoke to %s "%(self.district.name,
				self.member_name, self.friend_name)

class HomeVisit(models.Model):
	visitor_name = models.CharField(max_length=30)
	visited_name = models.CharField(max_length=30)
	visitor_email = models.CharField(max_length=30)
	district = models.ForeignKey(District)
	visit_date= models.DateField()

	def __str__(self):
		return "Home Visit in %s district: %s visited %s "%(self.district.name,
				self.visitor_name, self.visited_name)

