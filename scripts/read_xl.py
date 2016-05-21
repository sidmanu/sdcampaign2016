import os
import xlrd
from xlrd.sheet import ctype_text   

#open worksheet
xl_wb = xl_workbook = xlrd.open_workbook('struct.xls')
sheet_names = xl_workbook.sheet_names()
xl_sheet = xl_workbook.sheet_by_index(0)


import django
#setup django
os.environ["DJANGO_SETTINGS_MODULE"] =  "dialoguesforpeace.settings"
django.setup()
from dialogues.models import *
row = xl_sheet.row(0)  

def try_create_ga(ga_name):
	try:
		d = GA.objects.get(name=ga_name)
		print "found! %d: %s"%(d.id, d.name)
	except:
		l = Leader.objects.get(id=5)
		z = GA(name=ga_name, leader=l)
		z.save()
		print "GA %s created!"%(ga_name)

def try_create_area(child, parent):
	try:
		d = Area.objects.get(name=child)
		#print "found! %d: %s"%(d.id, d.name)
	except:
		l = Leader.objects.get(id=5)
		p = GA.objects.get(name=parent)
		r = Area(name=child, leader=l, parent=p)
		r.save()
		print "Area %s created!"%(child)


def try_create_chapter(child, parent):
	try:
		d = Chapter.objects.get(name=child)
		#print "found! %d: %s"%(d.id, d.name)
	except:
		l = Leader.objects.get(id=5)
		p = Area.objects.get(name=parent)
		r = Chapter(name=child, leader=l, parent=p)
		r.save()
		print "Chapter %s created!"%(child)



def try_create_district(child, parent):
	try:
		d = District.objects.get(name=child)
		#print "found! %d: %s"%(d.id, d.name)
	except:
		l = Leader.objects.get(id=5)
		p = Chapter.objects.get(name=parent)
		r = District(name=child, leader=l, parent=p)
		r.save()
		print "District %s created!"%(child)



for i in range(1,xl_sheet.nrows):
	row = xl_sheet.row(i)
	for idx, cell_obj in enumerate(row):
		cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
		if idx == 0:
			ga = cell_obj.value.strip()
		if idx == 1:
			area = cell_obj.value.strip()
		if idx == 2:
			chapter = cell_obj.value.strip()
		if idx == 3:
			district = cell_obj.value.strip()

	#print "%s, %s, %s, %s"%(district, chapter, area, ga)

	try_create_ga(ga)
	try_create_area(area, ga)
	try_create_chapter(chapter, area)
	try_create_district(district, chapter)
