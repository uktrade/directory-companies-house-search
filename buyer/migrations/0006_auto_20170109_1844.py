# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-09 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0005_auto_20161206_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='sector',
            field=models.CharField(choices=[('', ''), ('AEROSPACE', 'Aerospace'), ('AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'Agriculture, Horticulture and Fisheries'), ('AIRPORTS', 'Airports'), ('AUTOMOTIVE', 'Automotive'), ('BIOTECHNOLOGY_AND_PHARMACEUTICALS', 'Biotechnology and Pharmaceuticals'), ('BUSINESS_AND_CONSUMER_SERVICES', 'Business and Consumer Services'), ('CHEMICALS', 'Chemicals'), ('CLOTHING_FOOTWEAR_AND_FASHION', 'Clothing, Footwear and Fashion'), ('COMMUNICATIONS', 'Communications'), ('CONSTRUCTION', 'Construction'), ('CREATIVE_AND_MEDIA', 'Creative and Media'), ('DEFENCE', 'Defence'), ('EDUCATION_AND_TRAINING', 'Education and Training'), ('ELECTRONICS_AND_IT_HARDWARE', 'Electronics and IT Hardware'), ('ENVIRONMENT', 'Environment'), ('FINANCIAL_AND_PROFESSIONAL_SERVICES', 'Financial and Professional Services'), ('FOOD_AND_DRINK', 'Food and Drink'), ('GIFTWARE_JEWELLERY_AND_TABLEWARE', 'Giftware, Jewellery and Tableware'), ('GLOBAL_SPORTS_INFRASTRUCTURE', 'Global Sports Infrastructure'), ('HEALTHCARE_AND_MEDICAL', 'Healthcare and Medical'), ('HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS', 'Household Goods, Furniture and Furnishings'), ('LEISURE_AND_TOURISM', 'Leisure and Tourism'), ('MARINE', 'Marine'), ('MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING', 'Mechanical Electrical and Process Engineering'), ('METALLURGICAL_PROCESS_PLANT', 'Metallurgical Process Plant'), ('METALS_MINERALS_AND_MATERIALS', 'Metals, Minerals and Materials'), ('MINING', 'Mining'), ('OIL_AND_GAS', 'Oil and Gas'), ('PORTS_AND_LOGISTICS', 'Ports and Logistics'), ('POWER', 'Power'), ('RAILWAYS', 'Railways'), ('RENEWABLE_ENERGY', 'Renewable Energy'), ('RETAIL_AND_LUXURY', 'Retail and Luxury'), ('SECURITY', 'Security'), ('SOFTWARE_AND_COMPUTER_SERVICES', 'Software and Computer Services'), ('TEXTILES_INTERIOR_TEXTILES_AND_CARPETS', 'Textiles, Interior Textiles and Carpets'), ('WATER', 'Water')], max_length=255),
        ),
    ]