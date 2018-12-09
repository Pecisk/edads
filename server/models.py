from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100)
    surename = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Commander(models.Model):
    user = models.ForeignKey('User', related_name='commanders', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    station = models.ForeignKey('Station', on_delete=models.CASCADE, blank=True, null=True)

    def to_json_simple(self):
        return dict(
            id=self.id,
            name=self.name
        )

    def __str__(self):
        return self.name


class StarSystem(models.Model):
    name = models.CharField(
        verbose_name='Name of star system',
        max_length=200,
        blank=False
    )
    ref_eddb_system_id = models.PositiveIntegerField(blank=True, null=True)

    def to_json(self):
        return dict(
            id=self.id,
            name=self.name,
        )

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(
        verbose_name='Name of station',
        max_length=200,
        blank=False
    )
    located_in_system = models.ForeignKey('StarSystem', on_delete=models.CASCADE)
    located_near = models.ForeignKey('Body', on_delete=models.CASCADE, blank=True, null=True)
    ref_eddb_station_id = models.PositiveIntegerField(blank=True, null=True)

    def to_json_simple(self):
        return dict(
            id=self.id,
            name=self.name
        )

    def to_json(self):
        return dict(
            id=self.id,
            name=self.name,
            located_in_system=self.located_in_system.id,
            location=dict(
                id=self.id,
                type='station',
                located_in=dict(
                    id=self.located_in_system.id,
                    type='star_system'
                )
            )
        )

    def __str__(self):
        return self.name


class Body(models.Model):
    name = models.CharField(
        verbose_name='Name of body',
        max_length=200,
        blank=False
    )
    located_near = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    ref_eddb_body_id = models.PositiveIntegerField(blank=True, null=True)

    def to_json(self):
        return dict(
            id=self.id,
            name=self.name,
            located_near=self.located_near
        )

    def __str__(self):
        return self.name


class Advertisement(models.Model):

    # defines
    AD_TYPE_BARTER_TRADE = 'AD_TYPE_BARTER_TRADE'
    AD_TYPE_SEEK_PROTECTION = 'AD_TYPE_SEEK_PROTECTION'
    AD_TYPE_OFFER_PROTECTION = 'AD_TYPE_OFFER_PROTECTION'
    AD_TYPE_PLAYER_BOUNTY = 'AD_TYPE_PLAYER_BOUNTY'

    AD_COMBAT_RANK_HARMLESS = 'AD_COMBAT_RANK_HARMLESS'
    AD_COMBAT_RANK_MOSTLY_HARMLESS = 'AD_COMBAT_RANK_HARMLESS'
    AD_COMBAT_RANK_NOVICE = 'AD_COMBAT_RANK_NOVICE'
    AD_COMBAT_RANK_COMPETENT = 'AD_COMBAT_RANK_COMPETENT'
    AD_COMBAT_RANK_EXPERT = 'AD_COMBAT_RANK_EXPERT'
    AD_COMBAT_RANK_MASTER = 'AD_COMBAT_RANK_MASTER'
    AD_COMBAT_RANK_DANGEROUS = 'AD_COMBAT_RANK_DANGEROUS'
    AD_COMBAT_RANK_DEADLY = 'AD_COMBAT_RANK_DEADLY'
    AD_COMBAT_RANK_ELITE = 'AD_COMBAT_RANK_ELITE'

    AD_COMBAT_ROLE_ATTACKER = 'AD_COMBAT_ROLE_ATTACKER'
    AD_COMBAT_ROLE_DEFENDER = 'AD_COMBAT_ROLE_DEFENDER'
    AD_COMBAT_ROLE_SUPPORT = 'AD_COMBAT_ROLE_SUPPORT'

    commander = models.ForeignKey('Commander', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)

    type = models.CharField(
        verbose_name='Advertisement type',
        max_length=50,
        blank=False,
        choices=(
            (AD_TYPE_BARTER_TRADE, 'Exchange and trade of goods/materials'),
            (AD_TYPE_PLAYER_BOUNTY, 'Player bounty'),
            (AD_TYPE_SEEK_PROTECTION, 'Seeking protection'),
            (AD_TYPE_OFFER_PROTECTION, 'Offering protection'),
        )
    )

    activities_involved = models.ManyToManyField('Activity', related_name="ads_with_activity")

    # Combat/flight skill
    combat_rank = models.CharField(
        verbose_name='Combat rank',
        max_length=50,
        blank=True,
        null=True,
        choices=(
            (AD_COMBAT_RANK_HARMLESS, 'Harmless'),
            (AD_COMBAT_RANK_MOSTLY_HARMLESS, 'Mostly Harmless'),
            (AD_COMBAT_RANK_NOVICE, 'Novice'),
            (AD_COMBAT_RANK_COMPETENT, 'Competent'),
            (AD_COMBAT_RANK_EXPERT, 'Expert'),
            (AD_COMBAT_RANK_MASTER, 'Master'),
            (AD_COMBAT_RANK_DANGEROUS, 'Dangerous'),
            (AD_COMBAT_RANK_DEADLY, 'Deadly'),
            (AD_COMBAT_RANK_ELITE, 'Elite'),
        )
    )

    hours_in_game = models.PositiveIntegerField(default=0)

    # How can you help
    crew_member = models.BooleanField(default=False)
    wing_member = models.BooleanField(default=True)

    # combat role

    combat_role = models.CharField(
        verbose_name='Combat role',
        max_length=50,
        blank=False,
        null=True,
        choices=(
            (AD_COMBAT_ROLE_ATTACKER, 'Attacker'),
            (AD_COMBAT_ROLE_DEFENDER, 'Defender'),
            (AD_COMBAT_ROLE_SUPPORT, 'Support'),
        )
    )

    # Barter trade data
    tradeable_from = models.ForeignKey('Tradeable', related_name='as_tradeables_from',
                                       on_delete=models.CASCADE, blank=True, null=True)
    tradeable_to = models.ForeignKey('Tradeable', related_name='as_tradeables_to',
                                     on_delete=models.CASCADE, blank=True, null=True)

    # Legality - is it locally legal or not to engage in activity asked help for
    legal = models.BooleanField(default=False, blank=False)

    payment_pro_bono = models.BooleanField(default=False)
    payment_type = models.ForeignKey('Tradeable', related_name='as_payment',
                                     on_delete=models.CASCADE, blank=True, null=True)
    payment_units = models.PositiveIntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False, verbose_name='Is advertisement closed')
    hidden = models.BooleanField(default=False, verbose_name='Is advertisement hidden from search and listings')

    def to_json(self):
        json_response = dict(
            id=self.id,
            commander=self.commander.to_json_simple(),
            type=self.type,
            station=self.station.to_json_simple(),
            payment_type=self.payment_type.to_json() if self.payment_type else None,
            payment_units=self.payment_units,
            tradeable_from=self.tradeable_from.to_json() if self.tradeable_from else None,
            tradeable_to=self.tradeable_to.to_json() if self.tradeable_to else None,
            combat_role=self.combat_role,
            legal=self.legal,
            crew_member=self.crew_member,
            wing_member=self.wing_member,
            combat_rank=self.combat_rank,
            hours_in_space=self.hours_in_game,
            activities_involved=None
        )

        print(json_response)

        activities_involved = []

        for activity in self.activities_involved.all():
            activities_involved.append(
                dict(
                    id=activity.id,
                    name=activity.name
                )
            )

        json_response.update(
            activities_involved=activities_involved
        )

        return json_response

    def to_json_with_responses(self):
        response = self.to_json()

        response.update(
            responses=[response.to_json() for response in self.ad_responses_advert.all()],
        )

        return response

    # at this point we have cargo in units and amount of units - money isn't transeferable so that's not stored in db


class Tradeable(models.Model):

    UNIT_TON = 'UNIT_TON'
    UNIT_PIECE = 'UNIT_PIECE'

    name = models.CharField(max_length=100)
    unit_type = models.CharField(
        verbose_name='Type of measurement',
        max_length=50,
        blank=False,
        choices=(
            (UNIT_TON, 'In tons'),
            (UNIT_PIECE, 'In pieces'),
        )
    )

    rare = models.BooleanField(default=False)
    category = models.ForeignKey('TradeableCategory', related_name='tradeables_in_category',
                                 on_delete=models.CASCADE)

    def to_json(self):
        return dict(
            id=self.id,
            icon=self.category.icon.url,
            name=self.name,
            unit_type=self.unit_type
        )

    def __str__(self):
        return self.name


class TradeableCategory(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class AdResponse(models.Model):
    commander = models.ForeignKey('Commander', related_name='ad_responses_commander', on_delete=models.CASCADE)
    ad = models.ForeignKey('Advertisement', related_name='ad_responses_advert', on_delete=models.CASCADE)
    #notes = models.CharField(max_length=200)
    favorite = models.BooleanField(default=False)
    chosen = models.BooleanField(default=False)
    datetime_responded = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        print([message.to_json() for message in self.related_communication.all()])
        return dict(
            id=self.id,
            commander_id=self.commander.id,
            commander_name=self.commander.name,
            messages=[message.to_json() for message in self.related_communication.all()],
        )


class Message(models.Model):
    note = models.CharField(max_length=300)
    commander_from = models.ForeignKey('Commander', related_name='sent_messages', on_delete=models.CASCADE)
    commander_to = models.ForeignKey('Commander', related_name='recieved_messages', on_delete=models.CASCADE)
    meetup_station = models.ForeignKey('Station', related_name='mentioned_in_messages', null=True, blank=True, on_delete=models.CASCADE)
    meetup_datetime = models.DateTimeField(null=True, blank=True)
    #discord_show = models.BooleanField(default=False) # do commander wants to be communicated via discord, could be just shown automatically when applying
    #discord_name = models.CharField(max_length=200, verbose_name='') #? maybe it goes into user profile
    ad_response = models.ForeignKey('AdResponse', related_name='related_communication', on_delete=models.CASCADE)
    datetime_sent = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return dict(
            id=self.id,
            note=self.note,
            commander_from_id=self.commander_from.id,
            commander_from_name=self.commander_from.name,
            ad_response_id=self.ad_response.id,
        )
