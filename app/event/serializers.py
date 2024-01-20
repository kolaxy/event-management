from rest_framework import serializers
from .models import Organization, Event
from users.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema, swagger_serializer_method
from drf_yasg import openapi


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("title", "description", "address", "postcode")


class EventSerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ["id", "description", "organizations", "image", "date", "title"]


class EventCreateSerializer(EventSerializer):
    class Meta(EventSerializer.Meta):
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    format=openapi.FORMAT_INT64,
                    description="The unique identifier for the item.",
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="A description for the item."
                ),
                "organizations": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "0": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="The title of the organization",
                                    ),
                                    "description": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="The description for the organization",
                                    ),
                                    "info": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Info about the organization",
                                    ),
                                    "founder": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Org's founder",
                                    ),
                                    "members": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Items(
                                            type=openapi.TYPE_STRING,
                                            description="Members",
                                        ),
                                    ),
                                },
                            ),
                        },
                    ),
                    description="List of organizations",
                ),
                "image": openapi.Schema(
                    type=openapi.TYPE_FILE, description="An image."
                ),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description="Date",
                ),
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Ttile"),
            },
            "required": ["id", "description", "organizations", "date", "title"],
        }

    @swagger_serializer_method(serializer_or_field=serializers.JSONField())
    def get_organizations(self, obj):
        organizations_data = []
        for organization in obj.organizations.all():
            members_list = [str(member) for member in organization.members.all()]
            founder = str(organization.founder) if organization.founder else None
            organization_info = {
                organization.id: {
                    "title": organization.title,
                    "description": organization.description,
                    "info": f"{organization.address} {organization.postcode}",
                    "founder": founder,
                    "members": members_list,
                }
            }
            organizations_data.append(organization_info)

        return organizations_data
