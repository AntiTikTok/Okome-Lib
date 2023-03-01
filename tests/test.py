from tweepy_authlib import CookieSessionUserHandler
import tweepy

auth_handler = CookieSessionUserHandler(screen_name='', password='')
cookies = auth_handler.get_cookies()

api = tweepy.API(auth_handler)
print(api.verify_credentials())
print(api.home_timeline())