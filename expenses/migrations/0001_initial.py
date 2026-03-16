import uuid
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.CharField(db_index=True, max_length=100)),
                ('event_ts', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('amount_minor', models.IntegerField()),
                ('currency', models.CharField(default='INR', max_length=10)),
                ('description', models.CharField(max_length=255)),
                ('category', models.CharField(default='Other', max_length=50)),
                ('convo_id', models.CharField(blank=True, default='', max_length=100)),
                ('source', models.CharField(default='web', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-event_ts'],
            },
        ),
        migrations.CreateModel(
            name='MonthlyRollup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.CharField(db_index=True, max_length=100)),
                ('year_month', models.CharField(max_length=6)),
                ('totals_by_category', models.JSONField(default=dict)),
                ('total_amount_minor', models.IntegerField(default=0)),
                ('top_items', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('user_id', 'year_month')},
            },
        ),
    ]
