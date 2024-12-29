import json
import time
from datetime import timedelta

import jwt
import requests
import requests.exceptions
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from jwt.algorithms import RSAAlgorithm
from rest_framework import exceptions, response, status, views
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.backends.apple import AppleIdAuth
from social_core.backends.github import GithubOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.kakao import KakaoOAuth2
from social_core.backends.naver import NaverOAuth2
from social_core.exceptions import AuthForbidden, AuthTokenError, MissingBackend
from social_django.utils import load_backend, load_strategy

from authentications.register import register_social_user, save_image_from_url
from authentications.serializers import SocialLoginSerializer

from .common_functions import direct_login, extract_token, get_token, set_jwt_cookies


class KakaoWebLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        redirect_to = request.GET.get("redirect_to", None)
        if redirect_to is None:
            raise exceptions.ValidationError(_("Redirect URL not provided"))
        request.session["redirect_to"] = redirect_to

        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy,
            name="kakao",
            redirect_uri=request.build_absolute_uri("/api/auth/kakao-callback/"),
        )
        auth_url = backend.auth_url()
        return redirect(auth_url)


class KakaoCallbackView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        code = request.GET.get("code", None)
        if code is None:
            return response.Response({"error": _("Code not provided")}, status=400)

        strategy = load_strategy(request)
        kakao_backend = KakaoOAuth2(strategy=strategy)
        data = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_KAKAO_KEY,
            "redirect_uri": self.request.build_absolute_uri(
                "/api/auth/kakao-callback/"
            ),
            "grant_type": "authorization_code",
        }

        try:
            resp = requests.post(settings.KAKAO_TOKEN_URL, data=data)
            user_data = kakao_backend.user_data(resp.json().get("access_token"))

            user = register_social_user(
                profile_image_url=user_data.get("kakao_account")
                .get("profile")
                .get("profile_image_url"),
                email=user_data.get("kakao_account").get("email"),
                name=user_data.get("kakao_account").get("profile").get("nickname"),
                provider="kakao",
                role="user",
            )

            # Set cookies and redirect to frontend
            redirect_to = request.session.get("redirect_to")
            resp = redirect(redirect_to)

            return direct_login(
                request, resp, user, extract_token(get_token(user)), True
            )

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e


class NaverWebLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        redirect_to = request.GET.get("redirect_to", None)
        if redirect_to is None:
            raise exceptions.ValidationError(_("Redirect URL not provided"))
        request.session["redirect_to"] = redirect_to

        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy,
            name="naver",
            redirect_uri=request.build_absolute_uri("/api/auth/naver-callback/"),
        )
        auth_url = backend.auth_url()
        return redirect(auth_url)


class NaverCallbackView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        code = request.GET.get("code", None)
        if code is None:
            return response.Response({"error": _("Code not provided")}, status=400)

        strategy = load_strategy(request)
        naver_backend = NaverOAuth2(strategy=strategy)
        data = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_NAVER_KEY,
            "client_secret": settings.SOCIAL_AUTH_NAVER_SECRET,
            "redirect_uri": self.request.build_absolute_uri(
                "/api/auth/naver-callback/"
            ),
            "grant_type": "authorization_code",
        }

        try:
            resp = requests.post(settings.NAVER_TOKEN_URL, data=data)
            access_token = resp.json().get("access_token")

            user_data = naver_backend.user_data(access_token)

            user = register_social_user(
                profile_image_url=user_data.get("profile_image"),
                email=user_data.get("email"),
                name=user_data.get("nickname"),
                provider="naver",
                role="user",
            )

            # Set cookies and redirect to frontend
            redirect_to = request.session.get("redirect_to")
            resp = redirect(redirect_to)

            return direct_login(
                request, resp, user, extract_token(get_token(user)), True
            )

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e


class GoogleWebLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        redirect_to = request.GET.get("redirect_to", None)
        if redirect_to is None:
            raise exceptions.ValidationError(_("Redirect URL not provided"))
        request.session["redirect_to"] = redirect_to

        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy,
            name="google-oauth2",
            redirect_uri=request.build_absolute_uri("/api/auth/google-callback/"),
        )
        auth_url = backend.auth_url()
        return redirect(auth_url)


class GoogleCallbackView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        code = request.GET.get("code", None)
        if code is None:
            return response.Response({"error": _("Code not provided")}, status=400)

        strategy = load_strategy(request)
        google_backend = GoogleOAuth2(strategy=strategy)

        try:
            data = {
                "code": code,
                "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                "redirect_uri": request.build_absolute_uri(
                    "/api/auth/google-callback/"
                ),
                "grant_type": "authorization_code",
            }
            resp = requests.post(settings.GOOGLE_TOKEN_URL, data=data)
            user = google_backend.user_data(resp.json().get("access_token"))

            user = register_social_user(
                profile_image_url=user.get("picture"),
                email=user.get("email"),
                name=user.get("name"),
                provider="google",
                role="user",
            )

            # Set cookies and redirect to frontend
            redirect_to = request.session.get("redirect_to")
            resp = redirect(redirect_to)

            return direct_login(
                request, resp, user, extract_token(get_token(user)), True
            )

        except Exception as e:
            raise exceptions.AuthenticationFailed(detail=str(e))


class GithubWebLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        redirect_to = request.GET.get("redirect_to", None)
        if redirect_to is None:
            raise exceptions.ValidationError(_("Redirect URL not provided"))
        request.session["redirect_to"] = redirect_to

        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy,
            name="github",
            redirect_uri=request.build_absolute_uri("/api/auth/github-callback/"),
        )
        auth_url = backend.auth_url()
        return redirect(auth_url)


class GithubCallbackView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        code = request.GET.get("code", None)
        if code is None:
            return response.Response({"error": _("Code not provided")}, status=400)

        strategy = load_strategy(request)
        github_backend = GithubOAuth2(strategy=strategy)
        data = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_GITHUB_KEY,
            "client_secret": settings.SOCIAL_AUTH_GITHUB_SECRET,
            "redirect_uri": request.build_absolute_uri("/api/auth/github-callback/"),
        }

        try:
            resp = requests.post(
                settings.GITHUB_TOKEN_URL,
                data=data,
                headers={"Accept": "application/json"},
            )
            access_token = resp.json().get("access_token")

            user_data = github_backend.user_data(access_token)

            user = register_social_user(
                profile_image_url=user_data.get("avatar_url"),
                email=user_data.get("email"),
                name=user_data.get("name")
                or user_data.get("login"),  # GitHub might not provide name
                provider="github",
                role="user",
            )

            # Set cookies and redirect to frontend
            redirect_to = request.session.get("redirect_to")
            resp = redirect(redirect_to)

            return direct_login(
                request, resp, user, extract_token(get_token(user)), True
            )

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e
