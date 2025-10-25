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
    
    # Modern styling (same as candidate dashboard)
    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { 
            font-family: 'Raleway', sans-serif; 
            scroll-behavior: smooth;
        }
        .dashboard-wrapper { background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%); min-height: 100vh; }
        .sidebar-modern { background: linear-gradient(180deg, #1A1A1A 0%, #2d2d2d 100%); width: 280px; position: fixed; left: 0; top: 64px; height: calc(100vh - 64px); overflow-y: auto; box-shadow: 4px 0 24px rgba(0,0,0,0.15); z-index: 1001; transition: transform 0.3s ease; }
        .user-profile-card { background: rgba(0, 85, 184, 0.1); border: 1px solid rgba(0, 85, 184, 0.3); border-radius: 16px; padding: 20px; margin: 20px; }
        .profile-avatar { width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg, #0055B8 0%, #003d82 100%); display: flex; align-items: center; justify-content: center; font-size: 28px; color: white; font-weight: 700; box-shadow: 0 4px 12px rgba(0, 85, 184, 0.3); }
        .nav-item { padding: 14px 24px; margin: 8px 16px; border-radius: 12px; cursor: pointer; transition: all 0.3s ease; display: flex; align-items: center; gap: 12px; color: #b0b0b0; font-weight: 500; }
        .nav-item:hover { background: rgba(0, 85, 184, 0.1); color: #0055B8; transform: translateX(4px); }
        .nav-item.active { background: linear-gradient(135deg, #0055B8 0%, #003d82 100%); color: white; box-shadow: 0 4px 16px rgba(0, 85, 184, 0.4); }
        .main-content { margin-left: 280px; margin-top: 64px; padding: 32px; min-height: calc(100vh - 64px); transition: margin-left 0.3s ease; }
        .main-content.sidebar-collapsed { margin-left: 0; }
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); border-radius: 20px; padding: 28px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08); border: 1px solid rgba(255, 255, 255, 0.8); }
        .section-header { font-size: 28px; font-weight: 700; color: #1A1A1A; margin-bottom: 24px; display: flex; align-items: center; gap: 12px; }
        .section-header::before { content: ''; width: 4px; height: 32px; background: linear-gradient(180deg, #0055B8 0%, #003d82 100%); border-radius: 2px; }
        .btn-primary { background: linear-gradient(135deg, #0055B8 0%, #003d82 100%); color: white; padding: 12px 28px; border-radius: 12px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0, 85, 184, 0.3); }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(0, 85, 184, 0.4); }
        .btn-secondary { background: white; color: #0055B8; padding: 12px 28px; border-radius: 12px; font-weight: 600; border: 2px solid #0055B8; cursor: pointer; transition: all 0.3s ease; }
        .btn-secondary:hover { background: #0055B8; color: white; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .fade-in { animation: fadeIn 0.6s ease forwards; }

        /* ==========================
           Table Brand Enforcement
           ========================== */
        table, .q-table, .q-table * {
            font-family: 'Raleway', sans-serif !important;
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
        
        /* Mobile Responsive Styles */
        @media (max-width: 1023px) {
            .sidebar-modern {
                transform: translateX(-100%);
                box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
            }
            
            .sidebar-modern.mobile-open {
                transform: translateX(0);
            }
            
            .main-content {
                margin-left: 0 !important;
                padding: 16px !important;
            }
            
            .glass-card {
                padding: 16px !important;
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

    # Main dashboard wrapper
    with ui.element('div').classes('dashboard-wrapper'):
        # Sidebar
        sidebar = ui.element('div').classes('sidebar-modern')
        with sidebar:
            # User Profile Card
            with ui.element('div').classes('user-profile-card'):
                with ui.row().classes('items-center gap-4'):
                    initials = ''.join([n[0].upper() for n in user.get('name', 'ABC Trust').split()[:2]])
                    with ui.element('div').classes('profile-avatar'):
                        ui.label(initials)
                    
                    with ui.column().classes('gap-1'):
                        ui.label(user.get('name', 'ABC Trust')).classes('text-white font-semibold text-base')
                        ui.label(user.get('email', '')).classes('text-gray-300 text-xs')
            
            ui.separator().style('background: rgba(255,255,255,0.1); margin: 20px 0;')
            
            # Navigation menu (no icons)
            menu_items = [
                ('overview', 'Dashboard'),
                ('postings', 'Job Postings'),
                ('applications', 'Applications'),
                ('candidates', 'Candidates'),
                ('company', 'Company Profile'),
                ('settings', 'Settings'),
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
            
            for section, label in menu_items:
                is_active = section == active_section['current']
                nav_el = ui.element('div').classes(f'nav-item {"active" if is_active else ""}')
                nav_el.on('click', create_nav_handler(section))
                with nav_el:
                    ui.label(label).classes('text-sm')
                menu_buttons[section] = nav_el
            
            ui.separator().style('background: rgba(255,255,255,0.1); margin: 20px 0;')
            
            def logout_handler():
                from app.services.auth_utils import logout
                logout()
            
            logout_el = ui.element('div').classes('nav-item')
            logout_el.on('click', logout_handler)
            with logout_el:
                ui.label('Logout').classes('text-sm')

        # Main Content Area
        content_area = ui.column().classes('main-content')
        
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
            ui.label(f'Welcome back, {user.get("name", "ABC Trust")}!').classes('section-header')
            
            # Stats cards
            with ui.row().classes('w-full gap-6 mb-8'):
                # Active Job Postings Card
                with ui.card().classes('glass-card flex-1'):
                    ui.label('Active Job Postings').classes('text-gray-600 text-sm font-medium mb-2')
                    ui.label(str(dashboard_data['active_postings'])).classes('text-4xl font-bold brand-primary mb-1')
                    ui.label('Currently accepting applications').classes('text-xs text-gray-500')
                
                # Total Applications Card
                with ui.card().classes('glass-card flex-1'):
                    ui.label('Total Applications').classes('text-gray-600 text-sm font-medium mb-2')
                    ui.label(str(dashboard_data['pending_applications'])).classes('text-4xl font-bold brand-primary mb-1')
                    ui.label('Awaiting review').classes('text-xs text-gray-500')
                
                # Candidates Viewed Card
                with ui.card().classes('glass-card flex-1'):
                    ui.label('Candidates').classes('text-gray-600 text-sm font-medium mb-2')
                    ui.label(str(dashboard_data['candidates_count'])).classes('text-4xl font-bold brand-primary mb-1')
                    ui.label('In your pipeline').classes('text-xs text-gray-500')
            
            # Recent Activity (as table)
            with ui.card().classes('glass-card p-0 mb-6'):
                with ui.element('div').classes('px-6 py-4'):
                    ui.label('Recent Job Postings').classes('text-xl font-semibold brand-charcoal')
                if dashboard_data['job_postings']:
                    with ui.element('table').classes('w-full'):
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
            with ui.card().classes('glass-card'):
                ui.label('Quick Actions').classes('text-xl font-semibold brand-charcoal mb-4')
                with ui.row().classes('gap-4'):
                    ui.button('Post a New Job', 
                             on_click=lambda: ui.notify('Job posting form coming soon!')).classes('btn-primary')
                    ui.button('Browse Candidates', 
                             on_click=lambda: navigate_to_section('candidates')).classes('btn-secondary')
                    ui.button('Update Company Profile', 
                             on_click=lambda: ui.navigate.to('/employer/onboarding/profile')).classes('btn-secondary')
        
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
                ui.label('Job Postings').classes('section-header')
                ui.button('Create New Job' if not show_create_form['visible'] else 'View Job List', 
                         on_click=toggle_create_form).classes('btn-primary')
            
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
                    ui.label('No job postings yet').classes('text-gray-500 text-xl')
                    ui.label('Create your first job posting to start attracting candidates').classes('text-gray-400')
                    ui.button('Create Job Posting', 
                             on_click=toggle_create_form).classes('btn-primary mt-4')
        
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
            
            ui.button('Edit Company Profile', 
                     on_click=lambda: ui.navigate.to('/employer/onboarding/profile')).classes('btn-primary')
        
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
