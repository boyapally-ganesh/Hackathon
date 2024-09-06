from django.contrib import admin
from .models import HackathonModels,SubmissionModel,RegistrationModel
# Register your models here.
admin.site.register(HackathonModels)
admin.site.register(SubmissionModel)
admin.site.register(RegistrationModel)