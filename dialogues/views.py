from django.shortcuts import render

from dialogues.models import * 
from dialogues.serializers import *
import dialogues.queries as q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
import json

import datetime
from django.core.mail import send_mail



from rest_framework.permissions import IsAdminUser
from rest_framework import filters 
from rest_framework import generics

class DialogueView(generics.ListAPIView):
    serializer_class = DialogueSerializer

    model = Dialogue
    queryset = Dialogue.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('member_name', 'dialogue_date')

def home_visit_index(request):
    context = {}
    context['ga_list'] = q.get_all_gas()
    return render(request, 'dialogues/home_visit_index.html', context)


@csrf_exempt
def submit_daimoku_commitment(request):
    context = {}
    if request.POST:
        campaign_id= int(request.POST['campaign_id'])
        member_name = request.POST['member_name']
        member_email = request.POST['member_email']
        daimoku_minutes= request.POST['daimoku_minutes']

        campaign = q.get_campaign_by_id(campaign_id)
        try:
            pledge = DaimokuCommitment(member_name=member_name,
                            member_email=member_email,
                            committed_on_date=datetime.date.today(),
                            campaign=campaign,
                            duration_minutes=daimoku_minutes)
            pledge.save()
            context['message']='Your pledge has been successfully reported!'
            context['contribution'] = contribution
        except Exception, e:
            print e
            context['message'] = 'Error in submitting contribution'
            context['error'] = e

    context['campaign'] = campaign 
    context['total_daimoku_minutes'] = q.get_daimoku_total_minutes_by_campaign_id(campaign_id)
    context['total_daimoku_hours'] = q.get_daimoku_total_hours_by_campaign_id(campaign_id)
    context['contributions'] = q.get_most_recent_daimoku_contributions(campaign_id)
    context['pledges'] = q.get_most_recent_daimoku_pledges(campaign_id)
    context['total_pledged_hours'] = q.get_pledged_daimoku_total_hours_by_campaign_id(campaign_id)
    context['total_pledged_minutes'] = q.get_pledged_daimoku_total_minutes_by_campaign_id(campaign_id)


    return render(request, 'dialogues/daimoku_campaign.html', context)


@csrf_exempt
def submit_daimoku(request):
    context = {}
    if request.POST:
        campaign_id= int(request.POST['campaign_id'])
        member_name = request.POST['member_name']
        member_email = request.POST['member_email']
        daimoku_minutes= request.POST['daimoku_minutes']

        campaign = q.get_campaign_by_id(campaign_id)
        try:
            contribution = Daimoku(member_name=member_name,
                            member_email=member_email,
                            daimoku_date=datetime.date.today(),
                            campaign=campaign,
                            duration_minutes=daimoku_minutes)
            contribution.save()
            context['message']='Your contribution has been successfully reported!'
            context['contribution'] = contribution
        except Exception, e:
            print e
            context['message'] = 'Error in submitting contribution'
            context['error'] = e

    context['campaign'] = campaign 
    context['total_daimoku_minutes'] = q.get_daimoku_total_minutes_by_campaign_id(campaign_id)
    context['total_daimoku_hours'] = q.get_daimoku_total_hours_by_campaign_id(campaign_id)
    context['contributions'] = q.get_most_recent_daimoku_contributions(campaign_id)
    context['pledges'] = q.get_most_recent_daimoku_pledges(campaign_id)
    context['total_pledged_hours'] = q.get_pledged_daimoku_total_hours_by_campaign_id(campaign_id)
    context['total_pledged_minutes'] = q.get_pledged_daimoku_total_minutes_by_campaign_id(campaign_id)

    return render(request, 'dialogues/daimoku_campaign.html', context)



@csrf_exempt
def create_campaign(request):
    context = {}
    if request.POST:
        campaign_name = request.POST['campaign_name']
        campaign_type = request.POST['campaign_type']
        campaign_target = request.POST.get('campaign_target', '500')
        start_date = request.POST['start_date']
        start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        target_date = request.POST["target_date"]
        target_date = datetime.datetime.strptime(target_date, '%d-%m-%Y').strftime('%Y-%m-%d')

        target_unit = request.POST['campaign_unit']
        new_campaign = Campaign(name=campaign_name,
                            campaign_type=campaign_type,
                            target_value=campaign_target,
                            target_unit=target_unit,
                            start_date=start_date,
                            end_date=target_date) 
        new_campaign.save()
    context['campaign'] = new_campaign
    context['str_campaign_id'] = str(new_campaign.id)

    return render(request, 'dialogues/campaign_created.html', context)




def dist_direct_home_visit_index(request, district_id):
    context = {}
    context['district_id'] = district_id
    context['dist'] = q.get_district_by_id(district_id)
    context['total_hv_count'] = q.get_home_visits_count_by_district_id(district_id)
    context['month_hv_count'] = q.get_this_month_home_visits_count_by_district_id(district_id)
    context['total_gi_count'] = q.get_guest_invites_count_by_district_id(district_id)
    context['month_gi_count'] = q.get_this_month_guest_invites_count_by_district_id(district_id)
    context['month_home_visit_list'] = q.get_this_month_home_visits_by_district_id(district_id)
    context['month_guest_invite_list'] = q.get_this_month_guest_invites_by_district_id(district_id)
    return render(request, 'dialogues/hv_direct_district_summary.html', context)

def campaign_index(request, campaign_id):
    context = {}
    campaign = q.get_campaign_by_id(campaign_id)
    context['campaign'] = campaign
    if 'daimoku' in campaign.campaign_type.lower():
        context['total_daimoku_minutes'] = q.get_daimoku_total_minutes_by_campaign_id(campaign_id)
        context['total_daimoku_hours'] = q.get_daimoku_total_hours_by_campaign_id(campaign_id)
        context['contributions'] = q.get_most_recent_daimoku_contributions(campaign_id)
        context['pledges'] = q.get_most_recent_daimoku_pledges(campaign_id)
        context['total_pledged_hours'] = q.get_pledged_daimoku_total_hours_by_campaign_id(campaign_id)
        context['total_pledged_minutes'] = q.get_pledged_daimoku_total_minutes_by_campaign_id(campaign_id)
        return render(request, 'dialogues/daimoku_campaign.html', context)
    elif 'home_visit' in campaign.campaign_type.lower():
        return render(request, 'dialogues/homevisit_campaign.html', context)
    elif 'dialogue' in campaign.campaign_type.lower():
        return render(request, 'dialogues/dialogue_campaign.html', context)

    return render(request, 'dialogues/error.html', context)

def index(request):
    context = {}
    context['total_campaign_count'] = q.get_total_campaign_count()
    context['top_campaign_list'] = q.get_top_campaigns()
    return render(request, 'dialogues/index.html', context)

def logout_user(request):
    context = {}
    context['global_message'] = "You've been logged out."
    logout(request)
    return HttpResponseRedirect('/')

def send_my_activities_email(email_id, dialogues, hv):
    recipients = [email_id]
    subject = 'My Activities Summary - bodhibuddy.in'
    sender = 'noreply@bodhibuddy.in'
    content = """
Dear Bodhisattva,

Here is your dialogue history: 

"""
    
    
    if len(dialogues) == 0:
        content += "You have no recorded dialogues!"

    count = 0
    for d in dialogues:
        count += 1
        line = "%d) %s on %s in %s district\n"%(count, d.friend_name, str(d.dialogue_date),
                    d.district.name)
        content += line
        
    if len(hv) == 0:
        content += "You have no recorded home visits!"
    else:
        content += "\n\nHere are the home visits you recorded:\n\n"

    count = 0
    for d in hv:
        count += 1
        line = "%d) %s on %s in %s district\n"%(count, d.visited_name, str(d.visit_date),
                    d.district.name)
        content += line
    
    
    content += '\nThank You!\nbodhibuddy.in'
    send_mail(subject, content, sender, recipients)


def my_activities(request):
    context = {}
    if request.POST:
        email = request.POST['email']
        dialogues = q.get_dialogues_list_by_email(email)
        home_visits = q.get_home_visits_list_by_email(email)
        send_my_activities_email(email, dialogues, home_visits)
        context['display_message'] = 'If entered email-id was valid, you\'ll receive an email shortly!'

    return render(request, 'dialogues/my_activities.html', context)

def login_user(request):
    context = {}
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dialogues/leaders_dashboard/')
    return render(request, 'dialogues/login.html', context)

@login_required
def leaders_dashboard(request):
    context = {}
    total_count = q.get_total_count()
    context['total_count'] = total_count
    context['all_chapter_list'] = q.get_all_chapters() 
    context['daily_count_list'] = q.get_daily_count_list()
    context['district_count_list'] = q.get_district_wise_dialogues_count()
    context['district_hv_count_list'] = q.get_district_wise_hv_count()
    context['district_count_zero_list'] = q.get_district_wise_dialogues_count_zero()
    context['district_hv_count_zero_list'] = q.get_district_wise_hv_count_zero()
    context['areawise_total_count'] = q.get_areawise_total_count()
    return render(request, 'dialogues/leaders_dashboard.html', context)

@csrf_exempt
def ajax_get_matching_district(request):
    mimetype= 'application/json'
    dist_str= request.GET.get('dist_str','')
    #TODO: Temporarily returning
    #if len(dist_str) < 3:
    if True:
        data = []
        return HttpResponse(data, mimetype)
    districts = District.objects.filter(name__contains=dist_str)
    results = {}
    suggestions = []
    for dist in districts:
        dist_json = {}
        dist_json['value'] = '%s (Chapter: %s)'%(dist.name, dist.parent.name) 
        dist_json['data'] = dist.name
        dist_json['id'] = dist.id
        suggestions.append(dist_json)
    results['suggestions'] = suggestions
    data = json.dumps(results)      
    return HttpResponse(data, mimetype)


def ajax_get_district_summary(request, district_id):
    context = {}
    context['district_id'] = district_id
    context['dist'] = q.get_district_by_id(district_id)
    context['hv_count'] = q.get_home_visits_count_by_district_id(district_id)
    context['dialogue_count'] = q.get_dialogue_count_by_district_id(district_id)
    context['structure'] = q.get_district_structure_string_by_id(district_id)
    return render(request, 'dialogues/ajax_district_summary.html', context)


def ajax_get_total_count(request):
    context = {}
    context['total_count'] = q.get_total_count()
    return render(request, 'dialogues/ajax_total_count.html', context)

def ajax_get_districts_in_chapter(request, parent_id):
    context = {}
    context['options'] = q.get_districts_in_chapter(parent_id)

    return render(request, 'dialogues/ajax_select_options.html', context)

def ajax_get_chapters_in_area(request, parent_id):
    context = {}
    context['options'] = q.get_chapters_in_area(parent_id)

    return render(request, 'dialogues/ajax_select_options.html', context)

def ajax_get_areas_in_ga(request, parent_id):
    context = {}
    context['options'] = q.get_areas_in_ga(parent_id)

    return render(request, 'dialogues/ajax_select_options.html', context)


@csrf_exempt
def ajax_submit_new_home_visit(request):
    context = {}
    count = 0
    if request.method == 'POST':
        try:
            dist = q.get_district_by_id(request.POST.get('district_id'))
            friends = request.POST.get('visited_name','')
            friends = friends.split(',')
            for friend in friends:
                dlg = HomeVisit(visitor_name=request.POST.get('visitor_name',''),
                    visited_name=friend,
                    visitor_email=request.POST.get('visitor_email',''),
                    district=dist, visit_date = datetime.date.today())
                
                dlg.save()
                count += 1
            if count > 1:
                context['submit_msg']='Congratulations! %d Home visits have been submitted'%(count)
            else:
                context['submit_msg']='Congratulations! Your Home visits has been submitted'
            
        except:
            context['submit_msg'] ='Invalid data: visitor_name: %s, visited %s, district_id: %d!'%(member_name,
                visited_name, district_id)

    return render(request, 'dialogues/ajax_submit_new_home_visit_response.html', context)



@csrf_exempt
def ajax_submit_new_dialogue(request):
    context = {}
    count = 0
    if request.method == 'POST':
        try:
            dist = q.get_district_by_id(request.POST.get('district_id'))
            friends = request.POST.get('friend_name','')
            friends = friends.split(',')
            for friend in friends:
                dlg = Dialogue(member_name=request.POST.get('member_name',''),
                    friend_name=friend,
                    member_email=request.POST.get('member_email',''),
                    district=dist, dialogue_date = datetime.date.today())
                
                dlg.save()
                count += 1

            if count > 1:
                context['submit_msg']='Congratulations! %d Dialogues have been submitted'%(count)
            else:
                context['submit_msg']='Congratulations! Your dialogue has been submitted'
        except:
            context['submit_msg'] ='Invalid data: member_name: %s, friend_name: %s, district_id: %d!'%(member_name,
                friend_name, district_id)

    return render(request, 'dialogues/ajax_submit_new_dialogue_response.html', context)

def export_dist_sheet_dialogue_list_xls(request, dist_wise_list):
    import xlwt
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=dialogue_list.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    for dist_data in dist_wise_list:
        ws = wb.add_sheet(dist_data['district_name'])
    
        row_num = 0
        columns = [
            (u"Member Name", 8000),
            (u"Member Email", 8000),
            (u"Friend Name", 8000),
            (u"GA", 6000),
            (u"Area", 6000),
            (u"Chapter", 6000),
            (u"District", 6000),
            (u"Date", 6000),
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in xrange(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        for d in dist_data['dialogues']:
            row_num += 1
            row = [
                d.member_name,
                d.member_email,
                d.friend_name,
                d.district.parent.parent.parent.name,
                d.district.parent.parent.name,
                d.district.parent.name,
                d.district.name,
                str(d.dialogue_date)
            ]
            for col_num in xrange(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
                
    wb.save(response)
    return response


def export_dialogue_list_xls(request, dialogue_list):
    import xlwt
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=dialogue_list.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("All dialogues")
    
    row_num = 0
    
    columns = [
        (u"Member Name", 8000),
        (u"Member Email", 8000),
        (u"Friend Name", 8000),
        (u"GA", 6000),
        (u"Area", 6000),
        (u"Chapter", 6000),
        (u"District", 6000),
        (u"Date", 6000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    for d in dialogue_list:
        row_num += 1
        row = [
            d.member_name,
            d.member_email,
            d.friend_name,
            d.district.parent.parent.parent.name,
            d.district.parent.parent.name,
            d.district.parent.name,
            d.district.name,
            str(d.dialogue_date)
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response


def export_entire_dialogue_list_xls(request):

    all_dialogues = q.get_all_dialogues()
    return export_dialogue_list_xls(request, all_dialogues)
 
def export_chapter_dialogue_list_date_range_xls(request):
    
    chapter_id = int(request.GET.get('chapter_id',''))
    start_date = request.GET.get('start_date','01/01/2016 0:01 AM')
    start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')

    end_date = request.GET.get('end_date','12/1/2016 8:08 PM')
    end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
    dist_wise_list = q.get_chapter_dialogues_in_date_range(start_date, end_date, chapter_id) 

    return export_dist_sheet_dialogue_list_xls(request, dist_wise_list)

def export_dialogue_list_date_range_xls(request):
    
    start_date = request.GET.get('start_date','01/11/2015 8:01 PM')
    start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')

    end_date = request.GET.get('end_date','01/11/2015 8:08 PM')
    end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
    dialogues = q.get_dialogues_in_date_range(start_date, end_date) 

    return export_dialogue_list_xls(request, dialogues)

