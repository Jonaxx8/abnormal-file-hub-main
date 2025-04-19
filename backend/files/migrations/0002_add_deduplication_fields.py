from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_hash',
            field=models.CharField(db_index=True, max_length=64, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='is_duplicate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='file',
            name='original_file',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='duplicates',
                to='files.file'
            ),
        ),
        migrations.CreateModel(
            name='StorageStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_files', models.IntegerField(default=0)),
                ('duplicate_files', models.IntegerField(default=0)),
                ('total_size', models.BigIntegerField(default=0)),
                ('saved_size', models.BigIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
