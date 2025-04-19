from rest_framework import serializers
from .models import File, StorageStatistics

class FileSerializer(serializers.ModelSerializer):
    is_duplicate = serializers.BooleanField(read_only=True)
    duplicate_of = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'file', 'original_filename', 'file_type', 'size', 
                 'uploaded_at', 'is_duplicate', 'duplicate_of']
        read_only_fields = ['id', 'uploaded_at', 'is_duplicate']

    def get_duplicate_of(self, obj):
        if obj.original_file:
            return str(obj.original_file.id)
        return None

class StorageStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageStatistics
        fields = ['total_files', 'duplicate_files', 'total_size', 'saved_size', 'last_updated']