# Generated by Django 4.2.6 on 2023-10-29 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classwise_Fee',
            fields=[
                ('student_class', models.CharField(choices=[('nursery', 'Nursery'), ('pp-I', 'PP-I'), ('pp-II', 'PP-II'), ('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V'), ('VI', 'VI'), ('VII', 'VII'), ('VIII', 'VIII'), ('IX', 'IX'), ('X', 'X'), ('XI', 'XI'), ('XII', 'XII')], max_length=10, primary_key=True, serialize=False)),
                ('tuition_fee', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('exam_fee', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('miscellaneous_fee', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('area_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('transport_fee', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeeDetails',
            fields=[
                ('adm_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='home.student')),
                ('section', models.CharField(blank=True, max_length=50, null=True)),
                ('student_name', models.CharField(blank=True, max_length=50, null=True)),
                ('tuition_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('exam_fee', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('miscellaneous_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fee_concession', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fee_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('balance_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('area_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.transportation')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.classwise_fee')),
            ],
        ),
    ]
