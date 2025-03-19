from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
#besh kif nassen3ou product jdid nzidouha l user li aamél login
from rest_framework.permissions import IsAuthenticated
from .filter import ProductsFilter
from .models import Product, Review
from rest_framework import status
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from django.db.models import Avg
# Create your views here.

@api_view(['GET']) 
def get_all_products(request):
    filterset = ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    resPage = 2
    paginator = PageNumberPagination()
    paginator.page_size = resPage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializer(queryset,many=True)
    #products = Product.objects.all()
    #serializer = ProductSerializer(filterset.qs,many=True)
    print(filterset)
    return Response({"products":serializer.data})

@api_view(['GET'])
def get_by_id_product(request,pk):
    products = get_object_or_404(Product,id=pk)
    serializer = ProductSerializer(products,many=False)
    print(products)
    return Response({"product":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated]) #maynajém yaajouti kan kif yebda aamél login
def new_product(request): #Pas besoin d'un ID
    data = request.data 
    serializer = ProductSerializer(data = data)
    if serializer.is_valid():
        product = Product.objects.create(**data,user=request.user)
        res = ProductSerializer(product,many=False)
        
        return Response({"product":res.data})
    else:
        return Response(serializer.errors)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated]) #maynajém yaajouti kan kif yebda aamél login
def update_product(request,pk): #Pas besoin d'un ID
    product = get_by_id_product(Product,id=pk)
    
    #verifier si l user aandou lhak yaamél update ll produit
    if product.user != request.user:
        return Response({"error":"you can't update this product"}, status=status.HTTP_403_FORBIDDEN) #ma aandoush lha9 yaamél aaleha update
    
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']
    
    product.save()
    serializer = ProductSerializer(product,many=False)
    return Response({"product":serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) #maynajém yfassakh kan kif yebda aamél login
def delete_product(request,pk): #Pas besoin d'un ID
    product = get_by_id_product(Product,id=pk)
    
    #verifier si l user aandou lhak yaamél delete ll produit
    if product.user != request.user:
        return Response({"error":"you can't update this product"}, status=status.HTTP_403_FORBIDDEN) #ma aandoush lha9 yaamél aaleha update
    
    product.save()
    
    return Response({"data":"Delete is done"},status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) #maynajém yaajouti kan kif yebda aamél login
def create_review(request,pk): #lazem naamlou id 3la review khater kol review iji 3la produit mou3ayén
    user = request.user 
    product = get_object_or_404(Product,id=pk)
    data = request.data 
    review = product.reviews.filter(user=user)
   
    if data['rating'] <=0 or data['rating'] > 5:
        return Response({"error":'Please select between 1 to 5 only'}, status=status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        new_review = {'rating': data['rating'], 'comment':data['comment']}
        review.update(**new_review) 
        
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings'] 
        product.save()
        
        return Response({'details':'Product review updated'})
    
    else:
        Review.objects.create(
            user = user,
            product = product,
            rating = data['rating'],
            comment = data['comment']
        )
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        return Response({'details':'Product review created'})
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)
    
    
    review = product.reviews.aggregation(avg_ratings = Avg('rating'))
    
    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            
           rating['avg_ratings'] = 0
           product.ratings = rating['avg_ratings']
           product.save()
           return Response({'details':'Product review deleted'})
    else:
           return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)
        
          