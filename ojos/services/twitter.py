import tweepy


class OAuth2UserHandler(tweepy.OAuth2UserHandler):
    # Kudos https://github.com/tweepy/tweepy/pull/1806
    def refresh_token(self, refresh_token):
        new_token = super().refresh_token(
            "https://api.twitter.com/2/oauth2/token",
            refresh_token=refresh_token,
            body=f"grant_type=refresh_token&client_id={self.client_id}",
        )
        return new_token
