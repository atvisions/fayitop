from django.contrib import admin
from django.utils.html import format_html
from .models import (
    NewsCategory, News, ContactMessage, Lawyer, Testimonial,
    FamilyServicePackage, EnterpriseServicePackage,
    EnterpriseServiceType, EnterpriseServiceItem
)

# 自定义 AdminSite
class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        
        # 创建服务套餐管理分组
        service_package_models = []
        other_models = []
        
        for app in app_list:
            new_models = []
            for model in app['models']:
                model_admin = self._registry.get(model['model'])
                if model_admin and isinstance(model_admin, ServicePackageAdmin):
                    service_package_models.append(model)
                else:
                    new_models.append(model)
            app['models'] = new_models
            if new_models:
                other_models.append(app)
        
        if service_package_models:
            app_list = [{
                'name': '服务套餐管理',
                'app_label': 'service_packages',
                'app_url': '#',
                'has_module_perms': True,
                'models': service_package_models
            }] + other_models
            
        return app_list

# 创建自定义 AdminSite 实例
admin_site = CustomAdminSite(name='admin')

# 服务套餐管理基类
class ServicePackageAdmin(admin.ModelAdmin):
    """服务套餐管理基类"""
    def get_app_label(self):
        return '服务套餐管理'

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order', 'created_at')
    list_editable = ('sort_order',)
    search_fields = ('name',)
    ordering = ('sort_order', '-created_at')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'thumbnail_preview', 'views', 'is_published', 'created_at')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'summary', 'content')
    list_editable = ('is_published',)
    readonly_fields = ('views', 'thumbnail_preview')
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category', 'summary', 'content')
        }),
        ('图片', {
            'fields': ('thumbnail', 'thumbnail_preview')
        }),
        ('发布信息', {
            'fields': ('is_published', 'views')
        })
    )

# 服务套餐管理
@admin.register(FamilyServicePackage)
class FamilyServicePackageAdmin(ServicePackageAdmin):
    """家庭服务套餐管理"""
    list_display = ('service_type', 'title', 'price', 'is_active', 'created_at')
    list_editable = ('price', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('service_type', 'title', 'description')
    fieldsets = (
        (None, {
            'fields': ('service_type', 'title', 'description', 'price', 'is_active')
        }),
    )

@admin.register(EnterpriseServicePackage)
class EnterpriseServicePackageAdmin(ServicePackageAdmin):
    """服务套餐管理"""
    list_display = ['get_type_display', 'price', 'order', 'is_active', 'created_at']
    list_editable = ['price', 'order', 'is_active']
    list_filter = ['is_active', 'created_at']
    fieldsets = [
        (None, {
            'fields': ['type', 'price', 'order', 'is_active']
        })
    ]

@admin.register(EnterpriseServiceType)
class EnterpriseServiceTypeAdmin(ServicePackageAdmin):
    """服务类型管理"""
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active', 'created_at']
    fieldsets = [
        (None, {
            'fields': ['name', 'order', 'is_active']
        })
    ]

@admin.register(EnterpriseServiceItem)
class EnterpriseServiceItemAdmin(ServicePackageAdmin):
    """服务内容管理"""
    list_display = ['title', 'type', 'get_supported_packages', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['type', 'supported_packages', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['supported_packages']
    fieldsets = [
        (None, {
            'fields': ['type', 'title', 'description', 'supported_packages', 'order', 'is_active']
        })
    ]

    def get_supported_packages(self, obj):
        """获取支持的套餐列表"""
        return ', '.join([package.get_type_display() for package in obj.supported_packages.all()])
    get_supported_packages.short_description = '支持的套餐'

# 其他模型管理
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'phone', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'title', 'email', 'phone', 'introduction']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('基本信息', {
            'fields': ['name', 'title', 'image', 'introduction']
        }),
        ('联系方式', {
            'fields': ['email', 'phone']
        }),
        ('专业领域', {
            'fields': ['expertise_areas']
        }),
        ('显示设置', {
            'fields': ['order', 'is_active']
        }),
        ('时间信息', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['expertise_areas'].help_text = '请输入JSON格式的专业领域列表，例如：["商事诉讼", "知识产权", "劳动法"]'
        return form

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'title', 'rating', 'order', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'company', 'title', 'content']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('基本信息', {
            'fields': ['name', 'title', 'company', 'content', 'rating']
        }),
        ('头像', {
            'fields': ['avatar']
        }),
        ('显示设置', {
            'fields': ['order', 'is_active']
        }),
        ('时间信息', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ] 

# 重新注册所有模型到自定义 AdminSite
admin_site.register(NewsCategory, NewsCategoryAdmin)
admin_site.register(News, NewsAdmin)
admin_site.register(FamilyServicePackage, FamilyServicePackageAdmin)
admin_site.register(EnterpriseServicePackage, EnterpriseServicePackageAdmin)
admin_site.register(EnterpriseServiceType, EnterpriseServiceTypeAdmin)
admin_site.register(EnterpriseServiceItem, EnterpriseServiceItemAdmin)
admin_site.register(ContactMessage, ContactMessageAdmin)
admin_site.register(Lawyer, LawyerAdmin)
admin_site.register(Testimonial, TestimonialAdmin) 