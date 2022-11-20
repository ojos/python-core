import tweepy


class OAuth2UserHandler(tweepy.OAuth2UserHandler):
    def get_authorization_url(self):
        """Get the authorization URL to redirect the user to"""
        code_verifier = self._client.create_code_verifier(128)
        auth_url, state = self.authorization_url(
            "https://twitter.com/i/oauth2/authorize",
            code_challenge=self._client.create_code_challenge(code_verifier, "S256"),
            code_challenge_method="S256",
        )
        return auth_url, state, code_verifier

    def fetch_token(self, authorization_response, code_verifier=None):
        """After user has authorized the app, fetch access token with
        authorization response URL
        """
        return super(tweepy.OAuth2UserHandler, self).fetch_token(
            "https://api.twitter.com/2/oauth2/token",
            authorization_response=authorization_response,
            auth=self.auth,
            include_client_id=True,
            code_verifier=code_verifier or self._client.code_verifier,
        )

    # Kudos https://github.com/tweepy/tweepy/pull/1806
    def refresh_token(self, refresh_token):
        new_token = super().refresh_token(
            "https://api.twitter.com/2/oauth2/token",
            refresh_token=refresh_token,
            body=f"grant_type=refresh_token&client_id={self.client_id}",
        )
        return new_token
