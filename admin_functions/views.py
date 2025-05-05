from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from customers.models import global_pool
from .serializers import GlobalPoolSerializer
from rest_framework import generics
from authentication.models import User, CustomerPool

class GlobalPoolCreateDeleteView(generics.GenericAPIView):
    queryset = global_pool.objects.all()
    serializer_class = GlobalPoolSerializer
    #permission_classes = [permissions.IsAdminUser]  # Optional: restrict to admins

    def post(self, request, *args, **kwargs):
        global_pool_obj = global_pool.objects.create()
        global_pool_obj.refresh_from_db()
        serializer = self.get_serializer(global_pool_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        try:
            # Delete the latest global_pool (by highest ID)
            latest_pool = global_pool.objects.latest('id')
            latest_pool.delete()
            return Response({"message": "Latest global pool deleted."}, status=status.HTTP_204_NO_CONTENT)
        except global_pool.DoesNotExist:
            return Response({"error": "No global pool exists to delete."}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.views import APIView

class GlobalPoolResetView(APIView):

    def post(self, request):

        gp = global_pool.objects.get(id = request.data.get('global_pool'))
        if not gp:
            return Response({'error': "global_pool not found"}, status=400)
        gp.start = 2
        gp.end = 1
        gp.pool_amount = 0.00
        gp.counter = 1
        gp.latest = 1
        gp.save()

        return Response({"status":  "Pool Updated"}, status=200)
    


class CustomerPoolResetView(APIView):
    def post(self, request):
        user = User.objects.get(email = request.data.get('email'))
        if not user:
            return Response({"error": " Invalied User"}, status= 400)
        customer_pool = CustomerPool.objects.get(owner = user)
        customer_pool.token = -1
        customer_pool.save()

        return Response({"status": "Customer Pool Updated"}, status = 200)
    

class CustomersPoolResetView(APIView):

    def post(self, request):
        updated_count = CustomerPool.objects.all().update(token=-1, is_active=True)
        return Response({"status": f"{updated_count} Customer Pools Updated"}, status=status.HTTP_200_OK)
        
        
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
#from .models import CustomerPool

User = get_user_model()

class CreateCustomerPool(APIView):
    def post(self, request):
        email = request.data.get('email')
        token = request.data.get('token')

        if not email or token is None:
            return Response({"error": "Email and token are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if pool already exists
        if CustomerPool.objects.filter(owner=user).exists():
            return Response({"error": "Customer Pool already exists for this user"}, status=status.HTTP_400_BAD_REQUEST)

        CustomerPool.objects.create(owner=user, token=token)

        return Response({"status": "Customer Pool created successfully"}, status=status.HTTP_201_CREATED)


        

