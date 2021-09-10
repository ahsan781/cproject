# calendarapp/utils.py

from datetime import datetime, timedelta
from calendar import HTMLCalendar, month
from .models import ShiftDetail
from roster.helper import get_current_user
from datetime import datetime, timedelta, date

def cur_week():
    now = date.today() # - timedelta(days=1) # - timedelta(days=1) is only testing purpose
    mon = now - timedelta(days = now.weekday())
    cur_week = {}
    for i in range(0, 7):
        day = mon+timedelta(days=i)
        cur_week[day.strftime("%a")] = day
    return cur_week

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(date__day=day ,date__month=self.month)
		# print("-------",events_per_day)
		d = ''
		
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'
		
		if day != 0:
			return f"<td style='font-size:12px; width: 14.2%'><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		# print("current month = ",self.month)
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		weak = cur_week()
		shifts = ShiftDetail.objects.all()
		# shifts = ShiftDetail.objects.filter(date__range=[weak['Mon'], weak['Sun']])

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="table table-bordered">\n'
		cal += f'<center>{self.formatmonthname(self.year, self.month, withyear=withyear)}</center>\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, shifts)}\n'
		cal += f'</table>\n'
		return cal
