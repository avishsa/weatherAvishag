from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.db.models import Max,Min,Avg
from .models import Forecast,Forecastsum
from .insertions import insert_sumData

def get_count():
    return {'num forecasts':Forecast.objects.count()}
def get_data(lon, lat):
    res = list(Forecast.objects.filter(lon=lon,lat=lat).values("forecastTime", "Temperature","Precipitation"))
    if (len(res) ==0):
        return {'msg':'not found location'}
    return res    

def get_sum(lon,lat):
    def get_json(tMax,tMin,tAvg,pMax,pMin,pAvg):
        return {
            'max':{
                "Temperature":tMax,
                "Precipitation":pMax
            },
            'min':{
                "Temperature":tMin,
                "Precipitation":pMin
            },
            'avg' :{
                "Temperature":tAvg,
                "Precipitation":pAvg
            }
        }
    fc_qs = Forecastsum.objects.get(lon=lon,lat=lat)
    if(fc_qs == None):
        fcs_qs = Forecast.objects.filter(lon=lon,lat=lat)
        if(len(list(fcs_qs)) ==0):
            return {'msg':'not found location'}
        temp_max = fcs_qs.aggregate(Max('Temperature'))["Temperature__max"]
        temp_min = fcs_qs.aggregate(Min('Temperature'))["Temperature__min"]
        temp_avg = fcs_qs.aggregate(Avg('Temperature'))["Temperature__avg"]
        preci_max = fcs_qs.aggregate(Max('Precipitation'))["Precipitation__max"]
        preci_min = fcs_qs.aggregate(Min('Precipitation'))["Precipitation__min"]
        preci_avg = fcs_qs.aggregate(Avg('Precipitation'))["Precipitation__avg"]
        insert_sumData(lon,lat,
        temp_max,
        temp_min,
        temp_avg,
        preci_max,
        preci_min,
        preci_avg)
        return get_json(temp_max,temp_min,temp_avg,preci_max,preci_min,preci_avg)
    return get_json(fc_qs.temp_max, fc_qs.temp_min,fc_qs.temp_avg,
    fc_qs.Prec_max,fc_qs.Prec_min,fc_qs.Prec_avg)
    
