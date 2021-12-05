from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import  Product, Order, OrderItem, ShippingAddress
from .serializers import ProductSerializer, UserSerializer, OrderSerializer
from django.contrib.auth.hashers import make_password


# Обновление пользовательской информации
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    
    data = request.data
    if data['name'] !='':
        user.name = data['name']
    if data['email'] !='':
        user.email = data['email']
    if data['password'] !='':
        user.password = make_password(data['password'])
    
    user.save()
    
    return Response(serializer.data)



# Идентифицированный пользователь
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


# Функции отображения для товаров
@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view (['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False, context={'request': request})
    return Response (serializer.data)


# Функция отображения для заказов
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user 
    data = request.data
    
    orderItems = data['orderItems']
    
    if orderItems and len(orderItems) == 0:
        return Response({'details' : 'No oder Items'}, status = status.HTTP_400_BAD_REQUEST)
    else:
        # Создаем запись в табице Заказ
        order = Order.objects.create(
            user=user,
            paymentMethod = data['paymentMethod'],
            phoneNumber = data['phone'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            orderPrice = data['orderPrice'],            
        )
        # Создаем запись в табице Адрес для доставки
        shipping = ShippingAddress.objects.create(
            user=user,
            order = order,
            city = data['city'],
            street = data['street'],
            house = data['house'],
            postalCode = data['postalCode'],

        )
        
       
        for i in orderItems:
            product = Product.objects.get(_id=i['_id'])
            
            item = OrderItem.objects.create(
                product=product,
                order=order,
                title = product.title,
                qty = int(i['quantity']),
                price=i['price'],
                image=product.imageCover              
            )
        
        product.available -= item.qty
        product.save()
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


# Получаем информацию о заказе из БД по id заказа. 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
  user= request.user                    # 1
  try:
    order = Order.objects.get(_id=pk)
    if user.is_staff or order.user == user:         # 2
      serializer = OrderSerializer(order, many=False, context={'request': request})  # 3
      return Response(serializer.data)        # 4
    else:
      Response({'detail': 'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST)
  except:
    return Response({'detail':'Order does not exist'},status=status.HTTP_400_BAD_REQUEST )


# Получаем информацию о заказах конкретного пользователя. 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
  user= request.user
  orders = user.order_set.all()  
  serializer = OrderSerializer(orders, many=True, context={'request': request})                 
  return Response(serializer.data)










