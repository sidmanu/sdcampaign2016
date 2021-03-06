from dialogues.models import *
from django.db.models import Count
import datetime

#TODO: Make it faster. Instead of counting objects, read stats entries 
def get_total_campaign_count():
    return Campaign.objects.count()

def get_top_campaigns():
    return Campaign.objects.all()[:10]

def get_campaign_by_id(campaign_id):
    return Campaign.objects.get(id=campaign_id)

def get_pledged_daimoku_total_hours_by_campaign_id(campaign_id):
    return get_pledged_daimoku_total_minutes_by_campaign_id(campaign_id) / 60

def get_pledged_daimoku_total_minutes_by_campaign_id(campaign_id):
    camp = Campaign.objects.get(id=campaign_id)
    daimokus = DaimokuCommitment.objects.filter(campaign=camp)
    total_minutes = 0
    for d in daimokus:
        total_minutes += d.duration_minutes
    return total_minutes


def get_daimoku_total_hours_by_campaign_id(campaign_id):
    return get_daimoku_total_minutes_by_campaign_id(campaign_id) / 60

def get_daimoku_total_minutes_by_campaign_id(campaign_id):
    camp = Campaign.objects.get(id=campaign_id)
    daimokus = Daimoku.objects.filter(campaign=camp)
    total_minutes = 0
    for d in daimokus:
        total_minutes += d.duration_minutes
    return total_minutes

def get_most_recent_daimoku_pledges(campaign_id):
    camp = Campaign.objects.get(id=campaign_id)
    daimokus = DaimokuCommitment.objects.filter(campaign=camp).order_by('-committed_on_date')[:10]

    return daimokus


def get_most_recent_daimoku_contributions(campaign_id):
    camp = Campaign.objects.get(id=campaign_id)
    daimokus = Daimoku.objects.filter(campaign=camp).order_by('-daimoku_date')[:10]

    return daimokus


def get_national_homevisit_count():
    return HomeVisit.objects.count()

def get_daily_count_list():
    today = datetime.date.today()
    fifteen_days_ago = today - datetime.timedelta(days=15)
    return Dialogue.objects.filter(dialogue_date__gte=fifteen_days_ago).values('dialogue_date').annotate(count=Count('dialogue_date')).order_by('dialogue_date')

def get_district_wise_hv_count_zero():
    districts = District.objects.all()
    zero_dists = list()
    for dist in districts:
        if dist.homevisit_set.count() == 0:
            item = {}
            item['district_name'] = dist.name
            zero_dists.append(item)
    return zero_dists

def get_district_wise_hv_count():
    return HomeVisit.objects.all().values('district__name').annotate(count=Count('district')).order_by('count')


def get_district_wise_dialogues_count_zero():
    districts = District.objects.all()
    zero_dists = list()
    for dist in districts:
        if dist.dialogue_set.count() == 0:
            item = {}
            item['district_name'] = dist.name
            zero_dists.append(item)
    return zero_dists

def get_district_wise_dialogues_count():
    return Dialogue.objects.all().values('district__name').annotate(count=Count('district')).order_by('count')

def get_all_dialogues():
    return Dialogue.objects.all()

def get_chapter_total_count(chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    districts = chapter.district_set.all()
    count = 0
    for district in districts:
        count += Dialogue.objects.filter(district=district).count()
    return count 


def get_areawise_total_count():
    areas = Area.objects.all()
    data_list = []
    for area in areas:
        ele = {}
        ele['name'] = area.name
        area_count = 0
        for chapter in area.chapter_set.all():
            area_count += get_chapter_total_count(chapter.id)
            
        ele['area_count'] = area_count
        data_list.append(ele)
    return data_list


def get_chapter_dialogues_in_date_range(start_date, end_date, chapter_id):
    districts = Chapter.objects.get(id=chapter_id).district_set.all()
    data_list = []
    for district in districts:
        ele = {}
        ele['district_name'] = district.name
        ele['dialogues'] = Dialogue.objects.filter(district=district,
                    dialogue_date__range=[start_date, end_date])
        data_list.append(ele)
    return data_list

def get_dialogues_in_date_range(start_date, end_date):
    return Dialogue.objects.filter(dialogue_date__range=[start_date, end_date])

def get_all_gas():
    return GA.objects.all()

def get_all_chapters():
    return Chapter.objects.all().order_by('name')

def get_areas_in_ga(ga_id):
    ga = GA.objects.get(id=ga_id)
    return ga.area_set.all()

def get_chapters_in_area(id):
    area = Area.objects.get(id=id)
    return area.chapter_set.all()

def get_districts_in_chapter(id):
    chapter = Chapter.objects.get(id=id)
    return chapter.district_set.all()

def get_district_by_id(id):
    return District.objects.get(id=id)

def get_district_structure_string_by_id(id):
    d = District.objects.get(id=id)
    str = "%s > %s > %s > %s > %s"%(d.parent.parent.parent.parent.name,
                d.parent.parent.parent.name,
                d.parent.parent.name,
                d.parent.name,
                d.name)
    return str


def get_home_visits_list_by_email(email):
    return HomeVisit.objects.filter(visitor_email=email)

def get_guest_invites_list_by_email(email):
    return GuestInvite.objects.filter(member_email=email)


def get_dialogues_list_by_email(email):
    return Dialogue.objects.filter(member_email=email)

#Home Visits 

def get_guest_invites_count_by_district_id(district_id):
    dist = District.objects.get(id=district_id)
    return GuestInvite.objects.filter(district=dist).count()

def get_dialogue_count_by_district_id(district_id):
    dist = District.objects.get(id=district_id)
    return Dialogue.objects.filter(district=dist).count()   


def get_home_visits_count_by_district_id(district_id):
    dist = District.objects.get(id=district_id)
    return HomeVisit.objects.filter(district=dist).count()  

def get_this_month_guest_invites_by_district_id(district_id):
    dist = District.objects.get(id=district_id)
    today = datetime.datetime.today()
    month_start = today - datetime.timedelta(days=(today.day - 1))
    return GuestInvite.objects.filter(district=dist, invite_date__gte=month_start)


def get_this_month_home_visits_by_district_id(district_id):
    dist = District.objects.get(id=district_id)
    today = datetime.datetime.today()
    month_start = today - datetime.timedelta(days=(today.day - 1))
    return HomeVisit.objects.filter(district=dist, visit_date__gte=month_start)

def get_this_month_guest_invites_count_by_district_id(district_id):
    dist = District.objects.get(id=district_id)
    today = datetime.datetime.today()
    month_start = today - datetime.timedelta(days=(today.day - 1))
    return GuestInvite.objects.filter(district=dist, invite_date__gte=month_start).count()

def get_this_month_home_visits_count_by_district_id(district_id):
    dist = District.objects.get(id=district_id)
    today = datetime.datetime.today()
    month_start = today - datetime.timedelta(days=(today.day - 1))
    return HomeVisit.objects.filter(district=dist, visit_date__gte=month_start).count()

