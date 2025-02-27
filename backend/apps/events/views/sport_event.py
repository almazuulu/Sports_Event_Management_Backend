from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

from events.models import SportEvent
from events.serializers import (
    SportEventSerializer,
    SportEventCreateUpdateSerializer,
    SportEventPublicSerializer
)
from users.permissions import IsAdminUser, IsScorekeeper


class SportEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for SportEvents management.
    Provides CRUD operations with appropriate permissions.
    
    Admins have full access to create, update, and delete sport events.
    Authenticated users can view full sport event details.
    Unauthenticated users can access limited sport event information.
    
    Authentication is done via JWT Bearer token.
    """
    queryset = SportEvent.objects.all().order_by('start_date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event', 'sport_type', 'status']
    search_fields = ['name', 'description', 'rules', 'scoring_system']
    ordering_fields = ['name', 'start_date', 'end_date', 'registration_deadline']
    authentication_classes = [JWTAuthentication]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SportEventCreateUpdateSerializer
        elif self.action == 'public':
            return SportEventPublicSerializer
        return SportEventSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action == 'public':
            permission_classes = [AllowAny]
        elif self.action == 'update_status':
            permission_classes = [IsAdminUser | IsScorekeeper]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
        summary="Public sport events listing",
        description="Get a list of scheduled, registration, or ongoing sport events with limited information. No authentication required.",
        parameters=[
            OpenApiParameter(name="date", description="Filter sport events ending after this date (YYYY-MM-DD)", required=False, type=str),
            OpenApiParameter(name="event", description="Filter by event ID", required=False, type=str),
            OpenApiParameter(name="sport_type", description="Filter by sport type (e.g., football, basketball)", required=False, type=str)
        ],
        responses={200: SportEventPublicSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='public', authentication_classes=[])
    def public(self, request):
        """
        Public endpoint for retrieving basic sport event information.
        Does not require authentication.
        """
        # Only include active and registration sport events
        status_filter = Q(status='scheduled') | Q(status='registration') | Q(status='ongoing')
        
        # Base queryset with status filter
        queryset = SportEvent.objects.filter(status_filter).order_by('start_date')
        
        # Apply date filter only if date parameter is provided
        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(end_date__gte=date_param)
        
        # Filter by event if provided
        event_id = self.request.query_params.get('event')
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        
        # Filter by sport type if provided
        sport_type = self.request.query_params.get('sport_type')
        if sport_type:
            queryset = queryset.filter(sport_type=sport_type)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Update sport event status",
        description="Update the status of a sport event. Only admins and scorekeepers can update the status.",
        request={"application/json": {"type": "object", "properties": {"status": {"type": "string"}}}},
        responses={
            200: SportEventSerializer,
            400: OpenApiResponse(description="Bad request - invalid status transition"),
            403: OpenApiResponse(description="Forbidden - user does not have permission")
        }
    )
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Update the status of a sport event.
        Only admins and scorekeepers can update the status of a sport event.
        Requires JWT authentication.
        """
        sport_event = self.get_object()
        
        # Check if user is admin or scorekeeper
        if not (request.user.role == 'admin' or request.user.role == 'scorekeeper'):
            return Response(
                {"detail": _("You do not have permission to perform this action.")},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate new status
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {"status": _("This field is required.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate status transition
        valid_transitions = {
            'scheduled': ['registration', 'cancelled'],
            'registration': ['registration_closed', 'ongoing', 'cancelled'],
            'registration_closed': ['ongoing', 'cancelled'],
            'ongoing': ['completed', 'cancelled'],
            'completed': [],
            'cancelled': []
        }
        
        if new_status not in valid_transitions.get(sport_event.status, []):
            return Response(
                {"status": _("Invalid status transition from {} to {}.".format(
                    sport_event.get_status_display(), dict(SportEvent.GAME_STATUS_CHOICES).get(new_status)
                ))},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update status
        sport_event.status = new_status
        sport_event.updated_by = request.user
        sport_event.save(update_fields=['status', 'updated_by', 'updated_at'])
        
        serializer = self.get_serializer(sport_event)
        return Response(serializer.data)
    
    # Add documentation for the main ModelViewSet methods
    @extend_schema(
        summary="List all sport events",
        description="Returns a list of all sport events. Requires authentication.",
        responses={200: SportEventSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a new sport event",
        description="Create a new sport event. Only administrators can create sport events.",
        request=SportEventCreateUpdateSerializer,
        responses={201: SportEventSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve a sport event",
        description="Get details of a specific sport event. Requires authentication.",
        responses={200: SportEventSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update a sport event",
        description="Fully update a specific sport event. Only administrators can update sport events.",
        request=SportEventCreateUpdateSerializer,
        responses={200: SportEventSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partial update a sport event",
        description="Partially update a specific sport event. Only administrators can update sport events.",
        request=SportEventCreateUpdateSerializer,
        responses={200: SportEventSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete a sport event",
        description="Delete a specific sport event. Only administrators can delete sport events.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)