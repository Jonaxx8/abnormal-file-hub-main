from django.db import models
import uuid
import os
import hashlib

def file_upload_path(instance, filename):
    """Generate file path for new file upload"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=file_upload_path)
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_hash = models.CharField(max_length=64, db_index=True)  # SHA-256 hash
    is_duplicate = models.BooleanField(default=False)
    original_file = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='duplicates'
    )
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.original_filename

    def calculate_hash(self):
        """Calculate SHA-256 hash of file content"""
        sha256 = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()

class StorageStatistics(models.Model):
    total_files = models.IntegerField(default=0)
    duplicate_files = models.IntegerField(default=0)
    total_size = models.BigIntegerField(default=0)  # in bytes
    saved_size = models.BigIntegerField(default=0)  # in bytes
    last_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def update_statistics(cls):
        stats, _ = cls.objects.get_or_create(id=1)
        files = File.objects.all()
        
        stats.total_files = files.count()
        stats.duplicate_files = files.filter(is_duplicate=True).count()
        stats.total_size = sum(f.size for f in files)
        stats.saved_size = sum(f.size for f in files.filter(is_duplicate=True))
        stats.save()
