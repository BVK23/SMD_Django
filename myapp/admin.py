from django.contrib import admin

# Register your models here.
from .models import Acquisitiontime
admin.site.register(Acquisitiontime)

from .models import Bandwidth
admin.site.register(Bandwidth)

from .models import Endpoint
admin.site.register(Endpoint)

from .models import Patient
admin.site.register(Patient)

from .models import Patienttreatment
admin.site.register(Patienttreatment)

from .models import Session
admin.site.register(Session)

from .models import Treatment
admin.site.register(Treatment)

from .models import Treatmentbandwidth
admin.site.register(Treatmentbandwidth)
