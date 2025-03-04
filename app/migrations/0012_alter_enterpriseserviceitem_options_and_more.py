# Generated by Django 4.2.17 on 2025-01-13 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0011_alter_familyservicepackage_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="enterpriseserviceitem",
            options={
                "ordering": ["order", "-created_at"],
                "verbose_name": "企业服务项目",
                "verbose_name_plural": "企业服务项目",
            },
        ),
        migrations.AlterField(
            model_name="enterpriseserviceitem",
            name="description",
            field=models.TextField(blank=True, verbose_name="服务说明"),
        ),
        migrations.AlterField(
            model_name="enterpriseserviceitem",
            name="supported_packages",
            field=models.ManyToManyField(
                blank=True, to="app.enterpriseservicepackage", verbose_name="支持的套餐"
            ),
        ),
        migrations.AlterField(
            model_name="enterpriseserviceitem",
            name="title",
            field=models.TextField(
                help_text="支持换行，每行一个服务内容", verbose_name="服务内容"
            ),
        ),
    ]
