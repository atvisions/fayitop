from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
import logging
from django.db.models import Count, Avg
from .models import News, NewsCategory, ContactMessage, Lawyer, Testimonial, ServicePackage, ServiceItem, ServiceItemPackage, FamilyServicePackage, EnterpriseServicePackage, EnterpriseServiceItem, EnterpriseServiceType
from django.views.decorators.http import require_http_methods

logger = logging.getLogger('app')

def index(request):
    try:
        logger.debug('Index view called')
        return render(request, 'home.html')
    except Exception as e:
        logger.exception('Error in index view')
        return HttpResponse(f"Error: {str(e)}", status=500)

def news_list(request):
    return HttpResponse("News List")

def service_packages(request):
    """服务套餐页面"""
    # 获取所有启用的家庭服务套餐
    family_packages = FamilyServicePackage.objects.filter(
        is_active=True
    ).order_by('-created_at')
    
    # 获取所有启用的企业服务套餐，按价格从低到高排序
    enterprise_packages = list(EnterpriseServicePackage.objects.filter(
        is_active=True
    ))
    # 自定义排序：标准版、高级版、豪华版
    package_order = {'standard': 1, 'deluxe': 2, 'premium': 3}
    enterprise_packages.sort(key=lambda x: package_order[x.type.lower()])
    
    # 初始化企业服务数据字典
    enterprise_services = {}
    
    # 获取所有启用的服务类型，按排序字段排序
    service_types = EnterpriseServiceType.objects.filter(
        is_active=True
    ).order_by('order')
    
    # 遍历服务类型
    for service_type in service_types:
        # 获取该类型下的所有启用的服务项目，按排序字段排序
        service_items = EnterpriseServiceItem.objects.filter(
            type=service_type,
            is_active=True
        ).order_by('order')
        
        # 如果该类型下有服务项目
        if service_items.exists():
            # 处理每个服务项目
            items = []
            for item in service_items:
                # 获取该服务项目支持的套餐
                values = {}
                for package in enterprise_packages:  # 使用已排序的套餐列表
                    values[package.type] = '支持' if package in item.supported_packages.all() else '-'
                
                # 将服务项目及其值添加到列表中
                items.append({
                    'title': item.title,
                    'description': item.description,
                    'values': values
                })
            
            # 将该类型下的所有服务项目添加到结果字典中
            enterprise_services[service_type] = items
    
    context = {
        'family_packages': family_packages,
        'enterprise_packages': enterprise_packages,
        'enterprise_services': enterprise_services,
    }
    
    return render(request, 'service-packages.html', context)

def home(request):
    hero_slides = [
        {
            'title': '专业的法律服务团队',
            'description': '为您提供全方位的法律支持和风险防控',
            'button_text': '了解更多',
            'button_url': 'services',
            'bg_image': 'images/slides/legal-1.jpg'
        },
        {
            'title': '丰富的法律实践经验',
            'description': '多年的法律服务经验，为您提供最优质的法律解决方案',
            'button_text': '联系我们',
            'button_url': 'contact',
            'bg_image': 'images/slides/legal-2.jpg'
        },
        {
            'title': '全面的法律服务领域',
            'description': '覆盖商业、知识产权、劳动等多个法律领域',
            'button_text': '服务项目',
            'button_url': 'service_packages',
            'bg_image': 'images/slides/legal-3.jpg'
        }
    ]
    
    # 获取最新的3条用户评价
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    context = {
        'hero_slides': hero_slides,
        'testimonials': testimonials,
    }
    
    return render(request, 'home.html', context)

def contact(request):
    if request.method == 'POST':
        try:
            # 获取表单数据
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            service = request.POST.get('service')
            message = request.POST.get('message')
            
            # 创建新的咨询记录
            ContactMessage.objects.create(
                name=name,
                phone=phone,
                email=email,
                service=service,
                message=message
            )
            
            # 返回成功响应
            return JsonResponse({
                'status': 'success',
                'message': '您的咨询已提交成功，我们会尽快与您联系！'
            })
            
        except Exception as e:
            # 返回错误响应
            return JsonResponse({
                'status': 'error',
                'message': '提交失败，请稍后重试或直接联系我们。'
            }, status=400)
    
    return render(request, 'contact.html')

def services(request):
    services = {
        'business': {
            'id': 'business-law',
            'title': '商业法律服务',
            'description': '为企业提供全面的法律咨询和风险防控服务，保障企业合法权益。',
            'image': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800',
            'icon': '<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"></path></svg>',
            'features': [
                '公司设立与变更',
                '合同审查与管理',
                '知识产权保护',
                '劳动人事管理',
                '法律风险防控'
            ]
        },
        'intellectual': {
            'id': 'intellectual-property',
            'title': '知识产权服务',
            'description': '专业的知识产权保护服务，帮助企业建立完善的知识产权管理体系。',
            'image': 'https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?auto=format&fit=crop&w=800',
            'icon': '<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>',
            'features': [
                '商标注册与保护',
                '专利申请与维护',
                '著作权登记',
                '知识产权诉讼',
                '许可与转让'
            ]
        },
        'litigation': {
            'id': 'litigation',
            'title': '诉讼仲裁服务',
            'description': '提供专业的诉讼代理和仲裁服务，维护当事人合法权益。',
            'image': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800',
            'icon': '<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"></path></svg>',
            'features': [
                '民商事诉讼',
                '行政诉讼',
                '仲裁代理',
                '执行程序',
                '调解谈判'
            ]
        }
    }
    return render(request, 'services.html', {'services': services})

def team(request):
    # 获取所有启用的律师，按排序和创建时间排序
    lawyers = Lawyer.objects.filter(is_active=True).order_by('order', '-created_at')
    return render(request, 'about/team.html', {
        'lawyers': lawyers
    })

def testimonials(request):
    # 获取所有启用的评价，按排序和创建时间排序
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order', '-created_at')
    
    # 计算总体统计数据
    total_testimonials = testimonials.count()
    avg_rating = testimonials.aggregate(Avg('rating'))['rating__avg'] or 0
    satisfied_count = testimonials.filter(rating__gte=4).count()
    satisfaction_rate = int((satisfied_count / total_testimonials * 100) if total_testimonials > 0 else 0)
    
    context = {
        'testimonials': testimonials,
        'stats': {
            'satisfaction_rate': satisfaction_rate,
            'total_clients': 1500,  # 这个数字可以根据实际情况调整
            'avg_rating': round(avg_rating, 1),
            'total_testimonials': total_testimonials
        }
    }
    return render(request, 'about/testimonials.html', context)

def news(request):
    # 获取所有分类
    categories = NewsCategory.objects.all()
    
    # 获取当前分类
    current_category = request.GET.get('category', 'all')
    current_category_name = '全部'
    
    # 获取新闻列表，只显示已发布的
    news_list = News.objects.filter(is_published=True)
    
    # 如果选择了特定分类
    if current_category != 'all':
        category = NewsCategory.objects.get(id=current_category)
        current_category_name = category.name
        news_list = news_list.filter(category_id=current_category)
    
    # 准备分类数据，包含文章数量
    category_data = []
    # 添加"全部"选项
    total_count = News.objects.filter(is_published=True).count()
    category_data.append({
        'id': 'all',
        'name': '全部',
        'count': total_count
    })
    
    # 添加其他分类
    for category in categories:
        count = News.objects.filter(
            category=category,
            is_published=True
        ).count()
        category_data.append({
            'id': str(category.id),
            'name': category.name,
            'count': count
        })
    
    return render(request, 'news/news_list.html', {
        'news_list': news_list,
        'categories': category_data,
        'current_category': current_category,
        'current_category_name': current_category_name
    })

def news_detail(request, news_id):
    # 获取新闻详情
    news = get_object_or_404(News, id=news_id, is_published=True)
    
    # 增加浏览量
    news.views += 1
    news.save()
    
    return render(request, 'news/detail.html', {
        'news': news,
    }) 