from rest_framework import status, permissions, generics
from rest_framework.response import Response
from ..serializers import PasswordChangeSerializer

class PasswordChangeView(generics.GenericAPIView):
    """
    Change the password for the current authenticated user.
   
    Requires submitting the old password for verification,
    along with a new password and confirmation.
   
    * Requires authentication
    * Returns 200 OK on success
    * Returns 400 Bad Request if passwords don't match or old password is incorrect
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PasswordChangeSerializer
   
    def post(self, request):
        """
        Process password change request.
       
        Validates old password and ensures new password matches confirmation
        before updating the user's password in the database.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
       
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"status": "password set"}, status=status.HTTP_200_OK)