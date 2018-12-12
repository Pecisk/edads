from django.conf.urls import url
from django.urls import path

from .views import StarSystems, Stations, EDADSWebApp, StationSingle, StarSystemSingle, AdvertisementSingle, \
    LocationSearch, Login, Logout, RegisterUser, AdsSearch, AddAd, CommanderSetStation, CommanderAdResponse, \
    CommanderComms, CommanderAdResponseReply, AdClose, AdHide

urlpatterns = [
    path('', EDADSWebApp.as_view(), name='main'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('api/location_search/', LocationSearch.as_view(), name='location_search'),
    path('api/systems/', StarSystems.as_view(), name='systems'),
    path('api/system/<int:system_id>/', StarSystemSingle.as_view(), name='system'),
    path('api/stations/', Stations.as_view(), name='stations'),
    path('api/station/<int:station_id>/', StationSingle.as_view(), name='station'),
    path('api/advertisement/<int:ad_id>/', AdvertisementSingle.as_view(), name='ad'),
    path('api/advertisement/search/', AdsSearch.as_view(), name='ads_search'),
    path('api/advertisement/add/', AddAd.as_view(), name='add_ad'),
    path('api/commander/set_station/', CommanderSetStation.as_view(), name='set_station'),
    path('api/advertisement/<int:ad_id>/respond/', CommanderAdResponse.as_view(), name='respond_to_ad'),
    path('api/advertisement/<int:ad_id>/close/', AdClose.as_view(), name='close_ad'),
    path('api/advertisement/<int:ad_id>/hide/', AdHide.as_view(), name='hide_ad'),
    path('api/advertisement/response/<int:ad_response_id>/reply/',
         CommanderAdResponseReply.as_view(), name='reply_to_ad_response'),
    path('api/comms/', CommanderComms.as_view(), name='comms'),
]
