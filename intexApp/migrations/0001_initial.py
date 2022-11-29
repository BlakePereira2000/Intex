# Generated by Django 4.1.2 on 2022-11-29 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comorbidity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comorbidity_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Daily_Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('daily_weight', models.DecimalField(decimal_places=2, max_digits=8)),
                ('avg_blood_sugar', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lab_blood_pressure', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lab_sodium', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lab_creatinine', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lab_albumin', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lab_potassium', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lab_phosphorus', models.DecimalField(decimal_places=2, max_digits=8)),
                ('water_intake', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=200)),
                ('sodium', models.DecimalField(decimal_places=2, max_digits=8)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=8)),
                ('potassium', models.DecimalField(decimal_places=2, max_digits=8)),
                ('phosphorus', models.DecimalField(decimal_places=2, max_digits=8)),
                ('water', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=30)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=8)),
                ('height', models.DecimalField(decimal_places=2, max_digits=8)),
                ('gender', models.CharField(max_length=1)),
                ('stage', models.IntegerField(default=0)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('comorbidities', models.ManyToManyField(blank=True, to='intexapp.comorbidity')),
            ],
        ),
        migrations.CreateModel(
            name='Food_in_Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grams', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intexapp.food')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intexapp.daily_journal')),
            ],
        ),
        migrations.AddField(
            model_name='daily_journal',
            name='daily_foods',
            field=models.ManyToManyField(through='intexapp.Food_in_Day', to='intexapp.food'),
        ),
        migrations.AddField(
            model_name='daily_journal',
            name='journal_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='intexapp.user'),
        ),
    ]
