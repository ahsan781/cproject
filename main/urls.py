from main.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main import views



urlpatterns = [
    path('',index,name="index"),
    path('new',new,name="new"),
    path('users',AdminUesr,name="users"),
    path('login',Login,name="login"),
    path('logout',logout_view,name="logout"),
    path('userdashboard',userdashboard,name="userdashboard"),
    path('afterlogin',afterlogin_view,name="afterlogin"),
    path('adduser',Adduser,name="adduser"),
    path('multipleshift',AddMultipleShift,name="multipleshift"),
    path('shift',CalView,name="shift"),
    path('listview',views.listview,name="listview"),
    path('edit/<int:id>/',views.shiftupdate,name="edit"),
    path('edit1/<int:id>/',views.shiftupdate1,name="edit1"),
    path('delete/<int:id>/',views.shiftdelete,name="delete"),
    path('delete1/<int:id>/',views.shiftdelete1,name="delete1"),
    path('deletecalendar',views.deletecalendar,name="deletecalendar"),
    path('deleteweekcalendar',views.deleteweekcalendar,name="deleteweekcalendar"),
    path('deletedaycalendar',views.deletedaycalendar,name="deletedaycalendar"),
    #calender urls
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    

    path('shiftscheduler/', Shiftscheduler, name='shiftscheduler'),
    path('week/', Week, name='week'),
    path('weekremove/<int:id>/', deleteweek, name='weekremove'),
    path('week_as_csv/', export_shifts_as_csv, name='week_as_csv'),
    path('week_as_html/', export_shifts_as_html, name='week_as_html'),
    path('duplicate/<int:id>/', duplicateTask, name='duplicate'),
    path('multiduplicate/', multiduplicateTask, name='multiduplicate'),
    path('update_week/',updateWeek, name='update_week'),
    # path('update_week1/',updateWeek1, name='update_week1'),
    
   
  

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
