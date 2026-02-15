from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
