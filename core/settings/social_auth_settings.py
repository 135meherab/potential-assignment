from .base_settings import env

GOOGLE_TOKEN_URL = env.url(
    "GOOGLE_TOKEN_URL", default="https://oauth2.googleapis.com/token"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
# GOOGLE_REDIRECT_URL = env.url("GOOGLE_REDIRECT_URL", default="http://localhost:8000/auth/google/callback")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ["email", "profile"]

SOCIAL_AUTH_APPLE_ID_SERVICE = env("SOCIAL_AUTH_APPLE_ID_SERVICE")
SOCIAL_AUTH_APPLE_ID_CLIENT = env("SOCIAL_AUTH_APPLE_ID_CLIENT")
SOCIAL_AUTH_APPLE_ID_TEAM = env("SOCIAL_AUTH_APPLE_ID_TEAM")
SOCIAL_AUTH_APPLE_ID_SECRET = env("SOCIAL_AUTH_APPLE_ID_SECRET")
SOCIAL_AUTH_APPLE_ID_KEY = env("SOCIAL_AUTH_APPLE_ID_KEY")
SOCIAL_AUTH_APPLE_ID_SCOPE = ["email", "name"]
APPLE_TOKEN_URL = env.url(
    "APPLE_TOKEN_URL", default="https://appleid.apple.com/auth/token"
)
# APPLE_REDIRECT_URL = env.url("APPLE_REDIRECT_URL", default="http://localhost:8000/auth/apple/callback")

KAKAO_TOKEN_URL = env.url(
    "KAKAO_TOKEN_URL", default="https://kauth.kakao.com/oauth/token"
)
SOCIAL_AUTH_KAKAO_KEY = env("SOCIAL_AUTH_KAKAO_KEY")
SOCIAL_AUTH_KAKAO_SECRET = env("SOCIAL_AUTH_KAKAO_SECRET")
SOCIAL_AUTH_KAKAO_SCOPE = ["account_email", "profile_image", "profile_nickname"]

NAVER_TOKEN_URL = env.url(
    "NAVER_TOKEN_URL", default="https://nid.naver.com/oauth2.0/token"
)
SOCIAL_AUTH_NAVER_KEY = env("SOCIAL_AUTH_NAVER_KEY")
SOCIAL_AUTH_NAVER_SECRET = env("SOCIAL_AUTH_NAVER_SECRET")

GITHUB_TOKEN_URL = env.url(
    "GITHUB_TOKEN_URL", default="https://github.com/login/oauth/access_token"
)
SOCIAL_AUTH_GITHUB_KEY = env("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = env("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GITHUB_SCOPE = ["user:email"]


DEEPL_TRANSLATOR_API_KEY = env("DEEPL_TRANSLATOR_API_KEY", default="")


SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
