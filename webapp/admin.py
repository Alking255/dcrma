import csv
from django.http import HttpResponse
from django.contrib import admin
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Record
from django.utils.formats import date_format

class RecordAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country', 'formatted_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country')
    date_hierarchy = 'creation_date'
    list_filter = ('creation_date', 'city', 'province', 'country')
    actions = ['export_as_csv']  

    def formatted_date(self, obj):
        return date_format(obj.creation_date, format='SHORT_DATE_FORMAT', use_l10n=True)
    formatted_date.short_description = 'Creation Date'
    formatted_date.admin_order_field = 'creation_date'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        date_formats = ['%b. %d, %Y', '%Y-%m-%d', '%d/%m/%Y', '%Y']
        month_year_formats = ['%B %Y', '%b %Y', '%Y-%m']

        for date_format in date_formats:
            try:
                date = make_aware(datetime.strptime(search_term, date_format))
                if date_format == '%Y':
                    queryset |= self.model.objects.filter(creation_date__year=date.year)
                else:
                    queryset |= self.model.objects.filter(creation_date=date.date())
                break
            except ValueError:
                continue

        for my_format in month_year_formats:
            try:
                date = datetime.strptime(search_term, my_format)
                queryset |= self.model.objects.filter(
                    creation_date__year=date.year,
                    creation_date__month=date.month
                )
                break
            except ValueError:
                continue

        return queryset, use_distinct

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=records.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "CSV"

admin.site.register(Record, RecordAdmin)
