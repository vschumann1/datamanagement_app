from django.contrib import admin
from .models import weichen_ISK_2022
from .models import stuetzauwerke_ISK_2022
from .models import schallschutzwaende_ISK_2022
from .models import GSL_ISK_2022
from .models import ETCS_2022
from .models import traffic_2022
from .models import hlk_zeitraum_2022
from .models import bruecken_ISK_2022
from .models import bahnuebergaenge_ISK_2022
from .models import tunnel_ISK_2022
from .models import SML_ISK_2022
from .models import GSL_grouped_ISK_2022


# Register models here.
admin.site.register(weichen_ISK_2022)
admin.site.register(stuetzauwerke_ISK_2022)
admin.site.register(schallschutzwaende_ISK_2022)
admin.site.register(GSL_ISK_2022)
admin.site.register(ETCS_2022)
admin.site.register(traffic_2022)
admin.site.register(hlk_zeitraum_2022)
admin.site.register(bruecken_ISK_2022)
admin.site.register(bahnuebergaenge_ISK_2022)
admin.site.register(tunnel_ISK_2022)
admin.site.register(SML_ISK_2022)
admin.site.register(GSL_grouped_ISK_2022)