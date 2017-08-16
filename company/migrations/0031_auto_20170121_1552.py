# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-21 15:52
from __future__ import unicode_literals

import directory_validators.enrolment
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0030_auto_20170117_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='employees',
            field=models.CharField(blank=True, choices=[('', 'Please select an option'), ('1-10', '1-10'), ('11-50', '11-50'), ('51-200', '51-200'), ('201-500', '201-500'), ('501-1000', '501-1,000'), ('1001-10000', '1,001-10,000'), ('10001+', '10,001+')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='company',
            name='export_status',
            field=models.CharField(choices=[('', 'Please select an option'), ('YES', 'Yes, in the last year'), ('ONE_TWO_YEARS_AGO', 'Yes, 1 to 2 years ago'), ('OVER_TWO_YEARS_AGO', 'Yes, but more than 2 years ago'), ('NOT_YET', 'No, but we are preparing to'), ('NO_INTENTION', 'No, we are not planning to sell overseas')], max_length=20),
        ),
        migrations.AlterField(
            model_name='companycasestudy',
            name='sector',
            field=models.CharField(choices=[('AEROSPACE', 'Aerospace'), ('AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'Agriculture, horticulture and fisheries'), ('AIRPORTS', 'Airports'), ('AUTOMOTIVE', 'Automotive'), ('BIOTECHNOLOGY_AND_PHARMACEUTICALS', 'Biotechnology and pharmaceuticals'), ('BUSINESS_AND_CONSUMER_SERVICES', 'Business and consumer services'), ('CHEMICALS', 'Chemicals'), ('CLOTHING_FOOTWEAR_AND_FASHION', 'Clothing, footwear and fashion'), ('COMMUNICATIONS', 'Communications'), ('CONSTRUCTION', 'Construction'), ('CREATIVE_AND_MEDIA', 'Creative and media'), ('EDUCATION_AND_TRAINING', 'Education and training'), ('ELECTRONICS_AND_IT_HARDWARE', 'Electronics and IT hardware'), ('ENVIRONMENT', 'Environment'), ('FINANCIAL_AND_PROFESSIONAL_SERVICES', 'Financial and professional services'), ('FOOD_AND_DRINK', 'Food and drink'), ('GIFTWARE_JEWELLERY_AND_TABLEWARE', 'Giftware, jewellery and tableware'), ('GLOBAL_SPORTS_INFRASTRUCTURE', 'Global sports infrastructure'), ('HEALTHCARE_AND_MEDICAL', 'Healthcare and medical'), ('HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS', 'Household goods, furniture and furnishings'), ('LEISURE_AND_TOURISM', 'Leisure and tourism'), ('MARINE', 'Marine'), ('MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING', 'Mechanical electrical and process engineering'), ('METALLURGICAL_PROCESS_PLANT', 'Metallurgical process plant'), ('METALS_MINERALS_AND_MATERIALS', 'Metals, minerals and materials'), ('MINING', 'Mining'), ('OIL_AND_GAS', 'Oil and gas'), ('PORTS_AND_LOGISTICS', 'Ports and logistics'), ('POWER', 'Power'), ('RAILWAYS', 'Railways'), ('RENEWABLE_ENERGY', 'Renewable energy'), ('RETAIL_AND_LUXURY', 'Retail and luxury'), ('SECURITY', 'Security'), ('SOFTWARE_AND_COMPUTER_SERVICES', 'Software and computer services'), ('TEXTILES_INTERIOR_TEXTILES_AND_CARPETS', 'Textiles, interior textiles and carpets'), ('WATER', 'Water')], max_length=100),
        ),
    ]
