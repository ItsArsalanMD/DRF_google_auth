from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, login
from rest_framework_simplejwt.tokens import RefreshToken

from google_auth.sdk.services import (
    GoogleSdkLoginFlowService,
)


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class GoogleLoginRedirectApi(PublicApi):
    def get(self, request, *args, **kwargs):
        google_login_flow = GoogleSdkLoginFlowService()

        authorization_url, state = google_login_flow.get_authorization_url()

        request.session["google_oauth2_state"] = state

        return redirect(authorization_url)
    

class GoogleLoginApi(PublicApi):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        if error is not None:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )

        if code is None or state is None:
            return Response(
                {"error": "Code and state are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        session_state = request.session.get("google_oauth2_state")

        # if session_state is None:
        #     return Response(
        #         {"error": "session is none."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # # del request.session["google_oauth2_state"]

        # if state != session_state:
        #     return Response(
        #         {"error": "CSRF check failed."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
            
        google_login_flow = GoogleSdkLoginFlowService()

        google_tokens = google_login_flow.get_tokens(code=code, state=state)

        # id_token_decoded = google_tokens.decode_id_token()
        user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

        user_email = user_info["email"]
        
        User = get_user_model()  # Get the user model
        user, created = User.objects.get_or_create(
            email=user_email,
            defaults={
                "username": user_info.get("name"),
                "first_name": user_info.get("given_name", ""),
                "last_name": user_info.get("family_name", ""),
            }
        )
        
        if created:
            # You can set additional fields for the newly created user here if needed
            user.set_unusable_password()  # If using social login, you can set an unusable password
            user.save()

        if user is None:
            return Response(
                {"error": f"User with email {user_email} is not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        login(request, user)
        
         # Generate JWT tokens using Simple JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        result = {
            "refresh_token": str(refresh),
            "access_token": access_token,
            "user_info": user_info,
        }

        return Response(result)