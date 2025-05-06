

# Create your views here.
# views.py
from rest_framework import viewsets, status
from .models import Attribute, AttributeValue, Product, ProductImage
from .serializers import AttributeSerializer, AttributeValueSerializer, ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    @action(detail=True, methods=['get'], url_path='values')
    def get_attribute_values(self, request, pk=None):
        attribute = self.get_object()
        values = attribute.values.all()
        serializer = AttributeValueSerializer(values, many=True)
        return Response(serializer.data)

class AttributeValueViewSet(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def create(self, request, *args, **kwargs):
        data = request.data

        print("Received form data:", data)
        print("Received files:", request.FILES)

        # Extract images
        images = request.FILES.getlist('images')
        print("Received image files:", images)

        # Extract and create product
        product = Product.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            base_price = data.get("base_price"),
            offer_price = data.get("offer_price"),
            additional_details=data.get('additional_details'),
            is_active=data.get('is_active', 'true') == 'true',
            
            
        )

        # Set many-to-many attributes
        

        # Save images
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Size
from .serializers import SizeSerializer

class SizeCreateAPIView(APIView):
    def post(self, request):
        serializer = SizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    



