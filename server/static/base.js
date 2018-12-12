const AD_TYPE_BARTER_TRADE = 'AD_TYPE_BARTER_TRADE';
const AD_TYPE_SEEK_PROTECTION = 'AD_TYPE_SEEK_PROTECTION';
const AD_TYPE_OFFER_PROTECTION = 'AD_TYPE_OFFER_PROTECTION';
const AD_TYPE_PLAYER_BOUNTY = 'AD_TYPE_PLAYER_BOUNTY';

const AD_COMBAT_ROLE_ATTACKER = 'AD_COMBAT_ROLE_ATTACKER';
const AD_COMBAT_ROLE_DEFENDER = 'AD_COMBAT_ROLE_DEFENDER';
const AD_COMBAT_ROLE_SUPPORT = 'AD_COMBAT_ROLE_SUPPORT';

const AD_COMBAT_RANK_HARMLESS = 'AD_COMBAT_RANK_HARMLESS';
const AD_COMBAT_RANK_MOSTLY_HARMLESS = 'AD_COMBAT_RANK_HARMLESS';
const AD_COMBAT_RANK_NOVICE = 'AD_COMBAT_RANK_NOVICE';
const AD_COMBAT_RANK_COMPETENT = 'AD_COMBAT_RANK_COMPETENT';
const AD_COMBAT_RANK_EXPERT = 'AD_COMBAT_RANK_EXPERT';
const AD_COMBAT_RANK_MASTER = 'AD_COMBAT_RANK_MASTER';
const AD_COMBAT_RANK_DANGEROUS = 'AD_COMBAT_RANK_DANGEROUS';
const AD_COMBAT_RANK_DEADLY = 'AD_COMBAT_RANK_DEADLY';
const AD_COMBAT_RANK_ELITE = 'AD_COMBAT_RANK_ELITE';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = 'csrftoken';

var commander_comms = new Vue({
    el: '#commander-comms',
    delimiters: ['${', '}'],
    data: {
        commander_comms_shown: true,
        ads: []
    },
    methods: {
        showComms() {
            this.updateComms();
            this.commander_comms_shown = true;
        },
        updateComms() {
            var $this = this;
            axios.get('/api/comms/')
            .then(function (response) {
                console.log(response);
                $this.ads = response.data;
            })
            .catch(function (error) {
                console.log('Catch');
                if( error.response ){
                    console.log(error.response.data);
                }
            });
        },
        write_ad(ad) {
            return write_ad(ad);
        },
        ad_click(ad) {
            console.log(ad);
            ad_show_pane.ad = ad;
            ad_show_pane.ad_shown = true;
            ad_show_pane.ad_responses_shown = true;
        },
        toggleClose(ad) {
            var $this = this;
            axios.post('/api/advertisement/' + ad['id'] + '/close/', this.response)
            .then(function (response) {
                if(ad['close']==true) {
                    ad['close']=false;
                    Vue.set(ad, 'close', false);
                } else {
                    ad['close']=true;
                    Vue.set(ad, 'true', false);
                }
            })
            .catch(function (error) {
                if( error.response ){
                    console.log(error.response.data);
                }
            });
        },
        toggleHidden(ad) {
            var $this = this;
            axios.post('/api/advertisement/' + ad['id'] + '/hide/', this.response)
            .then(function (response) {
                if(ad['hide']==true) {
                    ad['hide']=false;
                } else {
                    ad['hide']=true;
                }
            })
            .catch(function (error) {
                if( error.response ){
                    console.log(error.response.data);
                }
            });
        }
    },
    beforeMount() {
    this.updateComms()
    }
});

var ad_show_pane = new Vue({
    el: '#ad-show-pane',
    delimiters: ['${', '}'],
    data: {
        ad_shown: false,
        response_form_shown: false,
        response_button_shown: true,
        ad_responses_shown: false,
        ad: {},
        response: {},
        response_reply_shown: {},
        response_reply: {},
    },
    methods: {
        show(ad) {
            this.ad_shown = true;
            this.ad = ad;
            console.log(ad);
        },
        adTitle(ad) {
            if(ad['type'] == AD_TYPE_BARTER_TRADE) {
                return "Trading";
            }
        },
        respond_advert() {
            if(!this.response_form_shown) {
                this.response_form_shown = true;
            } else {
                // add response to advert
                var $this = this;
                axios.post('/api/advertisement/' + $this.ad['id'] + '/respond/', this.response)
                .then(function (response) {
                    console.log(response);
                })
                .catch(function (error) {
                    console.log('Catch');
                    if( error.response ){
                        console.log(error.response.data);
                    }
                });
            }
        },
        write_ad(ad) {
            return write_ad(ad);
        },
        show_reply_to_response(response_id) {
            console.log(response_id);
            Vue.set(this.response_reply_shown, response_id, true);
        },
        post_reply_to_response(response_id) {
            var $this = this;
            axios.post('/api/advertisement/response/' + response_id + '/reply/', {'note': $this.response_reply[response_id]})
                .then(function (response) {
                    console.log(response.data);
                })
                .catch(function (error) {
                console.log(error.response);
            });
            Vue.set(this.response_reply_shown, response_id, false);
        },
    }
});

var ads_list = new Vue({
    el: '#ads-group',
    delimiters: ['${', '}'],
    data: {
        ads_shown: true,
        ads: []
    },
    methods: {
        update() {
            var $this = this;
            axios.post('/api/advertisement/search/', { "search_method": 'by_station', 'search_station_id': station_id })
                .then(function (response) {
                    console.log(response.data);
                    var ads_list = [];
                    for(var i = 0; i < response.data.length; i++) {
                        var obj = response.data[i];
                        var new_obj = JSON.parse(JSON.stringify(obj));
                        new_obj['text'] = write_ad(obj);
                        ads_list.push(new_obj);
                    }
                    $this.ads = ads_list;
                })
                .catch(function (error) {
                console.log(error);
            });
        },
        ad_click(ad) {
           ad_show_pane.show(ad);
        }
    },
    beforeMount() {
    this.update()
    }
});

var add_ad_form = new Vue({
    el: '#adaddformapp',
    delimiters: ['${', '}'],
    data: {
        fields: {
            ad_ad_type: AD_TYPE_BARTER_TRADE,
            ad_combat_rank: AD_COMBAT_RANK_MOSTLY_HARMLESS,
            ad_requirements_hours: 0,
            ad_wing_member: true,
            ad_crew_member: false,
            ad_legal: true,
            ad_payment_pro_bono: false,
            ad_tradeable_from: 0,
            ad_tradeable_from_units: 0,
            ad_tradeable_to: 0,
            ad_tradeable_to_units: 0,
            ad_activities: [],
        },
        show_form: false
    },
    methods: {
        resetForm() {
            this.fields.ad_ad_type = AD_TYPE_BARTER_TRADE;
            this.fields.ad_combat_rank = AD_COMBAT_RANK_MOSTLY_HARMLESS;
            this.fields.ad_requirements_hours = 0;
            this.fields.ad_wing_member = true;
            this.fields.ad_crew_member = false;
            this.fields.ad_legal = true;
            this.fields.ad_payment_pro_bono = false;
            this.fields.ad_tradeable_from = 0;
            this.fields.ad_tradeable_from_units = 0;
            this.fields.ad_tradeable_to = 0;
            this.fields.ad_tradeable_to_units = 0;
            this.fields.ad_activities = [];
        },
        submit() {
            var $this = this;
            axios.post('/api/advertisement/add/', this.fields)
                .then(function (response) {
                console.log(response);
                ads_list.update();
                $this.resetForm();
                $this.show_form = false;
                })
                .catch(function (error) {
                console.log(error);
            });
        },
        showForm() {
            this.show_form = true
        },
        changeAdType() {
            switch(this.ad_ad_type) {
                case AD_TYPE_BARTER_TRADE:
                    $('.ad-option').hide();
                    $('.trading').show();
                    break;
                case AD_TYPE_SEEK_PROTECTION:
                case AD_TYPE_OFFER_PROTECTION:
                    $('.ad-option').hide();
                    $('.activities').show();
                    $('.requirements').show();
                    break;
                default:
                    $('.ad-option').hide();
            }
        }
    }
});

// Setup CSRF cookie support for non-form AJAX requests
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// **********************************
// string constructions for ad texts

function commander_name_html(commander) {
    return 'Commander ' + commander['name'];
}

function combat_rank_html(combat_rank) {
    var ad_text = '';
    switch(combat_rank) {
        case AD_COMBAT_RANK_HARMLESS:
        ad_text += 'Harmless';
        break;
        case AD_COMBAT_RANK_MOSTLY_HARMLESS:
        ad_text += 'Mostly Harmless';
        break;
        case AD_COMBAT_RANK_NOVICE:
        ad_text += 'Novice';
        break;
        case AD_COMBAT_RANK_COMPETENT:
        ad_text += 'Competent';
        break;
        case AD_COMBAT_RANK_EXPERT:
        ad_text += 'Expert';
        break;
        case AD_COMBAT_RANK_MASTER:
        ad_text += 'Master';
        break;
        case AD_COMBAT_RANK_DANGEROUS:
        ad_text += 'Dangerous';
        break;
        case AD_COMBAT_RANK_DEADLY:
        ad_text += 'Deadly';
        break;
        case AD_COMBAT_RANK_ELITE:
        ad_text += 'Elite';
        break;
    }

    ad_text += ' combat rank required. ';

    return ad_text;
}

// produce string about crew and wing members

function crew_member_html(crew_member, wing_member) {
    var ad_text = '';
    // seeking wing member
    if (wing_member) {
        ad_text += 'wing member ';
    }

    // seeking crew member
    if (crew_member) {
        if (wing_member) {
            ad_text += 'or ';
        }
        ad_text += 'crew member ';
    }

    if (!wing_member && !crew_member) {
        ad_text += 'help ';
    }

    return ad_text;
}

function combat_role_html(combat_role) {
    var ad_text = '';
    if (combat_role == AD_COMBAT_ROLE_ATTACKER) {
        ad_text += 'attacker role ';
    } else if (combat_role == AD_COMBAT_ROLE_DEFENDER) {
        ad_text += 'defender role ';
    } else if (combat_role == AD_COMBAT_ROLE_SUPPORT) {
        ad_text += 'support role ';
    }
    return ad_text;
}

function activities_involved_html(activities_involved) {
    var ad_text = '';
    if (activities_involved) {
        ai = activities_involved;
        ai_count = ai.length;

        for (var i=0; i < ai_count; i++) {
            ad_text += ai[i]['name'];
            if(i +1 == ai_count) {
                ad_text +=' operations. ';
                break;
            }
            ad_text +=', ';
        }
    }
    return ad_text;
}

function payment_html(payment_type, payment_units) {
    var ad_text = '';
    if (payment_type) {
        ad_text += 'Payment in ';
        ad_text += payment_type['name'];
        if(payment_units) {
            ad_text += ', ' + payment_units + ' tons';
        }
        ad_text +='. ';
    }
    return ad_text;
}

// ********************
// Writing ad

function write_ad(ad) {

    switch(ad['type']) {

    case AD_TYPE_BARTER_TRADE:
        var tradeable_from = ad['tradeable_from']['name'];
        var tradeable_to = ad['tradeable_to']['name'];
        var ad_text = '';
        ad_text = commander_name_html(ad['commander']) + ' is seeking trade for exchanging <img src="' + ad['tradeable_from']['icon'] + '" width="18vw" style="stroke: white; fill: white;"></img> ' + tradeable_from + ' for <img src="' + ad['tradeable_to']['icon'] + '" width="18vw"></img> ' + tradeable_to + '. ';
        ad_text += 'For exchange rate and where to conclude deal contact issuer.';
        return ad_text;
        break;

    case AD_TYPE_SEEK_PROTECTION:
        ad_text = '';
        ad_text += commander_name_html(ad['commander']) + ' is seeking ';
        // what kind of member we are looking for team
        ad_text += crew_member_html(ad['crew_member'], ad['wing_member']);

        ad_text += 'for ';

        // role
        if (ad['combat_role']) {
            ad_text += combat_role_html(ad['combat_role']);
        }

        if (ad['activities_involved']) {
            ad_text += activities_involved_html(ad['activities_involved']);
        }

        if (ad['combat_rank']) {
            ad_text += combat_rank_html(ad['combat_rank']);
        }

        if(ad['hours_in_space']) {
            ad_text += ad['hours_in_space'] + ' hours minimum in space. ';
        }

        ad_text += payment_html(ad['payment_type'], ad['payment_units']);

        if (ad['legal']) {
            ad_text += 'Job might not be fully legal.';
        }

        return ad_text;
        break;

    case AD_TYPE_OFFER_PROTECTION:
        ad_text = '';
        ad_text += commander_name_html(ad['commander']) + ' is offering services, ';
        // what kind of member commander offers to be
        ad_text += crew_member_html(ad['crew_member'], ad['wing_member']);

        ad_text += 'for ';

        // role
        if (ad['combat_role']) {
            ad_text += combat_role_html(ad['combat_role']);
        }

        if (ad['activities_involved']) {
            ad_text += activities_involved_html(ad['activities_involved']);
        }

        if (ad['combat_rank']) {
            ad_text += combat_rank_html(ad['combat_rank']);
        }

        if(ad['hours_in_space']) {
            ad_text += ad['hours_in_space'] + ' hours minimum in space. ';
        }

        ad_text += payment_html(ad['payment_type'], ad['payment_units']);

        if (ad['legal']) {
            ad_text += 'Ready to for illegal activities too.';
        }
        //ad_text = 'Commander is offering his/her services as attacker, defender or support for any operations. Elite combat rank, 1000 hours minimum in space. Pro bono. Ready to for illegal activities too.';
        return ad_text;
        break;

    case AD_TYPE_PLAYER_BOUNTY:
        ad_text = '';
        ad_text += commander_name_html(ad['commander']) + ' is issuing bounty on another commander. ';
        ad_text += payment_html(ad['payment_type'], ad['payment_units']);
        if (ad['legal']) {
            ad_text += 'Hit job might not be fully legal. ';
        }

        return ad_text;
        break;

    default:
        return 'Unknown ad type';
    }
}

function load_and_show_ads(station_id) {
    $('.ads-group').html('');
    $.ajax({
        url : "/api/advertisement/search/",
        type : "POST",
        data: JSON.stringify({ "search_method": 'by_station', 'search_station_id': station_id }),
        contentType: 'application/json; charset=utf-8',

        // handle a successful response
        success : function(json) {
            var return_data = json;
            var ads_list = "";
            for(var i = 0; i < json.length; i++) {
                var obj = json[i];
                ads_list += '<div class="ad-info-block hg-line">' +
                        '<p>'+ write_ad(obj) + '</p>' +
                    '</div>';
            }
            $('#ads-group').html(ads_list);
            },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
            }
});
}

function set_station_id(e) {
    e.preventDefault();
    $('#search-pane').hide();
    station_id = $(this).attr('id');

    $.ajax({
        url: '/api/commander/set_station/',
        type: 'POST',
        data: {'station_id': $(this).attr('id')},

        success: function(json) {
            $('#station-name').html(json['name']);
            console.log('Station ID set');
        },

        error: function(xhr,errmsg,err) {

        }
    });

    load_and_show_ads(station_id);
}

$("#search-form").submit(function(e) {
    e.preventDefault();

    if ($('#search-location').val().length >= 2) {
        console.log('Search for ' + $('#search-location').val());
        $.ajax({
            url : "/api/location_search/", // the endpoint
            type : "POST", // http method
            data: { "search_location": $('#search-location').val() }, // padodam izveleto aktivitati

            // handle a successful response
            success : function(json) {
                    var return_data = json;
                    console.log(json);
                    $('#search-pane').show();
                    var search_results = "";
                    for(var i = 0; i < json.length; i++) {
                        var obj = json[i];
                        search_results += '<div class="search-entry"><a class="set-station-id" id="' + json[i]['id'] + '" href="#">' + json[i]['name'] + '</a></div>';
                    }
                    $('#search-results').html(search_results);
                    $('.set-station-id').click(set_station_id);
                },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>");
                    console.log(xhr.status + ": " + xhr.responseText);
                }
        });
    }
});


$('#search-pane-close-button').click(function(e) {
    e.preventDefault();
    $('#search-pane').hide();
});