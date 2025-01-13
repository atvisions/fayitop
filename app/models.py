from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

class ContactMessage(models.Model):
    # 咨询类型选项
    SERVICE_CHOICES = [
        ('legal_consultation', '法律咨询'),
        ('labor_compliance', '劳资合规'),
        ('contract_optimization', '合约优化'),
        ('debt_management', '债权管理'),
        ('intellectual_property', '知识产权'),
        ('corporate_governance', '公司治理'),
    ]

    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('电话', max_length=20)
    email = models.EmailField('邮箱')
    service = models.CharField('咨询类型', max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField('咨询内容')
    created_at = models.DateTimeField('提交时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '联系咨询'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} - {self.get_service_display()}' 

class NewsCategory(models.Model):
    """新闻分类"""
    name = models.CharField('分类名称', max_length=50)
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '新闻分类'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.name

class News(models.Model):
    """新闻文章"""
    title = models.CharField('标题', max_length=200)
    category = models.ForeignKey(NewsCategory, verbose_name='分类', on_delete=models.CASCADE)
    summary = models.TextField('摘要', max_length=500, blank=True)
    content = CKEditor5Field('内容', config_name='default')
    thumbnail = models.ImageField('缩略图', upload_to='news/thumbnails/%Y/%m')
    views = models.IntegerField('浏览量', default=0)
    is_published = models.BooleanField('是否发布', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 如果没有摘要，自动从内容中提取
        if not self.summary and self.content:
            # 移除HTML标签后截取
            from django.utils.html import strip_tags
            self.summary = strip_tags(self.content)[:200]
        super().save(*args, **kwargs)

    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" style="max-height: 50px;"/>')
        return ''
    thumbnail_preview.short_description = '缩略图预览' 

class Category(models.Model):
    name = models.CharField('分类名称', max_length=100)
    slug = models.SlugField('分类标识', unique=True)
    description = models.TextField('分类描述', blank=True)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('文章标识', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    summary = models.TextField('摘要')
    content = CKEditor5Field('内容')
    thumbnail = models.ImageField('缩略图', upload_to='articles/thumbnails/')
    views = models.IntegerField('浏览量', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    publish_date = models.DateTimeField('发布时间', default=timezone.now)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-publish_date']

    def __str__(self):
        return self.title 

class Lawyer(models.Model):
    name = models.CharField('姓名', max_length=100)
    title = models.CharField('职位', max_length=100)
    image = models.ImageField('照片', upload_to='lawyers/')
    introduction = models.TextField('简介')
    email = models.EmailField('邮箱')
    phone = models.CharField('电话', max_length=20)
    expertise_areas = models.JSONField('专业领域', default=list)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '律师'
        verbose_name_plural = '律师团队'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name 

class Testimonial(models.Model):
    name = models.CharField('客户姓名', max_length=100)
    title = models.CharField('职位', max_length=100)
    company = models.CharField('公司', max_length=100)
    content = models.TextField('评价内容')
    rating = models.IntegerField('评分', choices=[(i, f"{i}星") for i in range(1, 6)], default=5)
    avatar = models.ImageField('头像', upload_to='testimonials/', null=True, blank=True)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否显示', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '客户评价'
        verbose_name_plural = '客户评价'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.company}" 

class ServicePackage(models.Model):
    name = models.CharField('套餐名称', max_length=100)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '服务套餐'
        verbose_name_plural = '服务套餐'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField('服务类型', max_length=100)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '服务类型'
        verbose_name_plural = '服务类型'
        ordering = ['order']

    def __str__(self):
        return self.name

class ServiceItem(models.Model):
    type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='服务类型')
    title = models.CharField('服务标题', max_length=200)
    content = models.TextField('服务内容')
    description = models.TextField('服务说明')
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '服务项目'
        verbose_name_plural = '服务项目'
        ordering = ['type__order', 'order']

    def __str__(self):
        return f"{self.type.name} - {self.title}"

class ServiceItemPackage(models.Model):
    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE, verbose_name='服务项目')
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务套餐')
    value = models.CharField('服务内容', max_length=100)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '套餐服务内容'
        verbose_name_plural = '套餐服务内容'
        unique_together = ['service_item', 'package']

    def __str__(self):
        return f"{self.package.name} - {self.service_item.title}" 

class FamilyServicePackage(models.Model):
    service_type = models.CharField('服务类型', max_length=100)
    title = models.CharField('服务内容', max_length=200)
    description = models.TextField('服务说明')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '家庭服务套餐'
        verbose_name_plural = '家庭服务套餐'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service_type} - {self.title}"

class EnterpriseServiceType(models.Model):
    """企业服务类型"""
    name = models.CharField('类型名称', max_length=100)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '服务类型'
        verbose_name_plural = '服务类型'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

class EnterpriseServicePackage(models.Model):
    """企业服务套餐"""
    PACKAGE_CHOICES = (
        ('standard', '标准版'),
        ('premium', '高级版'),
        ('deluxe', '豪华版'),
    )
    type = models.CharField('套餐类型', max_length=20, choices=PACKAGE_CHOICES, unique=True)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '服务套餐'
        verbose_name_plural = '服务套餐'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.get_type_display()

class EnterpriseServiceItem(models.Model):
    """企业服务项目"""
    type = models.ForeignKey(EnterpriseServiceType, verbose_name='服务类型', on_delete=models.CASCADE)
    title = models.TextField('服务内容', help_text='支持换行，每行一个服务内容')
    description = models.TextField('服务说明', blank=True)
    supported_packages = models.ManyToManyField(EnterpriseServicePackage, verbose_name='支持的套餐', blank=True)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '企业服务项目'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title 