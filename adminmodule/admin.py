from django.contrib import admin
from .models import Admins,Course,Notes,Assignment,Batch,Video,Batch_videos#,usercourse

admin.site.register(Admins)
admin.site.register(Course)
admin.site.register(Notes)
admin.site.register(Assignment)
admin.site.register(Video)
admin.site.register(Batch)
admin.site.register(Batch_videos)
# admin.site.register(usercourse)