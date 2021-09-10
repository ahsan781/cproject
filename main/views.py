from django.forms.widgets import Textarea
from django.shortcuts import render,redirect
from .utils import cur_week
from django.core.mail import EmailMessage


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

from django.template.loader import get_template
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm
from.models import *
from django.contrib import messages
#  calender url
from datetime import datetime, date, timedelta, time
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.utils.safestring import mark_safe

import calendar, csv
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic.edit import FormView
from django.db.models import Count


from .models import *
from main.utils import Calendar
from .forms import EventForm, AddMemberForm,ProfileForm,AddUserForm,LoginForm
from .forms2 import EventForm1
from django.forms import formset_factory
from django.views.generic import ListView, TemplateView # Import TemplateView
# from .forms import BookFormset
import json
 
def new(request):
    return render(request,"cal.html")

#login view
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email = email, password = password)

        
        if user:
           form = login(request, user)
           return redirect('index')

                
        else:
            return redirect('login')
  
    form = AuthenticationForm()
    return render(request, 'account/login.html', {'form':form, 'title':'log in'})

#logout view
def logout_view(request):
    logout(request)
    return redirect('login')


#home page view
@login_required(login_url='login')
def index(request):
    return render(request,"index.html")


@login_required(login_url='/login')
def owner(user):
    return user.groups.filter(name='owner').exists()

@login_required(login_url='/login/')
def is_normaluser(user):
    return user.groups.filter(name='is_normaluser').exists()


# @login_required(login_url='/login/')

def AdminUesr(request):
    user = dict()
    normalusers= User.objects.all()
    adminusers= User.objects.filter(groups__name='owner')
    if request.method == 'POST':
        first_name=request.POST.getlist('first_name')
        last_name=request.POST.getlist('last_name')
        email=request.POST.getlist('email')
        mobile=request.POST.getlist('mobile')
        for i in range(len(email)):
            user[str(email[i])]=[first_name[i],last_name[i],email[i],mobile[i]]
        add_user_list = []
        for i in range(len(user.keys())):
            add_user_list.append(AddUser(first_name= user[email[i]][0],
            last_name=user[email[i]][1],email=user[email[i]][2],mobile=user[email[i]][3]))
        AddUser.objects.bulk_create(add_user_list)
        return redirect("users")

    adduser = AddUser.objects.all()
    form = AddUserForm()
    return render(request,"users1.html",{"adminusers":adminusers,"form":form,"adduser":adduser})



def AddMultipleShift(request):
    user1 = dict()

    if request.method == 'POST':
        date=request.POST.getlist('date')
        start_time=request.POST.getlist('start_time')
        end_time=request.POST.getlist('end_time')
        title=request.POST.getlist('title')
        username=request.POST.getlist('username')
        location=request.POST.getlist('location')
        note=request.POST.getlist('note')
        text=request.POST.getlist('text')

        # print(start_time,end_time,date,title,username,location)

        for j in range(len(title)):
            user1[str(title[j])]=[date[j],start_time[j],end_time[j],title[j],location[j],username[j],note[j],text[j]]
        add_user_list = []
        for k in range(len(user1.keys())):
            add_user_list.append(ShiftDetail(date= user1[title[k]][0],
            start_time=user1[title[k]][1],end_time=user1[title[k]][2],title=user1[title[k]][3],location=user1[title[k]][4],
            username=user1[title[k]][5],note=user1[title[k]][6],text=user1[title[k]][7]
            ))

        ShiftDetail.objects.bulk_create(add_user_list)
        # print("0-----",emailuser)
        return redirect("shift")

    addshift = ShiftDetail.objects.all()
    member = MemberProfile.objects.all()
    
    form = EventForm()
    return render(request,"multipleshift.html",{"form":form,"addshift":addshift,"member":member})





@login_required(login_url='/login/')
def afterlogin_view(request):
    if owner(request.user):
        return redirect('users')
    elif is_normaluser(request.user):
        return redirect('userdashboard')
 
    else:
        return redirect('login')


#userdashboard view
@login_required(login_url='/login/')
def userdashboard(request):
    return render(request,"userdashboard.html")



@login_required(login_url='/login/')
def Adduser(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = AddUserForm()
    return render(request,'adduser.html',{'form': form})    

def send_email(subject, temp, email_ctx, to_list):
    
    heading = subject or "Your heading"

    messageContent = get_template(temp).render(email_ctx) #sending value on HTML page through context
    msg = EmailMessage(heading, messageContent, settings.EMAIL_HOST_USER, to_list)
    msg.content_subtype = 'html'
    msg.send()
    return True

@login_required()
def Week(request):
    form = EventForm(request.POST , request.FILES or None)
    if request.POST and form.is_valid():
        shift_title = form.cleaned_data['title']
        date = form.cleaned_data['date']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        user = form.cleaned_data['user']
        note = form.cleaned_data['note']
        location = form.cleaned_data['location']
        job = form.cleaned_data['job']
        tz1 = form.cleaned_data['tz1']
        email= User.objects.get(username=user)        
        ShiftDetail.objects.get_or_create(
            user=user,
            title=shift_title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            note=note,
            date=date,
            job=job,
            tz1=tz1
            

        )
        send_email("This is roster", "basic_email.html", {}, [email.email])
        return HttpResponseRedirect(request.path_info)

    weak = cur_week()

    shifts = ShiftDetail.objects.filter(date__range=[weak['Mon'], weak['Sun']]).order_by('user')
    shift_detail= ShiftDetail.objects.all()
    users = set(i.user.username for i in shifts)
    jobs = set(i.job for i in shifts)
    context = {"cur_week":cur_week,"shifts":shifts,'users':users,'jobs':jobs, "form":form,"shift_detail":shift_detail}
    return render(request, "calender/calender1.html", context)


def listview(request):
    shifts= ShiftDetail.objects.all()
    if request.method == "POST":
        startdate = request.POST['start_time']
        enddate = request.POST['end_time']
        user = request.POST['user']
        if (startdate and enddate is not None):
         shifts= ShiftDetail.objects.filter(date__range=[startdate, enddate])
         return render(request,"listview.html",{"shifts":shifts})
        if (user is not None):
         shifts= ShiftDetail.objects.filter(username__contains= user)
         return render(request,"listview.html",{"shifts":shifts})
        if (user is not None and startdate and enddate is not None):
         shifts= ShiftDetail.objects.filter(username__contains= user,date__range=[startdate, enddate])
         return render(request,"listview.html",{"shifts":shifts})
    return render(request,"listview.html",{"shifts":shifts})

#shift update view
@login_required(login_url='/login')
def updateWeek(request):
    if request.method == 'POST':
        shift_id = request.POST.get('id')
        shift_date = request.POST.get('date')
        username = request.POST.get('user')
        user_id = request.POST.get('user_id')
        st_time = request.POST.get('st_time')
        print(st_time)
        print('//////',shift_date)
        print('//////',user_id)
        if(ShiftDetail.objects.filter(id=shift_id)):
            obj = ShiftDetail.objects.get(id=shift_id)
            if user_id:
                obj.username = user_id
            if username:
                obj.user = User.objects.get(username=username)
            if shift_date:
                obj.date = shift_date # datetime.strptime(shift_date, '%d-%m-%Y').date()
            if st_time:
                obj.start_time = datetime.strptime(st_time, '%I %p').time() #st_time
            obj.save()
        elif(Template.objects.filter(id=shift_id)):
            obj = Template.objects.get(id=shift_id)
            start = obj.start_time1  
            end = obj.end_time1
            tz1 = obj.tz11
            text = obj.text1
            location = obj.location1
            note = obj.note
            data = ShiftDetail(date=shift_date ,username=user_id,title=obj , start_time=start , end_time=end , tz1=tz1,text=text,location = location, note = note  )
            if st_time:
             obj.start_time1 = datetime.strptime(st_time, '%I %p').time() 
             print(obj.start_time1)
            #  start = obj.start_time1
            #  data = ShiftDetail(date=shift_date ,username=user_id,title=obj , start_time=start , end_time=end )
            data.save()

        # obj = Template.objects.get(id=shift_id)

        # print(obj)
        # if user_id:
        #     obj.username = user_id
        # if username:
        #     obj.user = User.objects.get(username=username)
        # if shift_date:
        #     obj.date = shift_date # datetime.strptime(shift_date, '%d-%m-%Y').date()
        # if st_time:
        #     obj.start_time = datetime.strptime(st_time, '%I %p').time() #st_time
        # obj.save()
        return JsonResponse({"result":"Done"})
    else:
        return JsonResponse({"result":"Method Not allowed"})
# def updateWeek1(request):
#     if request.method == 'POST':
#         shift_id = request.POST.get('id')
#         shift_date = request.POST.get('date')
#         username = request.POST.get('user')
#         user_id = request.POST.get('user_id')
#         st_time = request.POST.get('st_time')
#         print('//////',shift_date)
#         print('//////',username)
#         obj = Template.objects.get(id=shift_id)
#         print(obj)
#         if user_id:
#             obj.username = user_id
#         if username:
#             obj.user = User.objects.get(username=username)
#         if shift_date:
#             obj.date = shift_date # datetime.strptime(shift_date, '%d-%m-%Y').date()
#         if st_time:
#             obj.start_time = datetime.strptime(st_time, '%I %p').time() #st_time
#         obj.save()
#         return JsonResponse({"result":"Done"})
#     else:
#         return JsonResponse({"result":"Method Not allowed"})


#shift delete view
@login_required(login_url='/login/')
def deleteweek(request,id):
    # print("----1----")
    task=ShiftDetail.objects.filter(id=id)
    task1=Template.objects.filter(id=id)
    # print("--task---",task)
    task.delete()
    task1.delete()

    return redirect('shift')


#shift duplicate view
@login_required(login_url='/login/')
def duplicateTask(request, id):
    task = ShiftDetail.objects.get(id=id)

    ShiftDetail.objects.create(
    user = task.user,

    title = task.title,
    start_time = task.start_time,
    end_time = task.end_time,
    created_date = task.created_date,
    location = task.location,
    note = task.note,
    job = task.job,
    tz1 = task.tz1, 
    date= task.date,
    username = task.username

        )
    return redirect('shift')

# shift multiduplicate view
@login_required(login_url='/login/')
def multiduplicateTask(request):
    # print("----------------")
    if request.method == "POST":
        number = request.POST.get('numbers')
        id = request.POST.get('id')
        # print("--number---",number)
        val = MultiduplicateTask(numbers=number)
        val.save()
        task = ShiftDetail.objects.get(id=id)
        num= MultiduplicateTask.objects.last()
        for multi in range(0,int(num.numbers)):
            ShiftDetail.objects.create(
            user = task.user,
            title = task.title,
            start_time = task.start_time,
            end_time = task.end_time,
            created_date = task.created_date,
            location = task.location,
            note = task.note,
            job = task.job,
            tz1 = task.tz1, 
            date= task.date,
            username = task.username

                )


        return redirect('shift')    
    return render(request,"calendar.html")




@login_required(login_url='/login/')
def export_shifts_as_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="shifts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date','Start', 'End', 'Shift title', 'Job', 'User','Note','TEXT'])
    weak = cur_week()

    shifts = ShiftDetail.objects.filter(date__range=[weak['Mon'], weak['Sun']])
    for i in shifts:
        data = [i.date, i.start_time, i.end_time,
        i.title, i.job, i.user, i.note,i.text]
        writer.writerow(data)
    return response


# from here you export your queryset with head title as html file
@login_required(login_url='/login/')
def export_shifts_as_html(request):

    weak = cur_week()
    shifts = ShiftDetail.objects.filter(date__range=[weak['Mon'], weak['Sun']])
    context = {"head_title": "This is Test table", "shifts":shifts}

    template = get_template("calender/shifts_table.html")
    html = template.render(context)
    
    response = HttpResponse(html, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="shifts.html"'
    return response

# day
def get_day(day):
    
    if day:
        year, month,day = (int(x) for x in day.split('-'))
        return date(year, month, day)
    now = date.today()
    mon = now - timedelta(days = now.weekday())
    cday1 = 'day=' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    
    return now
def today_day():
    now = date.today()
    cday1 = 'day=' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    
    return cday1


def prev_day(day):
    now = day 
    mon = now - timedelta(days = 1)
    # prev_week = mon + timedelta(days = -7)
    # print("this next week",next_week)
    weak = 'day=' + str(mon.year) + '-' + str(mon.month) + '-' + str(mon.day)
    return weak

def next_day(day):
    now = day 
    mon = now + timedelta(days = 1)
    # next_week = mon + timedelta(days = 7)
    # print(next_week)
    weak = 'day=' + str(mon.year) + '-' + str(mon.month) + '-' + str(mon.day)
    return weak
def now_day(day):
    now = day 
    mon = now + timedelta(days = 1)
    next_week = mon + timedelta(days = 7)
    # print(next_week)
    weak = 'day=' + str(next_week.year) + '-' + str(next_week.month) + '-' + str(next_week.day)
    return now
def c_day(day):
    now = day 
    cday = 'day=' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    return cday
# week

def today_week():
    
    now = date.today()
    cweek1 = 'week=' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) 
    return cweek1
def today_month():
    
    now = date.today()
    cmonth1 = 'month=' + str(now.year) + '-' + str(now.month)
    return cmonth1

def get_week(req_week):
    
    if req_week:
        year, month,day = (int(x) for x in req_week.split('-'))
        return date(year, month, day)
    now = date.today()
    mon = now - timedelta(days = now.weekday())
    return mon

def prev_week(week):
    now = week 
    mon = now - timedelta(days = now.weekday())
    prev_week = mon + timedelta(days = -7)
    # print("this next week",next_week)
    weak = 'week=' + str(prev_week.year) + '-' + str(prev_week.month) + '-' + str(prev_week.day)
    return weak
def show_week(weak):
    now = weak
    mon = now - timedelta(days = now.weekday())
    cur_week = {}
    for i in range(0, 7):
        day = mon+timedelta(days=i)
        cur_week[day.strftime("%a")] = day
    
    return cur_week
def next_week(week):
    now = week 
    mon = now - timedelta(days = now.weekday())
    next_week = mon + timedelta(days = 7)
    # print(next_week)
    weak = 'week=' + str(next_week.year) + '-' + str(next_week.month) + '-' + str(next_week.day)
    return weak
def now_week(week):
    now = week 
    mon = now - timedelta(days = now.weekday())
    next_week = mon + timedelta(days = 7)
    # print(next_week)
    weak = 'week=' + str(next_week.year) + '-' + str(next_week.month) + '-' + str(next_week.day)
    return mon
def c_week(week):
    now = week 
    mon = now - timedelta(days = now.weekday())
    # print(next_week)
    weak = 'week=' + str(mon.year) + '-' + str(mon.month) + '-' + str(mon.day)
    return weak
def lastday_week(week):
    now = week 
    mon = now - timedelta(days = now.weekday())
    next_week = mon + timedelta(days = 6)
    print(',,,,,,,,',next_week)
    return next_week

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return date.today()

def prev_month(d):
    first = d.replace(day=1)
   
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
def lastday_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    lastdaymonth = next_month - timedelta(days=1)
    return lastdaymonth

def cur_month(d):
    # print(d)
    first = d.replace(day=1)
 
    return first
def c_month(d):
    # print(d)
    first = d.replace(day=1)
    prev_month = first - timedelta(days=0)
    # print(',,,,,,,,,',first)
    month =  'month=' + str(first.year) + '-' + str(first.month)
    return month
def CalView(request):
    if request.method == "POST" and 'date1' in request.POST :
        date =  request.POST['date1']
        st_time =  request.POST['stime1']
        end_time =  request.POST['etime1']
        tz1 =  request.POST['tz1']
        title =  request.POST['title1']
        location =  request.POST['location1']
        name =  request.POST['username1']
        file=request.FILES['file1']
        Textarea =  request.POST['textarea1']
        if 'action' in request.POST:
          print('jjjjj')
          template1 = Template( title1=title, date1 = date ,   start_time1= st_time , end_time1=end_time ,  tz11 =  tz1 ,username1 = name , location1=location, note=file , text1=Textarea)
          template1.save()
        else: 
          print('sssss') 
          template1 = ShiftDetail( title=title, date = date ,   start_time = st_time , end_time =end_time ,  tz1 =  tz1 ,username = name , location =location, note=file , text=Textarea)
          template1.save()
          return redirect("shift")
    form = EventForm()
    form1 = EventForm1()
    if request.method == "POST"  and 'date' in request.POST:
        date =  request.POST['date']
        st_time =  request.POST['st_time']
        end_time =  request.POST['end_time']
        tz1 =  request.POST['tz1']
        title =  request.POST['title']
        location =  request.POST['location']
        name =  request.POST['username']
        file=request.FILES['file']
        Textarea =  request.POST['textarea']
        template = Template( title1=title, date1 = date ,   start_time1= st_time , end_time1=end_time ,  tz11 =  tz1 ,username1 = name , location1=location, note=file , text1=Textarea)
        template.save()
        return redirect("shift")
    # d = get_date(request.GET.get('month', None))
    # days= get_date(request.GET.get('day', None))
    # cal = Calendar(d.year, d.month)
    # html_cal = cal.formatmonth(withyear=True)

    # member =MemberProfile.objects.all()
    # all_shift = ShiftDetail.objects.all()


    hours = [(i, time(i).strftime('%I %p')) for i in range(24)]
    all_shift= ShiftDetail.objects.all()
    all_template = Template.objects.all()
    users =   MemberProfile.objects.all()
    user1= AddUser.objects.all()
    # users = set((i.user.vender_profile, i.user.vender_profile.user.first_name) for i in all_shift)
    # print("------",users)
    user_sifts = all_shift.values('user').annotate(count=Count('title'))
    # print("--user_sifts----",user_sifts)
    jobs = set(i.job for i in all_shift)
    job_sifts = all_shift.values('job').annotate(count=Count('title'))
    # print(all_shift)
    context = {}
    month = get_date(request.GET.get('month', None))
    days= get_day(request.GET.get('day', None))
    week= get_week(request.GET.get('week', None))

    ds = request.GET.get('month', None)
    dayss= request.GET.get('day', None)
    week1s= request.GET.get('week', None)
    # print(cur_month(month))
    if(week1s != None):
        weak = show_week(week)
    else:  
        weak = cur_week()
    showm = "block"
    showw = "none"
    showd = "none"
    showmonth = "block"
    showweek = "none"
    showday = "none"
    cmonth = "block"
    cweek = "none"
    cday = "none"
    todaymonth = "block"
    todayweek = "none"
    todayday = "none"
    # print(now_day(days))
    # print(prev_week(week))
    if(ds != None):
        showm = "block"
        showw = "none"
        showd = "none"
        showmonth = "block"
        showweek = "none"
        showday = "none"
        cmonth = "block"
        cweek = "none"
        cday = "none"
        todaymonth = "block"
        todayweek = "none"
        todayday = "none"
    
    if(dayss != None):
        showm = "none"
        showw = "none"
        showd = "block"
        showmonth = "none"
        showweek = "none"
        showday = "block"
        cmonth = "none"
        cweek = "none"
        cday = "block"
        todaymonth = "none"
        todayweek = "none"
        todayday = "block"
    
    if(week1s != None):
        showm = "none"
        showw = "block"
        showd = "none"
        showmonth = "none"
        showweek = "block"
        showday = "none"
        cmonth = "none"
        cweek = "block"
        cday = "none"
        todaymonth = "none"
        todayweek = "block"
        todayday = "none"
     
    
    cal = Calendar(month.year, month.month)
    html_cal = cal.formatmonth(withyear=True)
    # print(prev_week())
    curent_month=cur_month(month)
    # print(month)
    lastdaymonth = lastday_month(month)
    # print('@@@@@@@@@@',lastdaymonth)
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = prev_month(month)
    context['c_month'] = c_month(month)
    context['cur_month'] = curent_month
    context['next_month'] = next_month(month)
    context['c_week'] = c_week(week)
    context['c_day'] = c_day(days)
    context['prev_week'] = prev_week(week)
    context['next_week'] = next_week(week)
    context['now_week'] = now_week(week)
    context['prev_day'] = prev_day(days)
    context['next_day'] = next_day(days)
    context['now_day'] = now_day(days)
    context['hours'] = hours
    context['showm'] = showm
    context['showw'] = showw
    context['showd'] = showd
    context['showmonth'] = showmonth
    context['showweek'] = showweek
    context['showday'] = showday
    context['all_shift'] = all_shift
    context['all_template'] = all_template
    context['users'] = users
    context['user1'] = user1
    context['jobs'] = jobs
    context['today_day'] = today_day()
    context['today_week'] = today_week()
    context['today_month'] = today_month()
    context['user_sifts'] = user_sifts
    context['job_sifts'] = job_sifts
    context['cur_week'] = weak
    context['form'] = form
    context['form1'] = form1
    context['cmonth'] = cmonth
    context['cweek'] = cweek
    context['cday'] = cday  
    context['todaymonth'] = todaymonth
    context['todayweek'] = todayweek
    context['todayday'] = todayday  
    context['multi'] = MultiduplicateTask.objects.last()
    # print(all_shift)
    return render(request,"calendar.html",context)        
    # return render(request,"calendar.html",{"form":form,"memberuser":member,"calendar":mark_safe(html_cal),"prev_month":prev_month,"next_month":next_month,"all_shift":all_shift})        




#main calendar view
class CalendarView(LoginRequiredMixin, generic.ListView, FormView):
    login_url = 'login'
    model = ShiftDetail
    form_class = EventForm
    template_name = 'cal.html'
    success_url = '/calendar/'
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        email= MemberProfile.objects.get(name=username)
        send_email("This is roster", "basic_email.html", {}, [email.email])
        return super().form_valid(form)
  
    def get_context_data(self, **kwargs):
        
        hours = [(i, time(i).strftime('%I %p')) for i in range(24)]
        all_shift= ShiftDetail.objects.all()
        # users = set((i.username, i.username) for i in all_shift)
        # print("------",users)
        user_sifts = all_shift.values('user').annotate(count=Count('title'))
        #print("--user_sifts----",user_sifts)
        jobs = set(i.job for i in all_shift)
        job_sifts = all_shift.values('job').annotate(count=Count('title'))
        weak = cur_week()
        all_shift.object_list = all_shift

        context = super().get_context_data(**kwargs)

        # print("---context---",context)
        
        d = get_date(self.request.GET.get('month', None))
        days= get_date(self.request.GET.get('day', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['hours'] = hours
        context['all_shift'] = all_shift
        # context['users'] = users
        context['jobs'] = jobs
        context['user_sifts'] = user_sifts
        context['job_sifts'] = job_sifts
        context['cur_week'] = weak
        context['multi'] = MultiduplicateTask.objects.last()
        context['memberuser'] = MemberProfile.objects.all()

        return context

@login_required(login_url='/login/')
def Shiftscheduler(request):
    return render(request,"calender/shiftscheduler.html")


@login_required
def shiftupdate(request, id=None, template_name='shift_edit_template.html'):
    if id:
        article = get_object_or_404(ShiftDetail, pk=id)
      
    else:
        article = ShiftDetail(user=username)

    form = EventForm(request.POST or None, instance=article)
    if request.POST :
        # print("post")
        print(form.data)
        # print(article)
        # print('///////',id)
        form.save()
        
        # Save was successful, so redirect to another page
        return redirect('shift')
    
    return render(request, template_name, {
        'form': form,
        'id' : article
    })
@login_required
def shiftupdate1(request, id=None, template_name='templateupdate.html'):
    if id:
        article1 = get_object_or_404(Template, pk=id)
            
    else:
        article1 = Template(user=username)
      
    form = EventForm1(request.POST or None, instance=article1)
    if request.POST  :
        form.save()
        # print(id)
        # print(article1)
        # form.save()
        
        # Save was successful, so redirect to another page
        return redirect('shift')
    
    return render(request, template_name, {
        'form': form,
        'id' : article1
    })
def shiftdelete(request, id):
   shift = ShiftDetail.objects.get(pk = id)
   shift1 = Template.objects.get(pk = id)
   shift1.delete()
   shift.delete()
   return redirect('shift')
def shiftdelete1(request, id):
   shift1 = Template.objects.get(pk = id)
   shift1.delete()
   return redirect('shift')
def deletecalendar(request):
   month = get_date(request.GET.get('month', None))
   curent_month=cur_month(month)
   lastdaymonth = lastday_month(month)
   shift = ShiftDetail.objects.filter(date__range=[curent_month,lastdaymonth])
   shift.delete()
   return redirect('shift')
def deleteweekcalendar(request):
   week= get_week(request.GET.get('week', None))
   curent_week=now_week(week)
   lastdayweek = lastday_week(week)
   shift = ShiftDetail.objects.filter(date__range=[curent_week,lastdayweek])
   shift.delete()
   return redirect('shift')
def deletedaycalendar(request):
   days= get_day(request.GET.get('day', None))
   curent_day=now_day(days)
   shift = ShiftDetail.objects.filter(curent_day)
   shift.delete()
   return redirect('shift')
