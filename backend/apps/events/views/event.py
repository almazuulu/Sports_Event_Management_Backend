from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

from events.models import Event
from events.serializers import (
    EventSerializer,
    EventCreateUpdateSerializer,
    EventPublicSerializer,
    SportEventSerializer
)
from users.permissions import IsAdminUser


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Events management.
    Provides CRUD operations with appropriate permissions.
   
    Admins have full access to create, update, and delete events.
    Authenticated users can view full event details.
    Unauthenticated users can access limited event information.
   
    Authentication is done via JWT Bearer token.
    """
    queryset = Event.objects.all().order_by('start_date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'location']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['name', 'start_date', 'end_date', 'created_at']
    authentication_classes = [JWTAuthentication]
   
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventCreateUpdateSerializer
        elif self.action == 'public':
            return EventPublicSerializer
        return EventSerializer
   
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action == 'public':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
   
    @extend_schema(
        summary="Public events listing",
        description="Get a list of active and registration events with limited information. No authentication required.",
        parameters=[
            OpenApiParameter(name="date", description="Filter events ending after this date (YYYY-MM-DD)", required=False, type=str)
        ],
        responses={200: EventPublicSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='public', authentication_classes=[])
    def public(self, request):
        """
        Public endpoint for retrieving basic event information.
        Does not require authentication.
        """
        # Only include active and completed events that haven't ended yet
        queryset = Event.objects.filter(
            Q(status='active') | Q(status='registration'),
            end_date__gte=self.request.query_params.get('date', None)
        ).order_by('start_date')
       
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
           
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
   
    @extend_schema(
        summary="Sport events for an event",
        description="Retrieve all sport events for a specific event. Requires authentication.",
        responses={200: SportEventSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_path='sport-events')
    def sport_events(self, request, pk=None):
        """
        Retrieve all sport events for a specific event.
        Requires JWT authentication.
        """
        event = self.get_object()
        sport_events = event.sport_events.all().order_by('start_date')
       
        page = self.paginate_queryset(sport_events)
        if page is not None:
            serializer = SportEventSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
           
        serializer = SportEventSerializer(sport_events, many=True)
        return Response(serializer.data)
        
    # Add documentation for the main methods of ModelViewSet
    @extend_schema(
        summary="List all events",
        description="Returns a list of all events. Requires authentication.",
        responses={200: EventSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a new event",
        description="Create a new event. Only administrators can create events.",
        request=EventCreateUpdateSerializer,
        responses={201: EventSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve an event",
        description="Get details of a specific event. Requires authentication.",
        responses={200: EventSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update an event",
        description="Fully update a specific event. Only administrators can update events.",
        request=EventCreateUpdateSerializer,
        responses={200: EventSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partial update an event",
        description="Partially update a specific event. Only administrators can update events.",
        request=EventCreateUpdateSerializer,
        responses={200: EventSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete an event",
        description="Delete a specific event. Only administrators can delete events.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)