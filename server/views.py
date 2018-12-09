from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
#from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from .models import StarSystem, Station, Advertisement, User, Commander, Tradeable, TradeableCategory, Activity,\
    AdResponse, Message
import json
from .error_codes import *
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class RegisterUser(View):
    def get(self, request):
        return render(request, 'register_user.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        password_again = request.POST['password_again']
        commander_name = request.POST['commander_name']
        if password != password_again:
            return render(request, 'register_user.html')

        user = User(username=username)
        user.set_password(password)
        user.save()

        commander = Commander(user=user, name=commander_name, station=Station.objects.get(id=31337))
        commander.save()

        login(request, user)

        request.session['commander_id'] = commander.id
        request.session['commander_name'] = commander.name

        return redirect('main')

class Logout(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('user is {user}'.format(user=user))
        if user is not None:
            login(request, user)
            commander = user.commanders.all()[0]
            request.session['commander_id'] = commander.id
            request.session['commander_name'] = commander.name
            return redirect('main')
        else:
            return render(request, 'login.html')


class EDADSWebApp(View):
    def get(self, request):
        if request.user.is_authenticated:
            # Commander id and name - for not it is first available
            # TODO field in User module which stores actual commander for proper persistance
            commander = request.user.commanders.all()[0]

            if 'commander_id' in request.session:
                commander_id = request.session['commander_id']
                commander_name = request.session['commander_name']
            else:
                commander_id = commander.id
                commander_name = commander.name
            # Type of ad - TODO how to make it universal without having multiple def places - make it in settings file
            ad_types = [
                ('AD_TYPE_BARTER_TRADE', 'Exchange and trade of goods/materials'),
                ('AD_TYPE_SEEK_PROTECTION', 'Seeking protection'),
                ('AD_TYPE_OFFER_PROTECTION', 'Offering protection'),
                ('AD_TYPE_PLAYER_BOUNTY', 'Player bounty'),
            ]
            ad_combat_rank = [
                ('AD_COMBAT_RANK_HARMLESS', 'Harmless'),
                ('AD_COMBAT_RANK_MOSTLY_HARMLESS', 'Mostly Harmless'),
                ('AD_COMBAT_RANK_NOVICE', 'Novice'),
                ('AD_COMBAT_RANK_COMPETENT', 'Competent'),
                ('AD_COMBAT_RANK_EXPERT', 'Expert'),
                ('AD_COMBAT_RANK_MASTER', 'Master'),
                ('AD_COMBAT_RANK_DANGEROUS', 'Dangerous'),
                ('AD_COMBAT_RANK_DEADLY', 'Deadly'),
                ('AD_COMBAT_RANK_ELITE', 'Elite'),
            ]

            activities = Activity.objects.all()
            tradeables = TradeableCategory.objects.all()

            return render(request, 'base.html', {'commander_id': commander_id,
                                                 'commander_name': commander_name,
                                                 'ad_types': ad_types,
                                                 'ad_combat_rank': ad_combat_rank,
                                                 'ad_activities': activities,
                                                 'tradeables': tradeables,
                                                 'commander_station': commander.station.name,
                                                 'commander_station_id': commander.station.id,
                                                 })
        return redirect('login')


class StarSystems(View):

    def get(self, request):
        systems = StarSystem.objects.all()
        return JsonResponse(
            dict(locations=[system.to_json() for system in systems])
        )


class Stations(View):

    def get(self, request):
        stations = Station.objects.all()
        return JsonResponse(
            [station.to_json() for station in stations], safe=False
        )


class StationSingle(View):

    def get(self, request, station_id):
        stations = Station.objects.filter(id=station_id)
        return JsonResponse(
            dict(locations=[station.to_json() for station in stations])
        )


class StarSystemSingle(View):

    def get(self, request, system_id):
        systems = StarSystem.objects.filter(id=system_id)
        return JsonResponse(
            dict(locations=[system.to_json() for system in systems])
        )


class AdvertisementSingle(View):

    def get(self, request, ad_id):
        ad = Advertisement.objects.filter(id=ad_id).first()
        return JsonResponse(ad.to_json())


class AdsSearch(View):

    def post(self, request):
        search_post = json.loads(request.body)
        search_method = search_post['search_method']

        if search_method == 'by_station':
            station_id = search_post['search_station_id']
            ads = Advertisement.objects.filter(station__id=station_id)
            return JsonResponse(
                [ad.to_json() for ad in ads], safe=False
            )


class LocationSearch(View):

    def post(self, request):
        searchString = request.POST['search_location']
        stations = Station.objects.filter(name__contains=searchString)
        return JsonResponse([station.to_json_simple() for station in stations], safe=False)


class AddAd(View):

    def post(self, request):
        request_body = json.loads(request.body)
        print(request_body)

        ad_type = request_body['ad_ad_type']

        if 'ad_activities' in request_body:
            ad_activities = request_body['ad_activities']
        else:
            ad_activities = None

        if 'ad_combat_rank' in request_body:
            ad_combat_rank = request_body['ad_combat_rank']
        else:
            ad_combat_rank = None

        if 'ad_crew_member' in request_body:
            ad_crew_member = True
        else:
            ad_crew_member = False

        if 'ad_wing_member' in request_body:
            ad_wing_member = True
        else:
            ad_wing_member = False

        if 'ad_legal' in request_body:
            ad_legal = True
        else:
            ad_legal = False

        if 'ad_payment_type' in request_body:
            ad_payment_type = Tradeable.objects.get(id=request_body['ad_payment_type'])
        else:
            ad_payment_type = None

        if 'ad_payment_pro_bono' in request_body:
            ad_payment_type = None
            ad_payment_pro_bono = True
        else:
            ad_payment_pro_bono = False

        if 'ad_payment_units' in request_body:
            ad_payment_units = request_body['ad_payment_type_units']
        else:
            ad_payment_units = 0

        if 'ad_tradeable_from' in request_body:
            ad_tradeable_from = Tradeable.objects.get(id=request_body['ad_tradeable_from'])
        else:
            ad_tradeable_from = None

        if 'ad_tradeable_to' in request_body:
            ad_tradeable_to = Tradeable.objects.get(id=request_body['ad_tradeable_to'])
        else:
            ad_tradeable_to = None

        commander = Commander.objects.get(id=request.session['commander_id'])
        ad = Advertisement(type=ad_type, payment_type=ad_payment_type, payment_units=ad_payment_units,
                           commander=commander, station=commander.station,
                           combat_rank=ad_combat_rank, crew_member=ad_crew_member,
                           wing_member=ad_wing_member, legal=ad_legal,
                           payment_pro_bono=ad_payment_pro_bono,
                           tradeable_from=ad_tradeable_from,
                           tradeable_to=ad_tradeable_to
                           )
        ad.save()

        if ad_activities:
            for ad_activity in ad_activities:
                ad.activities_involved.add(ad_activity)

        ad.save()

        return JsonResponse(
            dict(
                success=True,
                ad_id=ad.id,

            )
        )


class CommanderSetStation(View):

    def post(self, request):

        station_id = request.POST['station_id']
        commander = Commander.objects.get(id=request.session['commander_id'])
        commander.station = Station.objects.get(id=station_id)
        commander.save()

        return JsonResponse(commander.station.to_json_simple())


class CommanderAdResponse(View):

    def post(self, request, ad_id):

        # Gather data from form
        request_body = json.loads(request.body)
        note = request_body.get('note')
        if not note:
            return JsonResponse(dict(error=NOT_ALL_REQUIRED_FIELDS), status=400)

        commander = Commander.objects.get(pk=request.session['commander_id'])

        if not commander:
            return JsonResponse(dict(error=NO_COMMANDER_SET), status=400)

        try:
            ad = Advertisement.objects.get(pk=int(ad_id))

            if ad.closed:
                # Ad is closed, no reply is possible
                return JsonResponse(dict(error=AD_CLOSED), status=400)

            if ad.commander == commander:
                return JsonResponse(dict(error=COMMANDER_CANT_RESPOND_TO_OWN_AD), status=400)

            if not AdResponse.objects.filter(commander=commander, ad=ad).exists():

                ad_response = AdResponse.objects.create(
                    commander=commander, ad=ad
                )

                message = Message.create(
                    note=note,
                    commander_from=commander,
                    commander_to=ad.commander,
                    station=None,
                    datetime=None,
                    ad_response=ad_response
                )

                return JsonResponse(dict(status=SUCCESS))

            else:

                return JsonResponse(dict(error=COMMANDER_ALREADY_RESPONDED), status=400)

        except ObjectDoesNotExist:

            return JsonResponse(dict(error=INVALID_AD), status=400)


class CommanderAdResponseReply(View):

    def post(self, request, ad_response_id):

        request_body = json.loads(request.body)
        note = request_body.get('note')
        if not note:
            return JsonResponse(dict(error=NOT_ALL_REQUIRED_FIELDS), status=400)

        commander = Commander.objects.get(pk=request.session['commander_id'])

        if not commander:
            return JsonResponse(dict(error=NO_COMMANDER_SET), status=400)

        try:
            ad_response = AdResponse.objects.get(pk=ad_response_id)

            # validity check

            if ad_response.ad.closed:
                # Ad is closed, no reply is possible
                return JsonResponse(dict(error=AD_CLOSED), status=400)

            if commander is not ad_response.commander and commander is not ad_response.ad.commander:
                return JsonResponse(dict(error=COMMANDER_NOT_PART_OF_RESPONSE), status=400)

            if ad_response.commander == commander:
                commander_to = ad_response.ad.commander
            else:
                commander_to = ad_response.commander

            message = Message(
                note=note,
                commander_from=commander,
                commander_to=commander_to,
                meetup_station=None,
                meetup_datetime=None,
                ad_response=ad_response
            )
            message.save()

            return JsonResponse(dict())

        except ObjectDoesNotExist:

            return JsonResponse(dict(error=INVALID_AD_RESPONSE), status=400)

class CommanderComms(View):

    def get(self, request):
        ads = Advertisement.objects.filter(commander=Commander.objects.get(
            pk=request.session['commander_id']), ad_responses_advert__gt=0
        )
        return JsonResponse([ad.to_json_with_responses() for ad in ads], safe=False)
