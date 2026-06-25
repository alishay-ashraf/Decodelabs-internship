class ProtectedDataView(APIView):
    def get(self, request):
        # Extract token from the Authorization header (Format: Bearer <token>)
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
            
        token = auth_header.split(' ')[1]
        
        try:
            # The bouncer decodes and verifies the signature using the Master Key
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            
            # If successful, return the vault data
            return Response({
                "message": "Access Granted to the Digital Vault!",
                "secret_industrial_data": ["Component-A: Passing", "Component-B: Optimized"]
            }, status=status.HTTP_200_OK)
            
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired. Please log in again."}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token security breach detected."}, status=status.HTTP_401_UNAUTHORIZED)