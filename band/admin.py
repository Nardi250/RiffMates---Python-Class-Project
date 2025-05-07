from django.contrib import admin
from band.models import Musician
from datetime import datetime, date

class DecadeListFilter(admin.SimpleListFilter):
    title = 'decade of birth'
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        result = []
        this_year = datetime.now().year
        for i in range(1900, this_year, 10):
            result.append((str(i), str(i) + '-' + str(i+9)))
        return result

    def queryset(self, request, queryset):
        start = self.value()
        if start is None:
            return queryset
        start = int(start)
        return queryset.filter(birth__gte=date(start, 1, 1), birth__lte=date(start  + 9, 12, 31))
        
@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name','birth','show_bands','show_weekday')
    search_fields = ('first_name__startswith',)
    list_filter = (DecadeListFilter,)

    def show_weekday(self, obj):
        return obj.birth.strftime('%A')
    
    show_weekday.short_description = 'Weekday of birth'

    def show_bands(self, obj):
        bands = obj.band_set.all()
        if len(bands) == 0:
            return format_html('<i>No bands</i>')
        plural = 's' if len(bands) > 1 else ''
        param = 'id__in='+ ','.join([str(band.id) for band in bands])
        url = reverse('admin:bands_band_changelist') + param
        return format_html('a href="{}">{} band{}</a>', url, len(bands), plural)
    
    
    show_bands.short_description = 'Bands'

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):

        
        
        
                          


# Register your models here.
