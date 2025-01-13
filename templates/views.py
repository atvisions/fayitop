from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    # 轮播数据
    hero_slides = [
        {
            'title': '让法务惠普经营',
            'description': '一站式法律服务方案为企业经营保驾护航',
            'button_text': '立即咨询',
            'button_url': 'contact',
            'bg_image': 'images/slides/legal-1.jpg'  # 法律咨询场景
        },
        {
            'title': '成为您身边的智能化法务专家',
            'description': '专业高效的法律服务团队，为您的企业保驾护航',
            'button_text': '了解更多',
            'button_url': 'legal_consultation',
            'bg_image': 'images/slides/legal-2.jpg'  # 科技法务场景
        },
        {
            'title': '专业 · 高效 · 开放 · 共赢',
            'description': '以专业的能力、高效的服务、开放的态度，实现互利共赢',
            'button_text': '服务详情',
            'button_url': 'legal_tools',
            'bg_image': 'images/slides/legal-3.jpg'  # 团队协作场景
        },
        {
            'title': '智能化法务服务平台',
            'description': '运用现代科技，提供便捷高效的法律服务解决方案',
            'button_text': '开始体验',
            'button_url': 'contact',
            'bg_image': 'images/slides/legal-4.jpg'  # 智能科技场景
        }
    ]

    services_list = [
        {
            'title': '合同法律服务',
            'description': '提供各类合同审查、起草、谈判等专业服务'
        },
        {
            'title': '劳动法律服务',
            'description': '处理劳动争议、人事管理等相关法律事务'
        },
        {
            'title': '公司法律服务',
            'description': '企业日常法律顾问、公司治理、股权架构设计'
        },
        {
            'title': '知识产权服务',
            'description': '商标注册、专利申请、知识产权保护'
        }
    ]
    
    cases = [
        {
            'title': '某科技公司劳动争议案件',
            'description': '成功协助企业处理群体性劳动争议，避免重大损失'
        },
        {
            'title': '商业合同纠纷调解',
            'description': '通过调解方式快速解决跨境商业合同纠纷'
        },
        {
            'title': '知识产权保护案例',
            'description': '帮助企业建立完整的知识产权保护体系'
        }
    ]
    
    context = {
        'hero_slides': hero_slides,
        'services': services_list,
        'cases': cases
    }
    return render(request, 'home.html', context)

def legal_consultation(request):
    return render(request, 'services/legal_consultation.html')

def labor_compliance(request):
    return render(request, 'services/labor_compliance.html')

def contract_optimization(request):
    return render(request, 'services/contract_optimization.html')

def debt_management(request):
    return render(request, 'services/debt_management.html')

def intellectual_property(request):
    return render(request, 'services/intellectual_property.html')

def corporate_governance(request):
    return render(request, 'services/corporate_governance.html')

def legal_tools(request):
    return render(request, 'services/legal_tools.html')

def testimonials(request):
    return render(request, 'about/testimonials.html')

def team(request):
    team_members = [
        {
            'name': '张志远',
            'title': '高级合伙人',
            'description': '拥有20年公司法律服务经验，专注于企业并购重组、股权投资等领域。',
            'image': 'images/team/lawyer1.jpg',
            'specialties': ['公司法', '投资并购', '股权架构']
        },
        {
            'name': '李明珠',
            'title': '知识产权部主管',
            'description': '在知识产权保护和商标专利申请方面有丰富经验，曾服务多家科技企业。',
            'image': 'images/team/lawyer2.jpg',
            'specialties': ['知识产权', '商标专利', '技术许可']
        },
        {
            'name': '王建国',
            'title': '劳动法专家',
            'description': '专注于劳动争议解决和人力资源管理，擅长处理复杂劳动纠纷案件。',
            'image': 'images/team/lawyer3.jpg',
            'specialties': ['劳动法', '人事管理', '争议调解']
        },
        {
            'name': '陈雅琳',
            'title': '合规顾问',
            'description': '具有跨国企业合规管理经验，精通境内外监管要求和风险防控。',
            'image': 'images/team/lawyer4.jpg',
            'specialties': ['合规管理', '风险控制', '公司治理']
        },
        {
            'name': '刘泽华',
            'title': '诉讼部主任',
            'description': '资深诉讼律师，在商业纠纷解决和仲裁方面有丰富经验。',
            'image': 'images/team/lawyer5.jpg',
            'specialties': ['商业诉讼', '仲裁调解', '债权债务']
        },
        {
            'name': '赵婷婷',
            'title': '金融法律顾问',
            'description': '专注于金融法律服务，为多家金融机构提供常年法律顾问服务。',
            'image': 'images/team/lawyer6.jpg',
            'specialties': ['金融法', '资产管理', '投资基金']
        }
    ]
    
    context = {
        'team_members': team_members
    }
    return render(request, 'about/team.html', context)

def news(request):
    categories = [
        {'id': 'industry', 'name': '行业动态'},
        {'id': 'company', 'name': '公司新闻'},
        {'id': 'legal', 'name': '法律资讯'},
        {'id': 'case', 'name': '案例分析'}
    ]
    
    news_list = [
        {
            'id': 1,
            'title': '最高法发布新规：关于审理劳动争议案件若干问题的规定',
            'category': 'legal',
            'date': '2024-01-10',
            'thumbnail': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800',
            'summary': '最高人民法院发布关于审理劳动争议案件若干问题的规定，进一步明确劳动争议处理的法律适用标准。',
            'views': 2580
        },
        {
            'id': 2,
            'title': '我司成功举办2024企业法律风险防范研讨会',
            'category': 'company',
            'date': '2024-01-08',
            'thumbnail': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800',
            'summary': '研讨会聚焦企业合规管理、知识产权保护等热点话题，来自各行业的企业代表共同探讨法律风险防范策略。',
            'views': 1860
        },
        {
            'id': 3,
            'title': '人工智能时代的法律服务创新与挑战',
            'category': 'industry',
            'date': '2024-01-05',
            'thumbnail': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800',
            'summary': '随着AI技术的发展，法律服务行业正在经历深刻变革，智能化工具为法律服务带来新的机遇和挑战。',
            'views': 3420
        },
        {
            'id': 4,
            'title': '典型案例解析：某互联网公司商标权纠纷案件',
            'category': 'case',
            'date': '2024-01-03',
            'thumbnail': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800',
            'summary': '通过案例分析，深入探讨互联网企业在商标注册和保护方面需要注意的关键问题。',
            'views': 2150
        },
        {
            'id': 5,
            'title': '新《公司法》修订要点解读',
            'category': 'legal',
            'date': '2024-01-01',
            'thumbnail': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800',
            'summary': '详细解读新修订的《公司法》重要变化，分析对企业经营的影响及应对策略。',
            'views': 4280
        },
        {
            'id': 6,
            'title': '我司与某科技集团达成战略合作',
            'category': 'company',
            'date': '2023-12-28',
            'thumbnail': 'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=800',
            'summary': '双方将在法律科技领域展开深入合作，共同推动法律服务的数字化转型。',
            'views': 1920
        }
    ]
    
    # 获取当前选中的分类
    current_category = request.GET.get('category', '')
    if current_category:
        news_list = [news for news in news_list if news['category'] == current_category]
    
    context = {
        'categories': categories,
        'news_list': news_list,
        'current_category': current_category
    }
    return render(request, 'news/index.html', context)

def contact(request):
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        service = request.POST.get('service')
        message = request.POST.get('message')
        
        try:
            # TODO: 这里添加发送邮件或保存到数据库的逻辑
            
            # 添加成功消息
            messages.success(request, '感谢您的咨询，我们会尽快与您联系！')
            return redirect('contact')
        except Exception as e:
            messages.error(request, '提交失败，请稍后重试或直接联系我们。')
            
    return render(request, 'contact.html') 

def service_packages(request):
    return render(request, 'services/packages.html') 

def services(request):
    services_list = [
        {
            'title': '法律咨询',
            'description': '提供专业的法律咨询服务，解答企业经营过程中遇到的各类法律问题',
            'icon': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
            'image': 'https://images.unsplash.com/photo-1521791055366-0d553872125f?w=800'
        },
        {
            'title': '合同审查',
            'description': '专业的合同审查服务，帮助企业规避合同风险，保护企业权益',
            'icon': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
            'image': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800'
        },
        {
            'title': '劳动法律',
            'description': '处理劳动争议、人事管理等相关法律事务，保障企业和员工权益',
            'icon': 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
            'image': 'https://images.unsplash.com/photo-1521791055366-0d553872125f?w=800'
        },
        {
            'title': '知识产权',
            'description': '提供商标注册、专利申请、知识产权保护等全方位服务',
            'icon': 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z',
            'image': 'https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=800'
        }
    ]
    
    return render(request, 'services/index.html', {'services': services_list}) 