from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductImage, ProductFeature
from .product_serializers import ProductSerializer

class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data.copy()
        
        # Extract features from request
        features = []
        for key, value in request.data.items():
            if key.startswith('features[') and value.strip():
                features.append(value.strip())
        
        # Create product
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            
            # Add features
            for feature_text in features:
                ProductFeature.objects.create(product=product, feature=feature_text)
            
            # Handle images
            for key, file in request.FILES.items():
                if key.startswith('images['):
                    index = int(key.split('[')[1].split(']')[0])
                    primary_index = int(request.data.get('primary_image_index', 0))
                    is_primary = index == primary_index
                    ProductImage.objects.create(
                        product=product,
                        image=file,
                        is_primary=is_primary
                    )
            
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            data = request.data.copy()
            
            # Update product basic fields
            serializer = ProductSerializer(product, data=data, partial=True)
            if serializer.is_valid():
                product = serializer.save()
                
                # Update features
                features = []
                for key, value in request.data.items():
                    if key.startswith('features[') and value.strip():
                        features.append(value.strip())
                
                if features:
                    # Clear existing features and add new ones
                    ProductFeature.objects.filter(product=product).delete()
                    for feature_text in features:
                        ProductFeature.objects.create(product=product, feature=feature_text)
                
                # Handle image deletions
                for key, value in request.data.items():
                    if key.startswith('delete_images['):
                        try:
                            image_id = int(value)
                            ProductImage.objects.filter(id=image_id, product=product).delete()
                        except (ValueError, ProductImage.DoesNotExist):
                            pass
                
                # Handle new images (append to existing)
                primary_index = int(request.data.get('primary_image_index', -1))
                for key, file in request.FILES.items():
                    if key.startswith('images['):
                        index = int(key.split('[')[1].split(']')[0])
                        is_primary = index == primary_index
                        ProductImage.objects.create(
                            product=product,
                            image=file,
                            is_primary=is_primary
                        )
                
                return Response(ProductSerializer(product).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class LatestProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class SetPrimaryImageView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            image_id = request.data.get('image_id')
            
            if not image_id:
                return Response({'error': 'image_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set all images as non-primary
            ProductImage.objects.filter(product=product).update(is_primary=False)
            
            # Set the selected image as primary
            try:
                image = ProductImage.objects.get(id=image_id, product=product)
                image.is_primary = True
                image.save()
                return Response({'message': 'Primary image updated successfully'})
            except ProductImage.DoesNotExist:
                return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
                
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)