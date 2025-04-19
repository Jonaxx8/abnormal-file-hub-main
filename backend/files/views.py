from django.shortcuts import render
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime, timedelta
from .models import File, StorageStatistics
from .serializers import FileSerializer, StorageStatisticsSerializer

# Create your views here.

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        queryset = File.objects.all()
        
        # Search by filename
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(original_filename__icontains=search)
        
        # Filter by file type
        file_type = self.request.query_params.get('file_type', None)
        if file_type:
            queryset = queryset.filter(file_type__icontains=file_type)
        
        # Filter by size range (in bytes)
        min_size = self.request.query_params.get('min_size', None)
        max_size = self.request.query_params.get('max_size', None)
        if min_size:
            queryset = queryset.filter(size__gte=int(min_size))
        if max_size:
            queryset = queryset.filter(size__lte=int(max_size))
        
        # Filter by upload date
        date_filter = self.request.query_params.get('date_filter', None)
        if date_filter:
            today = datetime.now()
            if date_filter == 'today':
                queryset = queryset.filter(uploaded_at__date=today.date())
            elif date_filter == 'week':
                week_ago = today - timedelta(days=7)
                queryset = queryset.filter(uploaded_at__gte=week_ago)
            elif date_filter == 'month':
                month_ago = today - timedelta(days=30)
                queryset = queryset.filter(uploaded_at__gte=month_ago)
            elif date_filter == 'custom':
                start_date = self.request.query_params.get('start_date')
                end_date = self.request.query_params.get('end_date')
                if start_date:
                    queryset = queryset.filter(uploaded_at__gte=parse_datetime(start_date))
                if end_date:
                    queryset = queryset.filter(uploaded_at__lte=parse_datetime(end_date))
        
        return queryset.select_related('original_file')

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
