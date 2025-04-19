from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import File, StorageStatistics
from .serializers import FileSerializer, StorageStatisticsSerializer

# Create your views here.

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a temporary file instance to calculate hash
        temp_file = File(
            file=file_obj,
            original_filename=file_obj.name,
            file_type=file_obj.content_type,
            size=file_obj.size
        )
        
        # Calculate file hash
        file_hash = temp_file.calculate_hash()
        
        # Check for existing file with same hash
        existing_file = File.objects.filter(file_hash=file_hash, is_duplicate=False).first()
        
        if existing_file:
            # Create new file record pointing to existing file
            new_file = File.objects.create(
                file=existing_file.file,
                original_filename=file_obj.name,
                file_type=file_obj.content_type,
                size=file_obj.size,
                file_hash=file_hash,
                is_duplicate=True,
                original_file=existing_file
            )
            serializer = self.get_serializer(new_file)
        else:
            # Save new file
            temp_file.file_hash = file_hash
            temp_file.save()
            serializer = self.get_serializer(temp_file)
        
        # Update storage statistics
        StorageStatistics.update_statistics()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        stats = StorageStatistics.objects.first()
        if not stats:
            stats = StorageStatistics.update_statistics()
        serializer = StorageStatisticsSerializer(stats)
        return Response(serializer.data)
