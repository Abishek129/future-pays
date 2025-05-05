from rest_framework.authentication import BaseAuthentication
from firebase_admin import auth as firebase_auth
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No token provided, move on to next auth method

        id_token = auth_header.split(" ")[1]
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token.get("uid")
            email = decoded_token.get("email")
        except Exception:
            raise AuthenticationFailed('Invalid or expired Firebase token.')

        try:
            # First, check if user exists with this firebase_uid
            user = User.objects.get(firebase_uid=uid)
        except User.DoesNotExist:
            try:
                # Check by email
                user = User.objects.get(email=email)
                if user.is_staff:  # If admin, update their firebase_uid
                    user.firebase_uid = uid
                    user.save()
                else:
                    # Not admin, raise authentication failed
                    raise AuthenticationFailed('User not authorized. Please sign up first.')
            except User.DoesNotExist:
                # No such user at all
                raise AuthenticationFailed('User not found. Please sign up first.')

        return (user, None)
    



# utils.py

import requests

def geocode_address(address):
    GEOCODING_API_KEY = "YOUR_GOOGLE_API_KEY"
    GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": GEOCODING_API_KEY
    }

    response = requests.get(GEOCODING_URL, params=params)
    if response.status_code != 200:
        raise Exception("Geocoding API request failed.")

    data = response.json()
    if data["status"] != "OK":
        raise Exception(f"Geocoding failed: {data['status']}")

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
