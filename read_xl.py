import os
import xlrd
from xlrd.sheet import ctype_text   

import django
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
os.environ["DJANGO_SETTINGS_MODULE"] =  "dialoguesforpeace.settings"
django.setup()
from dialogues.models import *
#scan through all excel files in this directory


#---------------
#Utility API
#---------------
def try_create_region(region_name):
	try:
		d = Region.objects.get(name=region_name)
		#print "found! %d: %s"%(d.id, d.name)
	except ObjectDoesNotExist:
		z = Region(name=region_name)
		z.save()
		#print "Region %s created!"%(region_name)

def try_create_ga(child, parent):
	try:
		d = GA.objects.get(name=child)
		#print "found! %d: %s"%(d.id, d.name)
	except MultipleObjectsReturned:
		print "Duplicate GA %s in Region%s"%(child, parent)
	except ObjectDoesNotExist:
		p = Region.objects.get(name=parent)
		r = GA(name=child, parent=p)
		r.save()
		#print "GA %s created!"%(child)


def try_create_area(child, parent):
	try:
		d = Area.objects.get(name=child)
	except MultipleObjectsReturned:
		print "Duplicate Area %s in GA %s"%(child, parent)
	except ObjectDoesNotExist:
		p = GA.objects.get(name=parent)
		r = Area(name=child, parent=p)
		r.save()
		#print "Area %s created!"%(child)


def try_create_chapter(child, parent):
	try:
		d = Chapter.objects.get(name=child)
	except MultipleObjectsReturned:
		print "Duplicate Chapter %s in Area %s"%(child, parent)
	except ObjectDoesNotExist:
		p = Area.objects.get(name=parent)
		r = Chapter(name=child, parent=p)
		r.save()
		#print "Chapter %s created!"%(child)



def try_create_district(child, parent):
	try:
		d = District.objects.get(name=child)
		print "Duplicate District found %s in %s chapter"%(child, parent)
		#create district with chapter name appended to district name
		p = Chapter.objects.get(name=parent)
		dist_name = "%s - %s chapter"%(child,parent)
		r = District(name=dist_name, parent=p)
		r.save()
		print "created district %s to avoid nameclash"%dist_name
	except ObjectDoesNotExist:
		p = Chapter.objects.get(name=parent)
		r = District(name=child, parent=p)
		r.save()
		#print "District %s created!"%(child)

def parse_mds_leader_organogram(filename):
	#open worksheet
	xl_wb = xl_workbook = xlrd.open_workbook(filename)
	sheet_names = xl_workbook.sheet_names()
	xl_sheet = xl_workbook.sheet_by_index(0)

	from dialogues.models import *
	row = xl_sheet.row(0)  

	district_count = 0

	for i in range(8,xl_sheet.nrows):
		row = xl_sheet.row(i)
		valid_dist = False
		
		for idx, cell_obj in enumerate(row):
		
			cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
			if idx == 0:
				region = cell_obj.value.strip()
			if idx == 1:
				ga = cell_obj.value.strip()
			if idx == 2:
				area = cell_obj.value.strip()
			if idx == 3:
				chapter = cell_obj.value.strip()
			if idx == 4:
				district = cell_obj.value.strip()
			if idx == 6:
				structure = cell_obj.value.strip()
				if structure.lower() == 'district':
					district_count += 1
					valid_dist = True
					#print "%s, %s, %s, %s, %s"%(region, ga, area, chapter, district)
					
		if valid_dist:
			try_create_region(region)
			try_create_ga(ga, region)
			try_create_area(area, ga)
			try_create_chapter(chapter, area)
			try_create_district(district, chapter)

	print "Total number of districts added: %d"%district_count
	return district_count

#============ script begins ===============

total_district_count = 0
for i in os.listdir(os.path.join(os.getcwd(), 'scripts/')):
    if i.endswith(".xls"): 
	print "Parsing %s"%i
	total_district_count += parse_mds_leader_organogram(os.path.join(os.getcwd(),'scripts', i))

print "Total number of districts added pan India: %d"%total_district_count
