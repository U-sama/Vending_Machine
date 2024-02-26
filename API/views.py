from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Users, Product
from .serializers import UsersSerializer, ProductSerializer
from .permissions import IsSameUser, IsOwnerOrReadOnly, IsSeller, PostAuth
from .utils import format_change



class UserListCreate(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsSameUser]

class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [PostAuth, IsSeller, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSeller, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user)

@api_view(['POST'])
def deposit(request):
    try:
        if request.user.role == 'buyer':
            coins = request.data.get('coins', {})
            deposit_amount = 0
            for coin, count in coins.items():
                if coin in ["5", "10", "20", "50", "100"]:
                    deposit_amount += int(coin) * int(count)
                else:
                    return Response({'error': 'Invalid coin amount'}, status=status.HTTP_400_BAD_REQUEST)
            request.user.deposit += deposit_amount
            request.user.save()
            return Response({'message': 'Deposit successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only buyers can deposit'}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'error': 'An error occurred during deposit'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def buy(request):
    try:
        if request.user.role == 'buyer':
            product_list = request.data.get('products')
            total_cost = 0
            for product in product_list:
                product_id = product.get('productId')
                amount = request.data.get('amount', 1)
                product = Product.objects.get(pk=product_id)
                product_total = product.cost * amount
                if request.user.deposit >= product_total:
                    if product.amountAvailable >= amount:
                        request.user.deposit -= product_total
                        product.amountAvailable -= amount
                        total_cost += product_total
                    else:
                        return Response({'error': 'Product out of stock'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
            change = request.user.deposit
            request.user.deposit = 0
            request.user.save()
            product.save()
            return Response({'message': 'Purchase successful',
                             "total_spent": total_cost,
                             "purchased_products": product_list,
                             'change': format_change(change)
                             }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only buyers can buy products'}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'error': 'An error occurred during purchase'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def reset_deposit(request):
    try:
        if request.user.role == 'buyer':
            request.user.deposit = 0
            request.user.save()
            return Response({'message': 'Deposit reset successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only buyers can reset deposit'}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'error': 'An error occurred during deposit reset'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
