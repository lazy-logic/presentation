"""
Modern Employer Dashboard - AjuraConnect
A clean, professional dashboard for employers to manage job postings and candidates.
"""
from nicegui import ui, app
from app.services.api_service import api_service
from app.services.auth_utils import get_current_user, is_authenticated
from app.components.header import header
from app.components.footer import footer
import asyncio

def modern_employer_dashboard():
    """A modern employer dashboard with a clean UI/UX, no icons."""
    
    # Check authentication
    if not is_authenticated():
        ui.notify("Please login to access the dashboard", type='negative')
        ui.navigate.to('/login')
        return
    
    user = get_current_user()
    if user.get('role') not in ['EMPLOYER', 'ADMIN']:
        ui.notify("You are not authorized to view this page.", type='negative')
        # Redirect to their appropriate dashboard
        if user.get('role') == 'TRAINEE':
            ui.navigate.to('/candidates/dashboard')
        else:
            ui.navigate.to('/')
        return

    user_id = user.get('id')
    token = app.storage.user.get('token')
    
    if token:
        api_service.set_auth_token(token)
    else:
        print("[EMPLOYER_DASHBOARD] WARNING: No token found!")
    
    print(f"[EMPLOYER_DASHBOARD] Loading dashboard for user: {user.get('email')}")
    
    # Fetch employer profile data
    employer_profile = user.get('employerProfile', {})
    company_name = employer_profile.get('companyName', 'Your Company')
    company_logo = employer_profile.get('logoUrl', '')
    
    # State management
    dashboard_data = {
        'job_postings': [],
        'applications': [],
        'candidates_count': 0,
        'active_postings': 0,
        'pending_applications': 0
    }
    # Default to session-stored postings if present, else demo data (ensures overview table is populated)
    try:
        dashboard_data['job_postings'] = app.storage.user.get('job_postings', []) or []
        if not dashboard_data['job_postings']:
            dashboard_data['job_postings'] = [
                {
                    'id': 'demo-1',
                    'title': 'Software Engineer',
                    'location': 'Lagos, NG',
                    'type': 'Full-time',
                    'experienceLevel': 'Mid Level (2-5 years)',
                    'status': 'active',
                    'applications': 14,
                    'postedDate': '2025-10-15'
                },
                {
                    'id': 'demo-2',
                    'title': 'Data Analyst',
                    'location': 'Accra, GH',
                    'type': 'Contract',
                    'experienceLevel': 'Entry Level (0-2 years)',
                    'status': 'active',
                    'applications': 9,
                    'postedDate': '2025-10-14'
                },
                {
                    'id': 'demo-3',
                    'title': 'UI/UX Designer',
                    'location': 'Remote',
                    'type': 'Full-time',
                    'experienceLevel': 'Senior Level (5+ years)',
                    'status': 'closed',
                    'applications': 22,
                    'postedDate': '2025-10-10'
                },
            ]
        dashboard_data['active_postings'] = len([j for j in dashboard_data['job_postings'] if j.get('status') == 'active'])
        dashboard_data['pending_applications'] = sum(j.get('applications', 0) for j in dashboard_data['job_postings'])
    except Exception:
        pass
    
    async def fetch_dashboard_data():
        """Fetch all dashboard data from API."""
        try:
            # Fetch job postings
            job_response = api_service.get('/api/jobs')
            if job_response and isinstance(job_response, list):
                dashboard_data['job_postings'] = job_response
                dashboard_data['active_postings'] = len([j for j in job_response if j.get('status') == 'active'])
            
            # Fetch applications (if endpoint exists)
            # app_response = api_service.get('/api/applications')
            # if app_response:
            #     dashboard_data['applications'] = app_response
            
            ui.notify("Dashboard data loaded", type='positive')
        except Exception as e:
            print(f"Error fetching dashboard data: {str(e)}")
    
    header('/employers/dashboard')
    
    # Professional Modern Dashboard Styles (from institution dashboard)
    ui.add_head_html('''
    <link href="https://cdn.tailwindcss.com" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            box-sizing: border-box;
        }
        
        body {
            background: #FFFFFF;
            font-size: 14px;
            line-height: 1.5;
        }
        
        /* Professional Card System */
        .pro-card {
            background: white;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            padding: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .pro-card:hover {
            box-shadow: 0 3px 10px rgba(0, 85, 184, 0.08);
            transform: translateY(-1px);
        }
        
        /* Metric Cards - Dark Blue Analytics Cards */
        .metric-card {
            background: linear-gradient(135deg, #003d82 0%, #002855 100%);
            border-radius: 20px;
            border: 1px solid #004494;
            padding: 28px;
            margin: 8px 0;
            margin-left: 15px;
            margin-right: 15px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 61, 130, 0.3);
            color: white;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 85, 184, 0.2) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        .metric-card:hover {
            border-color: #0055B8 !important;
            box-shadow: 0 8px 20px rgba(0, 85, 184, 0.4) !important;
            transform: translateY(-4px);
        }
        
        /* White text for metric cards */
        .metric-card * {
            color: white !important;
        }
        
        .metric-value {
            font-size: 20px;
            font-weight: 800;
            color: white !important;
            line-height: 1;
            margin: 6px 0 4px 0;
        }
        
        .metric-label {
            font-size: 10px;
            color: rgba(255, 255, 255, 0.8) !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-trend {
            font-size: 11px;
            color: #4ade80 !important;
            font-weight: 600;
            margin-top: 4px;
        }
        
        /* Dark Sidebar Design */
        .pro-sidebar {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border-right: 1px solid #334155;
            height: 100vh;
            position: fixed;
            left: 0;
            top: 64px;
            width: 280px;
            z-index: 1001;
            transition: transform 0.3s ease;
        }
        
        /* Mobile Responsive Styles */
        @media (max-width: 1023px) {
            .pro-sidebar {
                transform: translateX(-100%);
                box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
            }
            
            .pro-sidebar.mobile-open {
                transform: translateX(0);
            }
            
            .dashboard-main-content {
                margin-left: 0 !important;
                padding: 16px !important;
            }
            
            .metric-card {
                margin: 8px 0 !important;
            }
            
            .metric-value {
                font-size: 18px !important;
            }
            
            .pro-card {
                padding: 12px !important;
            }
            
            /* Stack cards vertically on mobile */
            .grid {
                grid-template-columns: 1fr !important;
            }
            
            /* Mobile hamburger menu button */
            .mobile-hamburger {
                display: flex !important;
                position: fixed;
                top: 72px;
                left: 16px;
                width: 44px;
                height: 44px;
                background: #0055B8;
                border-radius: 8px;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 8px rgba(0, 85, 184, 0.3);
                z-index: 999;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .mobile-hamburger:hover {
                background: #004494;
                box-shadow: 0 4px 12px rgba(0, 85, 184, 0.4);
            }
            
            .mobile-hamburger .material-icons {
                color: white;
                font-size: 24px;
            }
        }
        
        @media (min-width: 1024px) {
            .mobile-hamburger {
                display: none !important;
            }
            
            .dashboard-main-content {
                margin-left: 280px;
            }
        }
        
        /* Mobile overlay */
        .mobile-overlay {
            display: none;
            position: fixed;
            top: 64px;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
        }
        
        .mobile-overlay.active {
            display: block;
        }
        
        /* Dark Navigation */
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            width: 100%;
            padding: 12px 16px;
            margin: 4px 0;
            border-radius: 10px;
            text-align: left;
            transition: all 0.2s ease;
            background: transparent;
            border: none;
            font-size: 14px;
            font-weight: 500;
            color: #94a3b8;
            cursor: pointer;
        }
        
        .nav-item:hover {
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff !important;
        }
        
        .nav-item.active {
            background: linear-gradient(135deg, #0055B8 0%, #003d82 100%) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(0, 85, 184, 0.4) !important;
        }
        
        /* Professional Buttons */
        .pro-btn-primary, .pro-btn-primary * {
            background: linear-gradient(135deg, #0055B8 0%, #003d82 100%) !important;
            color: white !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.3s ease !important;
            font-size: 13px !important;
            box-shadow: 0 2px 8px rgba(0, 85, 184, 0.2) !important;
        }
        
        .pro-btn-primary:hover, .pro-btn-primary:hover * {
            box-shadow: 0 4px 12px rgba(0, 85, 184, 0.3) !important;
            transform: translateY(-1px) !important;
            background: linear-gradient(135deg, #0055B8 0%, #003d82 100%) !important;
            color: white !important;
        }
        
        .pro-btn-secondary, .pro-btn-secondary * {
            background: white !important;
            color: #0055B8 !important;
            padding: 7px 14px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: 2px solid #e2e8f0 !important;
            transition: all 0.3s ease !important;
            font-size: 12px !important;
        }
        
        .pro-btn-secondary:hover, .pro-btn-secondary:hover * {
            background: #f8fafc !important;
            border-color: #0055B8 !important;
            transform: translateY(-1px) !important;
            color: #0055B8 !important;
        }
        
        /* Force all buttons to follow brand profile */
        button, .q-btn {
            font-family: 'Inter', sans-serif !important;
        }
        
        button.pro-btn-primary, .q-btn.pro-btn-primary {
            background: linear-gradient(135deg, #0055B8 0%, #003d82 100%) !important;
            color: white !important;
            border: none !important;
        }
        
        button.pro-btn-secondary, .q-btn.pro-btn-secondary {
            background: white !important;
            color: #0055B8 !important;
            border: 2px solid #e2e8f0 !important;
        }
        
        /* Action Buttons - Redesigned */
        .action-button-primary {
            background: linear-gradient(135deg, #0055B8 0%, #003d82 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 85, 184, 0.25);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex: 1;
            min-width: 180px;
        }
        
        .action-button-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 85, 184, 0.35);
        }
        
        .action-button-primary * {
            color: white !important;
        }
        
        .action-button-secondary {
            background: white;
            color: #0055B8;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid #e2e8f0;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex: 1;
            min-width: 180px;
        }
        
        .action-button-secondary:hover {
            background: #f8fafc;
            border-color: #0055B8;
            transform: translateY(-2px);
            box-shadow: 0 2px 8px rgba(0, 85, 184, 0.15);
        }
        
        .action-button-secondary * {
            color: #0055B8 !important;
        }
        
        @media (max-width: 768px) {
            .action-button-primary,
            .action-button-secondary {
                flex: 1 1 100%;
                min-width: 100%;
            }
        }
        
        /* Section Header */
        .section-header {
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .section-title {
            font-size: 20px;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.2;
        }
        
        .section-subtitle {
            font-size: 13px;
            color: #64748b;
            margin-top: 3px;
        }

        /* ==========================
           Table Brand Enforcement
           ========================== */
        table, .q-table, .q-table * {
            font-family: 'Inter', sans-serif !important;
            color: #1A1A1A !important;
        }
        .q-table, table {
            background: #FFFFFF !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }
        .q-table thead tr, thead tr {
            background: #f8fafc !important;
            border-bottom: 2px solid #e2e8f0 !important;
        }
        .q-th, thead th {
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            font-weight: 700 !important;
            font-size: 11px !important;
            color: #475569 !important;
            padding: 10px 12px !important;
        }
        .q-td, tbody td {
            font-size: 13px !important;
            color: #334155 !important;
            padding: 12px !important;
            border-bottom: 1px solid #f1f5f9 !important;
        }
        .q-tr:hover, tbody tr:hover { background: #f8fafc !important; }
        tbody tr:last-child .q-td, tbody tr:last-child td { border-bottom: none !important; }
        .q-table a, table a { color: #0055B8 !important; text-decoration: none !important; }
        .q-table a:hover, table a:hover { text-decoration: underline !important; }
        .q-table .q-btn, table .q-btn { color: #0055B8 !important; }
        .q-table__bottom, .q-table__separator { border-color: #e2e8f0 !important; }
        
        /* Table Responsive - Horizontal Scroll */
        .table-container {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        table {
            min-width: 600px;
            width: 100%;
        }
        
        /* Overview Table - More elegant spacing */
        .overview-table th {
            background: #f8fafc;
            padding: 14px 16px;
            text-align: left;
            font-size: 11px;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .overview-table td {
            padding: 18px 16px;
            border-bottom: 1px solid #f1f5f9;
            font-size: 13px;
            color: #334155;
        }
        
        .overview-table tr:hover {
            background: #fafbfc;
        }
        
        .overview-table tr:last-child td {
            border-bottom: none;
        }
        
        /* Grid Layouts */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .content-grid {
            display: grid;
            gap: 14px;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
    ''')
    
    # State management
    active_section = {'current': 'overview'}
    employer_data = {'profile': None}
    postings_state = {
        'sort_by': 'Posted',  # Title | Location | Type | Experience | Status | Applications | Posted
        'sort_dir': 'desc',   # asc | desc
        'status_filter': 'All',  # All | active | closed
        'type_filter': 'All',    # All | Full-time | Part-time | Contract | Internship
        'page': 1,
        'page_size': 10,
    }
    applications_state = {
        'sort_by': 'Applied On',  # Applicant | Job | Status | Applied On
        'sort_dir': 'desc',
        'status_filter': 'All',   # All | Under Review | Interview | Shortlisted | Rejected | Hired
        'page': 1,
        'page_size': 10,
    }

    # Professional Dashboard Layout
    with ui.row().classes('w-full').style('min-height: 100vh; gap: 0; margin: 0; padding-top: 64px;'):
        # Professional Sidebar
        sidebar = ui.column().classes('pro-sidebar').style('width: 260px; padding: 24px 20px; position: fixed; left: 0; top: 64px; bottom: 64px; overflow-y: auto; z-index: 40;')
        with sidebar:
            # Brand Section
            with ui.column().classes('mb-8'):
                # User Profile Card
                with ui.card().style('background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 16px; border-radius: 12px; backdrop-filter: blur(10px);'):
                    with ui.row().classes('items-center gap-3'):
                        # Company logo or initials
                        if company_logo:
                            with ui.element('div').style('width: 40px; height: 40px; border-radius: 50%; overflow: hidden; border: 2px solid rgba(255, 255, 255, 0.2); box-shadow: 0 2px 8px rgba(0, 85, 184, 0.3);'):
                                ui.image(company_logo).style('width: 100%; height: 100%; object-fit: cover;')
                        else:
                            initials = ''.join([n[0].upper() for n in company_name.split()[:2]])
                            with ui.element('div').style('width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #0055B8 0%, #003d82 100%); display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0, 85, 184, 0.3);'):
                                ui.label(initials).style('color: white; font-weight: 700; font-size: 16px;')
                        
                        with ui.column().classes('gap-0 flex-1'):
                            ui.label(company_name).style('font-size: 14px; font-weight: 700; color: #ffffff; line-height: 1;')
                            ui.label(user.get('email', '')).style('font-size: 11px; color: #94a3b8; margin-top: 4px;')
            
            ui.separator().style('margin: 20px 0; background: rgba(255, 255, 255, 0.1);')
            
            # Navigation Menu
            with ui.column().classes('flex-1').style('gap: 4px;'):
                menu_items = [
                    ('overview', 'dashboard', 'Dashboard'),
                    ('postings', 'work', 'Job Postings'),
                    ('applications', 'assignment', 'Applications'),
                    ('candidates', 'group', 'Candidates'),
                    ('company', 'business', 'Company Profile'),
                    ('settings', 'settings', 'Settings'),
                ]
                
                menu_buttons = {}
                
                # Define close function before menu handlers
                def close_mobile_menu():
                    sidebar.classes(remove='mobile-open')
                
                def create_nav_handler(section):
                    def handler():
                        active_section['current'] = section
                        for sec, btn_el in menu_buttons.items():
                            btn_el.classes(remove='active', add='')
                        menu_buttons[section].classes(add='active')
                        content_area.clear()
                        with content_area:
                            render_section(section)
                        # Auto-hide sidebar on mobile after clicking menu item
                        close_mobile_menu()
                    return handler
                
                for section, icon, label in menu_items:
                    is_active = section == active_section['current']
                    nav_el = ui.element('div').classes(f'nav-item {"active" if is_active else ""}')
                    nav_el.on('click', create_nav_handler(section))
                    with nav_el:
                        ui.icon(icon, size='20px')
                        ui.label(label)
                    menu_buttons[section] = nav_el
            
            ui.separator().style('margin: 20px 0; background: rgba(255, 255, 255, 0.1);')
            
            def logout_handler():
                from app.services.auth_utils import logout
                logout()
            
            logout_btn = ui.element('div').classes('nav-item')
            logout_btn.on('click', logout_handler)
            with logout_btn:
                ui.icon('logout', size='20px')
                ui.label('Logout')

        # Main Content Area
        content_area = ui.column().classes('dashboard-main-content').style('flex: 1; padding: 32px; margin-top: 64px; min-height: calc(100vh - 128px);')
        
        # Mobile hamburger menu button (top-left corner)
        mobile_hamburger = ui.element('div').classes('mobile-hamburger')
        with mobile_hamburger:
            ui.icon('menu')
        
        # Toggle functionality
        def toggle_mobile_menu():
            sidebar.classes(toggle='mobile-open')
        
        mobile_hamburger.on('click', toggle_mobile_menu)
        
        def navigate_to_section(section):
            """Navigate to a different section."""
            active_section['current'] = section
            for sec, btn_el in menu_buttons.items():
                btn_el.classes(remove='active', add='')
            menu_buttons[section].classes(add='active')
            content_area.clear()
            with content_area:
                render_section(section)
        
        def render_section(section):
            """Render content based on active section."""
            with ui.element('div').classes('fade-in'):
                if section == 'overview':
                    render_overview()
                elif section == 'postings':
                    render_job_postings()
                elif section == 'applications':
                    render_applications()
                elif section == 'candidates':
                    render_candidates()
                elif section == 'company':
                    render_company_profile()
                elif section == 'settings':
                    render_settings()
        
        def render_overview():
            """Render the overview dashboard section."""
            # Welcome Header
            with ui.row().classes('items-center justify-between w-full').style('margin-bottom: 20px;'):
                with ui.column().classes('gap-1'):
                    ui.label(f'Welcome Back, {user.get("name", "ABC Trust")}!').classes('section-title')
                    ui.label('Here\'s what\'s happening with your company today').classes('section-subtitle')
            
            # Metrics Grid with Dark Blue Cards
            with ui.element('div').classes('stats-grid'):
                metrics = [
                    ('Active Job Postings', dashboard_data['active_postings'], 'work', '#0055B8', '+12% from last month'),
                    ('Total Applications', dashboard_data['pending_applications'], 'assignment', '#10b981', '+8% from last month'),
                    ('Candidates', dashboard_data['candidates_count'], 'group', '#f59e0b', '5 new this week'),
                    ('Response Rate', '85%', 'trending_up', '#8b5cf6', '+3% improvement'),
                ]
                
                for label, value, icon, color, trend in metrics:
                    with ui.card().classes('metric-card'):
                        with ui.row().classes('items-start justify-between w-full'):
                            with ui.column().classes('gap-0 flex-1'):
                                ui.label(label).classes('metric-label')
                                ui.label(str(value)).classes('metric-value').style(f'color: {color} !important;')
                                ui.label(trend).classes('metric-trend')
                            ui.icon(icon, size='24px').style(f'color: {color} !important; opacity: 0.3;')
            
            # Recent Job Postings Section
            with ui.card().classes('pro-card').style('margin-top: 8px;'):
                with ui.row().classes('items-center justify-between w-full').style('margin-bottom: 16px;'):
                    with ui.column().classes('gap-0'):
                        ui.label('Recent Job Postings').style('font-size: 16px; font-weight: 700; color: #0f172a;')
                        ui.label(f'{dashboard_data["active_postings"]} active postings').style('font-size: 11px; color: #64748b;')
                
                # Job Postings Overview Table
                if dashboard_data['job_postings']:
                    with ui.element('div').classes('table-container'):
                        with ui.element('table').classes('overview-table'):
                            with ui.element('thead'):
                                with ui.element('tr'):
                                    for h in ['Title', 'Location', 'Type', 'Status', 'Applications', 'Posted']:
                                        with ui.element('th'):
                                            ui.label(h)
                            with ui.element('tbody'):
                                for job in dashboard_data['job_postings'][:5]:
                                    with ui.element('tr'):
                                        with ui.element('td'):
                                            ui.label(job.get('title', 'Job Title'))
                                        with ui.element('td'):
                                            ui.label(job.get('location', 'Location'))
                                        with ui.element('td'):
                                            ui.label(job.get('type', 'Full-time'))
                                        with ui.element('td'):
                                            ui.label((job.get('status') or 'active').upper())
                                        with ui.element('td'):
                                            ui.label(str(job.get('applications', 0)))
                                        with ui.element('td'):
                                            ui.label(job.get('postedDate', ''))
                else:
                    with ui.column().classes('items-center py-12 gap-4'):
                        ui.label('No job postings yet').classes('text-gray-500 text-lg')
                        ui.button('Create Your First Job Posting', 
                                 on_click=lambda: navigate_to_section('postings')).classes('btn-primary')
            
            # Quick Actions
            with ui.card().classes('pro-card').style('margin-top: 16px;'):
                ui.label('Quick Actions').style('font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 16px;')
                
                # Action buttons with icons
                with ui.row().classes('gap-3 w-full').style('flex-wrap: wrap;'):
                    # Post a New Job - Primary Action
                    with ui.element('div').classes('action-button-primary').on('click', lambda: navigate_to_section('postings')):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('add_circle', size='20px')
                            ui.label('Post a New Job')
                    
                    # Browse Candidates
                    with ui.element('div').classes('action-button-secondary').on('click', lambda: navigate_to_section('candidates')):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('group', size='20px')
                            ui.label('Browse Candidates')
                    
                    # Update Company Profile
                    with ui.element('div').classes('action-button-secondary').on('click', lambda: ui.navigate.to('/employer/onboarding/profile')):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('business', size='20px')
                            ui.label('Company Profile')
        
        def render_job_postings():
            """Render job postings section."""
            # State for showing create form
            show_create_form = {'visible': False}
            
            # Get jobs from session storage
            posted_jobs = app.storage.user.get('job_postings', [])
            if not posted_jobs:
                posted_jobs = [
                    {
                        'id': 'demo-1',
                        'title': 'Software Engineer',
                        'location': 'Lagos, NG',
                        'type': 'Full-time',
                        'experienceLevel': 'Mid Level (2-5 years)',
                        'status': 'active',
                        'applications': 14,
                        'postedDate': '2025-10-15'
                    },
                    {
                        'id': 'demo-2',
                        'title': 'Data Analyst',
                        'location': 'Accra, GH',
                        'type': 'Contract',
                        'experienceLevel': 'Entry Level (0-2 years)',
                        'status': 'active',
                        'applications': 9,
                        'postedDate': '2025-10-14'
                    },
                    {
                        'id': 'demo-3',
                        'title': 'UI/UX Designer',
                        'location': 'Remote',
                        'type': 'Full-time',
                        'experienceLevel': 'Senior Level (5+ years)',
                        'status': 'closed',
                        'applications': 22,
                        'postedDate': '2025-10-10'
                    },
                ]
            
            def toggle_create_form():
                show_create_form['visible'] = not show_create_form['visible']
                navigate_to_section('postings')
            
            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label('Job Postings').style('font-size: 20px; font-weight: 800; color: #0f172a;')
                # Brand-compliant action button
                with ui.element('div').classes('action-button-primary').on('click', toggle_create_form):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('add_circle' if not show_create_form['visible'] else 'list', size='20px')
                        ui.label('Create New Job' if not show_create_form['visible'] else 'View Job List')
            
            # Show create form if visible
            if show_create_form['visible']:
                render_create_job_form(toggle_create_form)
                return

            # Filters and sort controls
            with ui.row().classes('w-full items-center justify-between mb-4'):
                with ui.row().classes('gap-3'):
                    status_options = ['All', 'active', 'closed']
                    type_options = ['All', 'Full-time', 'Part-time', 'Contract', 'Internship']
                    sort_options = ['Title', 'Location', 'Type', 'Experience', 'Status', 'Applications', 'Posted']
                    ui.select(status_options, value=postings_state['status_filter'], label='Status')\
                        .props('outlined dense').on('update:model-value', lambda e: (postings_state.update({'status_filter': e.value, 'page': 1}), navigate_to_section('postings')))
                    ui.select(type_options, value=postings_state['type_filter'], label='Type')\
                        .props('outlined dense').on('update:model-value', lambda e: (postings_state.update({'type_filter': e.value, 'page': 1}), navigate_to_section('postings')))
                    ui.select(sort_options, value=postings_state['sort_by'], label='Sort by')\
                        .props('outlined dense').on('update:model-value', lambda e: (postings_state.update({'sort_by': e.value}), navigate_to_section('postings')))
                    ui.select(['asc','desc'], value=postings_state['sort_dir'], label='Direction')\
                        .props('outlined dense').on('update:model-value', lambda e: (postings_state.update({'sort_dir': e.value}), navigate_to_section('postings')))
                with ui.row().classes('gap-3'):
                    ui.select([10, 20, 50], value=postings_state['page_size'], label='Page size')\
                        .props('outlined dense').on('update:model-value', lambda e: (postings_state.update({'page_size': int(e.value), 'page': 1}), navigate_to_section('postings')))

            # Apply filters
            filtered = posted_jobs
            if postings_state['status_filter'] != 'All':
                filtered = [j for j in filtered if (j.get('status') or '').lower() == postings_state['status_filter'].lower()]
            if postings_state['type_filter'] != 'All':
                filtered = [j for j in filtered if (j.get('type') or '') == postings_state['type_filter']]

            # Apply sorting
            key = postings_state['sort_by']
            reverse = postings_state['sort_dir'] == 'desc'
            def sort_key(j):
                if key == 'Applications':
                    return j.get('applications', 0)
                if key == 'Posted':
                    return j.get('postedDate', '')
                if key == 'Experience':
                    return j.get('experienceLevel', '')
                return (j.get(key.lower(), '') if key in ['Title','Location','Type','Status'] else '')
            try:
                filtered = sorted(filtered, key=sort_key, reverse=reverse)
            except Exception:
                pass

            # Pagination
            total = len(filtered)
            page_size = int(postings_state['page_size'])
            total_pages = max(1, (total + page_size - 1) // page_size)
            postings_state['page'] = min(max(1, postings_state['page']), total_pages)
            start = (postings_state['page'] - 1) * page_size
            page_rows = filtered[start:start+page_size]
            
            if page_rows:
                # Render as a brand-styled table
                with ui.card().classes('glass-card p-0'):
                    with ui.element('div').classes('table-container'):
                        with ui.element('table').classes('w-full'):
                            # Table Header
                            with ui.element('thead'):
                                with ui.element('tr'):
                                    for h in ['Title', 'Location', 'Type', 'Experience', 'Status', 'Applications', 'Posted', 'Actions']:
                                        with ui.element('th'):
                                            ui.label(h)
                            # Table Body
                            with ui.element('tbody'):
                                for job in page_rows:
                                    with ui.element('tr'):
                                        with ui.element('td'):
                                            ui.label(job.get('title', 'Job Title'))
                                        with ui.element('td'):
                                            ui.label(job.get('location', 'Location'))
                                        with ui.element('td'):
                                            ui.label(job.get('type', 'Full-time'))
                                        with ui.element('td'):
                                            ui.label(job.get('experienceLevel', 'Entry Level'))
                                        with ui.element('td'):
                                            ui.label((job.get('status') or 'active').upper())
                                        with ui.element('td'):
                                            ui.label(str(job.get('applications', 0)))
                                        with ui.element('td'):
                                            ui.label(job.get('postedDate', ''))
                                        with ui.element('td'):
                                            with ui.row().classes('gap-2'):
                                                ui.button('View', on_click=lambda j=job: ui.notify(f"Viewing {j.get('title')}", type='info')).props('flat size=sm')
                                                ui.button('Edit', on_click=lambda j=job: ui.notify(f"Edit feature coming soon for {j.get('title')}", type='info')).props('flat size=sm')
                                                ui.button('Close', on_click=lambda j=job: close_job_posting(j.get('id'))).props('flat size=sm color=negative')
                # Pagination controls
                with ui.row().classes('justify-end items-center gap-3 mt-3'):
                    ui.button('Prev', on_click=lambda: (postings_state.update({'page': max(1, postings_state['page']-1)}), navigate_to_section('postings'))).props('outline size=sm')
                    ui.label(f"Page {postings_state['page']} of {total_pages}").classes('text-sm text-gray-600')
                    ui.button('Next', on_click=lambda: (postings_state.update({'page': min(total_pages, postings_state['page']+1)}), navigate_to_section('postings'))).props('outline size=sm')
            else:
                with ui.column().classes('items-center py-16 gap-4'):
                    ui.label('No job postings yet').style('font-size: 18px; color: #64748b; font-weight: 600;')
                    ui.label('Create your first job posting to start attracting candidates').style('font-size: 14px; color: #94a3b8;')
                    # Brand-compliant action button
                    with ui.element('div').classes('action-button-primary').on('click', toggle_create_form).style('margin-top: 16px;'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('add_circle', size='20px')
                            ui.label('Create Job Posting')
        
        def close_job_posting(job_id):
            """Close/deactivate a job posting."""
            jobs = app.storage.user.get('job_postings', [])
            for job in jobs:
                if job.get('id') == job_id:
                    job['status'] = 'closed'
                    app.storage.user['job_postings'] = jobs
                    ui.notify(f"Job posting '{job.get('title')}' has been closed", type='positive')
                    # Refresh the section
                    navigate_to_section('postings')
                    break
        
        def render_create_job_form(on_cancel):
            """Render inline job creation form."""
            from datetime import datetime
            
            job_data = {
                'title': '',
                'location': '',
                'type': 'Full-time',
                'experienceLevel': 'Entry Level (0-2 years)',
                'description': '',
                'requirements': '',
                'salary': '',
            }
            
            def save_job():
                if not job_data['title']:
                    ui.notify('Job title is required', type='negative')
                    return
                if not job_data['location']:
                    ui.notify('Location is required', type='negative')
                    return
                
                # Create new job posting
                import uuid
                new_job = {
                    'id': str(uuid.uuid4())[:8],
                    'title': job_data['title'],
                    'location': job_data['location'],
                    'type': job_data['type'],
                    'experienceLevel': job_data['experienceLevel'],
                    'description': job_data['description'],
                    'requirements': job_data['requirements'],
                    'salary': job_data['salary'],
                    'status': 'active',
                    'applications': 0,
                    'postedDate': datetime.now().strftime('%Y-%m-%d')
                }
                
                # Save to storage
                jobs = app.storage.user.get('job_postings', [])
                jobs.append(new_job)
                app.storage.user['job_postings'] = jobs
                
                ui.notify(f"Job posting '{job_data['title']}' created successfully!", type='positive')
                navigate_to_section('postings')
            
            with ui.card().classes('glass-card'):
                ui.label('Create New Job Posting').classes('text-2xl font-bold mb-4')
                
                with ui.column().classes('w-full gap-4'):
                    ui.input('Job Title', placeholder='e.g., Senior Software Engineer').classes('w-full').props('outlined').bind_value(job_data, 'title')
                    ui.input('Location', placeholder='e.g., Lagos, Nigeria or Remote').classes('w-full').props('outlined').bind_value(job_data, 'location')
                    
                    with ui.row().classes('w-full gap-4'):
                        ui.select(['Full-time', 'Part-time', 'Contract', 'Internship'], label='Job Type', value='Full-time').classes('flex-1').props('outlined').bind_value(job_data, 'type')
                        ui.select(['Entry Level (0-2 years)', 'Mid Level (2-5 years)', 'Senior Level (5+ years)', 'Executive'], label='Experience Level', value='Entry Level (0-2 years)').classes('flex-1').props('outlined').bind_value(job_data, 'experienceLevel')
                    
                    ui.input('Salary Range (Optional)', placeholder='e.g., $50,000 - $70,000').classes('w-full').props('outlined').bind_value(job_data, 'salary')
                    ui.textarea('Job Description', placeholder='Describe the role, responsibilities, and what the candidate will be doing...').classes('w-full').props('outlined rows=4').bind_value(job_data, 'description')
                    ui.textarea('Requirements', placeholder='List the required skills, qualifications, and experience...').classes('w-full').props('outlined rows=4').bind_value(job_data, 'requirements')
                    
                    with ui.row().classes('w-full justify-end gap-3 mt-4'):
                        ui.button('Cancel', on_click=on_cancel).classes('btn-secondary')
                        ui.button('Create Job Posting', on_click=save_job).classes('btn-primary')

        
        def render_applications():
            """Render applications section as a table."""
            # Load applications from session if available, else sample
            applications = app.storage.user.get('applications', []) or [
                {'applicant': 'Sarah Ochieng', 'job': 'Full Stack Developer', 'status': 'Under Review', 'applied': '2025-10-18'},
                {'applicant': 'Michael Adebayo', 'job': 'Data Scientist', 'status': 'Interview', 'applied': '2025-10-17'},
                {'applicant': 'Grace Mwangi', 'job': 'UI/UX Designer', 'status': 'Shortlisted', 'applied': '2025-10-16'},
            ]
            ui.label('Applications').classes('section-header')

            # Filters and sort controls
            with ui.row().classes('w-full items-center justify-between mb-4'):
                with ui.row().classes('gap-3'):
                    status_options = ['All', 'Under Review', 'Interview', 'Shortlisted', 'Rejected', 'Hired']
                    sort_options = ['Applicant', 'Job', 'Status', 'Applied On']
                    ui.select(status_options, value=applications_state['status_filter'], label='Status')\
                        .props('outlined dense').on('update:model-value', lambda e: (applications_state.update({'status_filter': e.value, 'page': 1}), navigate_to_section('applications')))
                    ui.select(sort_options, value=applications_state['sort_by'], label='Sort by')\
                        .props('outlined dense').on('update:model-value', lambda e: (applications_state.update({'sort_by': e.value}), navigate_to_section('applications')))
                    ui.select(['asc','desc'], value=applications_state['sort_dir'], label='Direction')\
                        .props('outlined dense').on('update:model-value', lambda e: (applications_state.update({'sort_dir': e.value}), navigate_to_section('applications')))
                with ui.row().classes('gap-3'):
                    ui.select([10, 20, 50], value=applications_state['page_size'], label='Page size')\
                        .props('outlined dense').on('update:model-value', lambda e: (applications_state.update({'page_size': int(e.value), 'page': 1}), navigate_to_section('applications')))

            # Apply filters
            filtered = applications
            if applications_state['status_filter'] != 'All':
                filtered = [a for a in filtered if (a.get('status') or '') == applications_state['status_filter']]

            # Apply sorting
            key = applications_state['sort_by']
            reverse = applications_state['sort_dir'] == 'desc'
            def sort_key(a):
                if key == 'Applied On':
                    return a.get('applied','')
                return a.get(key.lower().replace(' ', '_'), '') if key in ['Applicant','Job','Status'] else ''
            try:
                filtered = sorted(filtered, key=sort_key, reverse=reverse)
            except Exception:
                pass

            # Pagination
            total = len(filtered)
            page_size = int(applications_state['page_size'])
            total_pages = max(1, (total + page_size - 1) // page_size)
            applications_state['page'] = min(max(1, applications_state['page']), total_pages)
            start = (applications_state['page'] - 1) * page_size
            page_rows = filtered[start:start+page_size]
            with ui.card().classes('glass-card p-0'):
                with ui.element('div').classes('table-container'):
                    with ui.element('table').classes('w-full'):
                        with ui.element('thead'):
                            with ui.element('tr'):
                                for h in ['Applicant', 'Job', 'Status', 'Applied On', 'Actions']:
                                    with ui.element('th'):
                                        ui.label(h)
                        with ui.element('tbody'):
                            for app_row in page_rows:
                                with ui.element('tr'):
                                    with ui.element('td'):
                                        ui.label(app_row.get('applicant', ''))
                                    with ui.element('td'):
                                        ui.label(app_row.get('job', ''))
                                    with ui.element('td'):
                                        ui.label(app_row.get('status', ''))
                                    with ui.element('td'):
                                        ui.label(app_row.get('applied', ''))
                                    with ui.element('td'):
                                        with ui.row().classes('gap-2'):
                                            ui.button('View', on_click=lambda a=app_row: ui.notify(f"Viewing application: {a.get('applicant')}"))\
                                                .props('flat size=sm')
                                            ui.button('Message', on_click=lambda a=app_row: ui.notify(f"Messaging {a.get('applicant')}"))\
                                                .props('flat size=sm')
            # Pagination controls
            with ui.row().classes('justify-end items-center gap-3 mt-3'):
                ui.button('Prev', on_click=lambda: (applications_state.update({'page': max(1, applications_state['page']-1)}), navigate_to_section('applications'))).props('outline size=sm')
                ui.label(f"Page {applications_state['page']} of {total_pages}").classes('text-sm text-gray-600')
                ui.button('Next', on_click=lambda: (applications_state.update({'page': min(total_pages, applications_state['page']+1)}), navigate_to_section('applications'))).props('outline size=sm')

        def render_candidates():
            """Render candidates section as a table."""
            # Load candidates from session if available, else sample
            candidates = app.storage.user.get('candidates', []) or [
                {'name': 'Sarah Ochieng', 'title': 'Full Stack Developer', 'location': 'Nairobi, KE', 'skills': ['React','Node.js','Python'], 'rating': 4.8, 'availability': 'Available'},
                {'name': 'Michael Adebayo', 'title': 'Data Scientist', 'location': 'Lagos, NG', 'skills': ['Python','ML','SQL'], 'rating': 4.9, 'availability': 'Available Soon'},
                {'name': 'Grace Mwangi', 'title': 'UI/UX Designer', 'location': 'Nairobi, KE', 'skills': ['Figma','Prototyping','Research'], 'rating': 4.7, 'availability': 'Available'},
            ]
            ui.label('Candidates').classes('section-header')
            with ui.card().classes('glass-card p-0'):
                with ui.element('div').classes('table-container'):
                    with ui.element('table').classes('w-full'):
                        with ui.element('thead'):
                            with ui.element('tr'):
                                for h in ['Name', 'Title', 'Location', 'Skills', 'Rating', 'Availability', 'Actions']:
                                    with ui.element('th'):
                                        ui.label(h)
                        with ui.element('tbody'):
                            for c in candidates:
                                with ui.element('tr'):
                                    with ui.element('td'):
                                        ui.label(c.get('name',''))
                                    with ui.element('td'):
                                        ui.label(c.get('title',''))
                                    with ui.element('td'):
                                        ui.label(c.get('location',''))
                                    with ui.element('td'):
                                        ui.label(', '.join(c.get('skills', [])[:5]))
                                    with ui.element('td'):
                                        ui.label(str(c.get('rating','')))
                                    with ui.element('td'):
                                        ui.label(c.get('availability',''))
                                    with ui.element('td'):
                                        with ui.row().classes('gap-2'):
                                            ui.button('View', on_click=lambda cand=c: ui.notify(f"Viewing {cand.get('name')}"))\
                                                .props('flat size=sm')
                                            ui.button('Contact', on_click=lambda cand=c: ui.notify(f"Contacting {cand.get('name')}"))\
                                                .props('flat size=sm')
        
        def render_company_profile():
            """Render company profile section."""
            ui.label('Company Profile').classes('section-header')
            
            with ui.card().classes('glass-card mb-6'):
                with ui.row().classes('items-start gap-6'):
                    if company_logo:
                        ui.image(company_logo).classes('w-32 h-32 rounded-lg object-cover')
                    
                    with ui.column().classes('gap-2 flex-1'):
                        ui.label(company_name).classes('text-2xl font-bold brand-charcoal')
                        ui.label(f"{employer_profile.get('industry', 'Industry')} • {employer_profile.get('companySize', 'Size')}").classes('text-gray-600')
                        if employer_profile.get('website'):
                            ui.link(employer_profile.get('website'), employer_profile.get('website')).classes('text-blue-600 text-sm')
                
                ui.separator().classes('my-4')
                
                ui.label('About').classes('font-semibold brand-charcoal mb-2')
                ui.label(employer_profile.get('description', 'No company description available')).classes('text-gray-700')
                
                if employer_profile.get('city') or employer_profile.get('country'):
                    ui.separator().classes('my-4')
                    ui.label('Location').classes('font-semibold brand-charcoal mb-2')
                    ui.label(f"{employer_profile.get('city', '')}, {employer_profile.get('country', '')}").classes('text-gray-700')
            
            # Brand-compliant action button
            with ui.element('div').classes('action-button-primary').on('click', lambda: ui.navigate.to('/employer/onboarding/profile')):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('edit', size='20px')
                    ui.label('Edit Company Profile')
        
        def render_settings():
            """Render settings section."""
            ui.label('Account Settings').classes('section-header')
            
            with ui.card().classes('glass-card mb-6'):
                ui.label('Profile Information').classes('text-lg font-semibold brand-charcoal mb-4')
                
                with ui.column().classes('gap-4'):
                    ui.input('Full Name', value=user.get('name', 'ABC Trust')).props('outlined readonly').classes('w-full')
                    ui.input('Email', value=user.get('email', '')).props('outlined readonly').classes('w-full')
                    ui.label('Contact support to change your email or name').classes('text-sm text-gray-500')
            
            with ui.card().classes('glass-card mb-6'):
                ui.label('Notifications').classes('text-lg font-semibold brand-charcoal mb-4')
                
                with ui.column().classes('gap-3'):
                    with ui.row().classes('items-center justify-between'):
                        ui.label('Email notifications for new applications').classes('text-gray-700')
                        ui.switch(value=True)
                    
                    with ui.row().classes('items-center justify-between'):
                        ui.label('Weekly summary reports').classes('text-gray-700')
                        ui.switch(value=True)
                    
                    with ui.row().classes('items-center justify-between'):
                        ui.label('Marketing emails').classes('text-gray-700')
                        ui.switch(value=False)
            
            with ui.card().classes('glass-card'):
                ui.label('Danger Zone').classes('text-lg font-semibold text-red-600 mb-4')
                ui.button('Delete Account', on_click=lambda: ui.notify('Contact support to delete your account')).props('outline').classes('text-red-600 border-red-600')

        # Initial render
        with content_area:
            render_section(active_section['current'])
        
        # Load dashboard data (removed async to prevent reload loop)
        # asyncio.create_task(fetch_dashboard_data())
    
    footer()
