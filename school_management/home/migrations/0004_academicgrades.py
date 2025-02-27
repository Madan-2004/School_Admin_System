# Generated by Django 4.2.6 on 2023-10-29 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicGrades',
            fields=[
                ('adm_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='home.student')),
                ('academic_year', models.CharField(max_length=10)),
                ('first_language', models.DecimalField(decimal_places=2, max_digits=5)),
                ('second_language', models.DecimalField(decimal_places=2, max_digits=5)),
                ('third_language', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mathematics', models.DecimalField(decimal_places=2, max_digits=5)),
                ('science', models.DecimalField(decimal_places=2, max_digits=5)),
                ('social', models.DecimalField(decimal_places=2, max_digits=5)),
                ('computers', models.DecimalField(decimal_places=2, max_digits=5)),
                ('overall_grade', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
