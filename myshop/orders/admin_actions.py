import csv
import datetime
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import HttpResponse

def export_to_csv(modeladmin, request: WSGIRequest, queryset: QuerySet):
    print(f'Tipo de queryset -> {type(queryset)}')
    
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [fields for fields in opts.get_fields() if not \
              fields.many_to_many and not fields.one_to_many]
    
    writer.writerow([field.verbose_name for field in fields])
    
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
        
    return response