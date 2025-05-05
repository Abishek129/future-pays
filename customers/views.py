from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Cart, global_pool
from products.models import Size, Product
from .serializers import CartSerializer
from .tasks import distribute_money, add_refferal_money




class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()  # ← this is what DRF was missing
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from authentication.models import CustomerPool
from .serializers import OrderSerializer
from customers.models import Cart, Address
class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        size_label = request.data.get('size')
        product_id = request.data.get('product')

        if not size_label or not product_id:
            return Response({"error": "Both size and product are required"}, status=400)

        try:
            size = Size.objects.get(label=size_label.lower())
        except Size.DoesNotExist:
            return Response({"error": "Invalid size provided"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Invalid product ID"}, status=400)

        cart = Cart.objects.create(
            user=user,
            size=size,
            product=product
        )

        return Response({"status": "Cart item added", "cart_id": cart.id}, status=201)

    def get(self, request, cart_id):
        user = request.user

        try:
            cart = Cart.objects.get(id=cart_id, user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)

        data = {
            "id": cart.id,
            "product": cart.product.name,
            "size": cart.size.label,
            "payable_amount": str(cart.payable_amount),
        }
        return Response(data, status=200)



from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView


class BuyNowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart_id = request.data.get('cart')
            address_id = request.data.get('address')

            if not cart_id or not address_id:
                return Response({'error': 'Cart and Address are required.'}, status=400)

            cart = Cart.objects.filter(id=cart_id, user=request.user).first()
            if not cart:
                return Response({'error': 'Cart not found or unauthorized.'}, status=404)

            address = Address.objects.filter(id=address_id, user=request.user).first()
            if not address:
                return Response({'error': 'Address not found or unauthorized.'}, status=404)

            order = Order.objects.create(
                user=request.user,
                product=cart.product,
                size=cart.size,
                payable_amount=cart.payable_amount,
                address=address,
                payment_status='paid',
                order_status='placed'
            )

            serializer = OrderSerializer(order)
            customer_pool = CustomerPool.objects.get(owner = request.user)
            gp = global_pool.objects.order_by('id').first()
            customer_pool.token = gp.end+1
            customer_pool.save()
            gp.end+=1
            gp.pool_amount += 200
            if gp.end - gp.start + 1 == 2**gp.counter:
                gp.counter+=1
                distribute_money(gp.pool_amount, gp.start)
                gp.start = gp.end + 1
                
                gp.pool_amount = 0
            gp.save()
            add_refferal_money(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:

            cart = Cart.objects.filter(id=cart_id, user=request.user).first()
            if not cart:
                return Response({'error': 'Cart not found or unauthorized.'}, status=404)
            print(cart)
            address = Address.objects.filter(id=address_id, user=request.user).first()
            if not address:
                return Response({'error': 'Address not found or unauthorized.'}, status=404)
            print(address)
            return Response({'error': str(e)}, status=500)
        



