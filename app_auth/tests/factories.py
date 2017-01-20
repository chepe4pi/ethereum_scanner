import factory
from allauth.socialaccount.models import SocialAccount

from app_auth.models import ApiKey, ClientInfo
from app_core.tests.factories import UserFactory


class ClientInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientInfo

    ip_address = '127.0.0.2'


class ApiKeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApiKey

    key = '123'
    client_info = factory.SubFactory(ClientInfoFactory)


twitter_extra_data = {
    "status": {"possibly_sensitive": False, "source": "<a href=\"http://justcoz.org\" rel=\"nofollow\">justcoz</a>",
               "text": "Donate a tweet a day to @greenpeaceru. Spread the word and make a difference. https://t.co/0d4kQXJlRg \u261ehttps://t.co/0Hd2qheDPj",
               "in_reply_to_user_id_str": None, "truncated": False, "id_str": "759043928913944576", "entities": {
            "urls": [{"expanded_url": "http://mo.nu/r/greenpeaceru/965/3?uid=4yYX", "url": "https://t.co/0d4kQXJlRg",
                      "indices": [78, 101], "display_url": "mo.nu/r/greenpeaceru\u2026"},
                     {"expanded_url": "http://justcoz.org", "url": "https://t.co/0Hd2qheDPj", "indices": [103, 126],
                      "display_url": "justcoz.org"}], "hashtags": [], "symbols": [], "user_mentions": [
                {"id": 55518204, "name": "Greenpeace Russia", "indices": [24, 37], "screen_name": "greenpeaceru",
                 "id_str": "55518204"}]}, "in_reply_to_status_id_str": None, "in_reply_to_status_id": None,
               "coordinates": None, "contributors": None, "in_reply_to_user_id": None, "is_quote_status": False,
               "created_at": "Fri Jul 29 15:12:29 +0000 2016", "id": 759043928913944576, "favorite_count": 0,
               "retweet_count": 0, "retweeted": False, "favorited": False, "lang": "en", "geo": None, "place": None,
               "in_reply_to_screen_name": None}, "profile_use_background_image": True,
    "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", "favourites_count": 0,
    "profile_sidebar_fill_color": "DDEEF6", "follow_request_sent": False, "is_translator": False, "lang": "ru",
    "created_at": "Wed Jan 15 13:33:21 +0000 2014", "id_str": "2292713618", "profile_background_tile": False,
    "listed_count": 0, "profile_text_color": "333333", "entities": {"description": {"urls": []}}, "url": None,
    "screen_name": "chepe4pi", "translator_type": "none", "following": False, "geo_enabled": False,
    "statuses_count": 57, "id": 2292713618, "time_zone": None, "followers_count": 0, "utc_offset": None,
    "profile_image_url": "http://pbs.twimg.com/profile_images/771255744922394624/ikSvtpF7_normal.jpg",
    "profile_sidebar_border_color": "C0DEED", "location": "", "default_profile": True, "verified": False,
    "profile_link_color": "1DA1F2",
    "profile_image_url_https": "https://pbs.twimg.com/profile_images/771255744922394624/ikSvtpF7_normal.jpg",
    "has_extended_profile": False,
    "name": "\u041a\u0443\u0440\u044b\u043b\u0435\u0432 \u0410\u043b\u0435\u043a\u0441\u0435\u0439", "protected": False,
    "contributors_enabled": False, "profile_background_color": "C0DEED",
    "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", "default_profile_image": False,
    "notifications": False, "is_translation_enabled": False, "friends_count": 0, "description": ""}


class SocialAccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = SocialAccount

    user = factory.SubFactory(UserFactory)
    provider = 'twitter'
    extra_data = twitter_extra_data
