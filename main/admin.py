from django.contrib import admin
from.models import User,ShiftDetail,VendorProfile,AddUser,MemberProfile,MultiduplicateTask,Template

# Register your models here.

admin.site.register(User)
admin.site.register(ShiftDetail)
admin.site.register(VendorProfile)
admin.site.register(AddUser)
admin.site.register(MemberProfile)
admin.site.register(MultiduplicateTask)
admin.site.register(Template)