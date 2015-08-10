from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.utils.timezone import now, timedelta

def get_access_token(user):
    # our oauth2 app
    app, created = Application.objects.get_or_create(user=user, name="myapp")

    try:
        cur_access_token = AccessToken.objects.get(
            user=user, application=app)
    except AccessToken.DoesNotExist:
        cur_access_token = None

    if cur_access_token:
        return cur_access_token
    else:
        # we generate a temporary token
        token = generate_token()
        # we generate a refresh token
        refresh_token = generate_token()

        expires = now() + timedelta(seconds=oauth2_settings.
                                    ACCESS_TOKEN_EXPIRE_SECONDS)
        scope = "read write"

        # we create the access token
        access_token = AccessToken.objects.\
            create(user=user,
                   application=app,
                   expires=expires,
                   token=token,
                   scope=scope)

        # we create the refresh token
        RefreshToken.objects.\
            create(user=user,
                   application=app,
                   token=refresh_token,
                   access_token=access_token)

        return access_token

def get_new_access_token(user):
    """
    Takes a user instance and return an access_token as a string
    """

    # our oauth2 app
    app = Application.objects.get(name="myapp")

    # We delete the old access_token and refresh_token
    try:
        old_access_token = AccessToken.objects.get(
            user=user, application=app)
        old_refresh_token = RefreshToken.objects.get(
            user=user, access_token=old_access_token
        )
    except:
        pass
    else:
        old_access_token.delete()
        old_refresh_token.delete()

    # we generate an access token
    token = generate_token()
    # we generate a refresh token
    refresh_token = generate_token()

    expires = now() + timedelta(seconds=oauth2_settings.
                                ACCESS_TOKEN_EXPIRE_SECONDS)
    scope = "read write"

    # we create the access token
    access_token = AccessToken.objects.\
        create(user=user,
               application=app,
               expires=expires,
               token=token,
               scope=scope)

    # we create the refresh token
    RefreshToken.objects.\
        create(user=user,
               application=app,
               token=refresh_token,
               access_token=access_token)

    # we call get_token_json and returns the access token as json
    return access_token
