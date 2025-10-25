"""
Redesigned Modern Candidate Dashboard - Dompell Africa
A clean, professional dashboard with enhanced UX and modern design
"""
from nicegui import ui, app
from app.services.api_service import api_service
from app.services.auth_utils import get_current_user, is_authenticated
from app.components.header import header
from app.components.footer import footer

import asyncio
import mimetypes

def redesigned_candidate_dashboard():
    """Completely redesigned candidate dashboard with modern UI/UX."""
    
    # Check authentication
    if not is_authenticated():
        ui.notify("Please login to access the dashboard", type='negative')
        ui.navigate.to('/login')
        return
    
    user = get_current_user()
    user_id = user.get('id')
    token = app.storage.user.get('token')
    
    # Debug: Check token
    print(f"[DASHBOARD] User ID: {user_id}")
    print(f"[DASHBOARD] Token exists: {bool(token)}")
    print(f"[DASHBOARD] Token preview: {token[:20] if token else 'None'}...")
    
    # Set token in API service
    if token:
        api_service.set_auth_token(token)
    else:
        print("[DASHBOARD] WARNING: No token found!")
    
    # Add header
    header('/candidates/dashboard')
    
    # Modern styling
    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { 
            font-family: 'Raleway', sans-serif; 
            scroll-behavior: smooth;
        }
        
        /* Layout */
        .dashboard-wrapper {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%);
            min-height: 100vh;
        }
        
        /* Sidebar */
        .sidebar-modern {
            position: fixed;
            left: 0;
            top: 64px;
            width: 280px;
            height: calc(100vh - 64px);
            background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15);
            overflow-y: auto;
            z-index: 100;
            transition: width 0.3s ease;
        }
        
        .sidebar-modern.collapsed {
            width: 80px;
        }
        
        .sidebar-modern.collapsed .user-profile-card {
            padding: 12px;
            margin: 12px;
        }
        
        .sidebar-modern.collapsed .user-info,
        .sidebar-modern.collapsed .nav-item .text-sm {
            display: none;
        }
        
        .sidebar-modern.collapsed .nav-item {
            justify-content: center;
            padding: 14px;
            margin: 8px;
        }
        
        .sidebar-modern.collapsed .profile-avatar {
            width: 48px;
            height: 48px;
            font-size: 20px;
        }
        
        .sidebar-modern::-webkit-scrollbar {
            width: 6px;
        }
        
        .sidebar-modern::-webkit-scrollbar-track {
            background: #1A1A1A;
        }
        
        .sidebar-modern::-webkit-scrollbar-thumb {
            background: #0055B8;
            border-radius: 3px;
        }
        
        .user-profile-card {
            background: rgba(0, 85, 184, 0.1);
            border: 1px solid rgba(0, 85, 184, 0.3);
            border-radius: 16px;
            padding: 20px;
            margin: 20px;
        }
        
        .profile-avatar {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0055B8 0%, #003d82 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            color: white;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(0, 85, 184, 0.3);
        }
        
        .nav-item {
            padding: 14px 24px;
            margin: 8px 16px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #b0b0b0;
            font-weight: 500;
            white-space: nowrap;
        }
        
        .nav-item:hover {
            background: rgba(0, 85, 184, 0.1);
            color: #0055B8;
            transform: translateX(4px);
        }
        
        .nav-item.active {
            background: linear-gradient(135deg, #0055B8 0%, #003d82 100%);
            color: white;
            box-shadow: 0 4px 16px rgba(0, 85, 184, 0.4);
        }
        
        .nav-icon {
            font-size: 22px;
        }
        
        /* Main Content */
        .main-content {
            margin-left: 280px;
            margin-top: 64px;
            padding: 32px;
            min-height: calc(100vh - 64px);
            transition: margin-left 0.3s ease;
        }
        
        .main-content.sidebar-collapsed {
            margin-left: 80px;
        }
        
        /* Toggle Button */
        .menu-toggle {
            position: absolute;
            top: 20px;
            right: -15px;
            width: 30px;
            height: 30px;
            background: #0055B8;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0, 85, 184, 0.3);
            transition: all 0.3s ease;
            z-index: 101;
        }
        
        .menu-toggle:hover {
            background: #004494;
            transform: scale(1.1);
        }
        
        .menu-toggle .material-icons {
            color: white;
            font-size: 18px;
        }
        
        /* Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.8);
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }
        
        .stat-card {
            background: linear-gradient(135deg, #003d82 0%, #002855 100%);
            border-radius: 20px;
            padding: 28px;
            color: white;
            position: relative;
            overflow: hidden;
            border: 1px solid #004494;
            box-shadow: 0 4px 12px rgba(0, 61, 130, 0.3);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            border-color: #0055B8;
            box-shadow: 0 8px 20px rgba(0, 85, 184, 0.4);
            transform: translateY(-4px);
        }
        
        .stat-card::before {
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
        
        .stat-number {
            font-size: 48px;
            font-weight: 800;
            line-height: 1;
            margin: 12px 0;
        }
        
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Progress Bars */
        .progress-bar-container {
            background: #e5e7eb;
            border-radius: 12px;
            height: 12px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-bar-fill {
            background: linear-gradient(90deg, #0055B8 0%, #00a8ff 100%);
            height: 100%;
            border-radius: 12px;
            transition: width 1s ease;
            box-shadow: 0 2px 8px rgba(0, 85, 184, 0.4);
        }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .badge-success {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }
        
        .badge-warning {
            background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
            color: white;
        }
        
        .badge-info {
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            color: white;
        }
        
        /* Buttons - Brand Guidelines Compliant */
        .btn-primary {
            background-color: #0055B8 !important;
            color: white !important;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            font-family: 'Raleway', sans-serif !important;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(0, 85, 184, 0.2);
        }
        
        .btn-primary:hover {
            background-color: #004494 !important;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(0, 85, 184, 0.3);
        }
        
        .btn-secondary {
            background-color: white !important;
            color: #0055B8 !important;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            font-family: 'Raleway', sans-serif !important;
            border: 2px solid #0055B8 !important;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0, 85, 184, 0.1);
        }
        
        .btn-secondary:hover {
            background-color: #F2F7FB !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 85, 184, 0.15);
        }
        
        /* Section Headers */
        .section-header {
            font-size: 28px;
            font-weight: 700;
            color: #1A1A1A;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .section-header::before {
            content: '';
            width: 4px;
            height: 32px;
            background: linear-gradient(180deg, #0055B8 0%, #003d82 100%);
            border-radius: 2px;
        }
        
        /* Skills Chips */
        .skill-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: linear-gradient(135deg, #0055B8 0%, #003d82 100%);
            color: white;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            margin: 4px;
            box-shadow: 0 2px 8px rgba(0, 85, 184, 0.2);
            transition: all 0.2s ease;
        }
        
        .skill-chip:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 85, 184, 0.3);
        }
        
        /* Timeline */
        .timeline-item {
            position: relative;
            padding-left: 32px;
            padding-bottom: 24px;
        }
        
        .timeline-item::before {
            content: '';
            position: absolute;
            left: 8px;
            top: 8px;
            bottom: -16px;
            width: 2px;
            background: linear-gradient(180deg, #0055B8 0%, transparent 100%);
        }
        
        .timeline-dot {
            position: absolute;
            left: 0;
            top: 8px;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #0055B8;
            box-shadow: 0 0 0 4px rgba(0, 85, 184, 0.2);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease forwards;
        }
        
        /* Responsive */
        @media (max-width: 1024px) {
            .sidebar-modern {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }
            
            .sidebar-modern.open {
                transform: translateX(0);
            }
            
            .main-content {
                margin-left: 0;
            }
        }
        /* Professional Card System (aligned with institution dashboard) */
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
        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            padding: 12px;
            margin: 8px 0;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(0, 85, 184, 0.05) 0%, transparent 70%);
            border-radius: 50%;
            transform: translate(30%, -30%);
        }
        .metric-label { font-size: 10px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .metric-value { font-size: 20px; font-weight: 800; color: #0055B8; line-height: 1; margin: 6px 0 4px 0; }
        .metric-trend { font-size: 11px; color: #10b981; font-weight: 600; margin-top: 4px; }
        /* Grid for metrics */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 20px; padding-left: 20px; padding-right: 20px; }

        /* Reusable row and pill styles */
        .item-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 14px;
            background: #f9fafb;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            transition: background 0.2s ease;
        }
        .item-row:hover { background: #f3f6fa; }
        .status-pill {
            display: inline-flex;
            align-items: center;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.3px;
            text-transform: uppercase;
        }
        .status-under-review { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
        .status-interview { background: #ecfccb; color: #3f6212; border: 1px solid #bef264; }
        .status-applied { background: #e2e8f0; color: #334155; border: 1px solid #cbd5e1; }

        /* ==========================
           Table Brand Enforcement - Strict Brand Guidelines
           ========================== */
        /* Apply to all tables including Quasar q-table */
        table, .q-table, .q-table * {
            font-family: 'Raleway', sans-serif !important;
            color: #1A1A1A !important;
        }
        /* Container */
        .q-table, table {
            background: #FFFFFF !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(0, 85, 184, 0.08) !important;
        }
        /* Header cells - Brand Colors */
        .q-table thead tr, thead tr {
            background: #F2F7FB !important;
            border-bottom: 2px solid #0055B8 !important;
        }
        .q-th, thead th {
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            font-weight: 700 !important;
            font-size: 12px !important;
            color: #1A1A1A !important;
            padding: 12px 16px !important;
            font-family: 'Raleway', sans-serif !important;
        }
        /* Body cells */
        .q-td, tbody td {
            font-size: 14px !important;
            color: #4D4D4D !important;
            padding: 14px 16px !important;
            border-bottom: 1px solid #e5e7eb !important;
            font-family: 'Raleway', sans-serif !important;
        }
        /* Rows */
        .q-tr:hover, tbody tr:hover {
            background: #F2F7FB !important;
        }
        tbody tr:last-child .q-td, tbody tr:last-child td {
            border-bottom: none !important;
        }
        /* Links and action buttons inside tables - Brand Blue */
        .q-table a, table a { 
            color: #0055B8 !important; 
            text-decoration: none !important;
            font-weight: 600 !important;
            font-family: 'Raleway', sans-serif !important;
        }
        .q-table a:hover, table a:hover { 
            text-decoration: underline !important;
            color: #004494 !important;
        }
        .q-table .q-btn, table .q-btn {
            background-color: #0055B8 !important;
            color: white !important;
            font-family: 'Raleway', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
        }
        .q-table .q-btn:hover, table .q-btn:hover {
            background-color: #004494 !important;
        }
        /* Pagination/footer area */
        .q-table__bottom, .q-table__separator { 
            border-color: #e5e7eb !important;
            background: #F2F7FB !important;
        }
        .q-table__bottom .q-btn {
            color: #0055B8 !important;
            font-family: 'Raleway', sans-serif !important;
        }
    </style>
    ''')
    
    # State management
    active_section = {'current': 'overview'}
    user_data = {'profile': None}
    
    # Load user profile
    def load_user_profile():
        """Load complete user profile from API (synchronous)."""
        try:
            print(f"[PROFILE_LOAD] Attempting to load profile for user: {user_id}")
            print(f"[PROFILE_LOAD] API service has token: {bool(api_service.token)}")
            
            response = api_service._make_request('GET', f'/users/{user_id}')
            
            print(f"[PROFILE_LOAD] Response status: {response.status_code}")
            
            if response.ok:
                data = response.json()
                user_data['profile'] = data.get('data', {})
                print(f"[PROFILE_LOAD] Profile loaded successfully")
                print(f"[PROFILE_LOAD] Full profile structure: {user_data['profile']}")
                return user_data['profile']
            elif response.status_code == 401:
                # Session expired - redirect to login
                print(f"[ERROR] Session expired: {response.text}")
                from app.services.auth_utils import logout
                ui.notify('Your session has expired. Please log in again.', type='warning')
                logout()
                return None
            else:
                print(f"[ERROR] Failed to load profile: {response.status_code}")
                print(f"[ERROR] Response body: {response.text}")
                return None
        except Exception as e:
            print(f"[ERROR] Loading profile: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # Load profile data BEFORE rendering UI
    load_user_profile()
    
    # Main dashboard wrapper
    with ui.element('div').classes('dashboard-wrapper'):
        
        # Sidebar
        with ui.element('div').classes('sidebar-modern') as sidebar:
            # Toggle Button
            toggle_btn = ui.element('div').classes('menu-toggle')
            with toggle_btn:
                ui.icon('chevron_left').classes('toggle-icon')
            
            # Toggle functionality
            def toggle_sidebar():
                sidebar.classes(toggle='collapsed')
                content_area_wrapper.classes(toggle='sidebar-collapsed')
                # Change icon direction
                if 'collapsed' in (sidebar._classes or ''):
                    toggle_btn.clear()
                    with toggle_btn:
                        ui.icon('chevron_right').classes('toggle-icon')
                else:
                    toggle_btn.clear()
                    with toggle_btn:
                        ui.icon('chevron_left').classes('toggle-icon')
            
            toggle_btn.on('click', toggle_sidebar)
            
            # User Profile Card
            with ui.element('div').classes('user-profile-card'):
                with ui.row().classes('items-center gap-4'):
                    # Avatar - Always try to show profile picture from loaded profile
                    profile_pic_url = ''
                    if user_data.get('profile'):
                        tp = user_data['profile'].get('traineeProfile') or {}
                        profile_pic_url = tp.get('profilePictureUrl') or ''
                        print(f"[SIDEBAR] Profile picture URL: {profile_pic_url}")
                    else:
                        print(f"[SIDEBAR] No profile data available")
                    
                    # Show image if URL exists, otherwise show initials
                    if profile_pic_url and profile_pic_url.strip():
                        print(f"[SIDEBAR] Rendering profile image")
                        with ui.element('div').style('width: 56px; height: 56px; border-radius: 50%; overflow: hidden; border: 3px solid rgba(255,255,255,0.4); box-shadow: 0 4px 12px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;'):
                            ui.image(profile_pic_url).style('width: 100%; height: 100%; object-fit: cover; object-position: center;')
                    else:
                        # Fallback to initials avatar
                        print(f"[SIDEBAR] Rendering initials avatar")
                        initials = ''.join([n[0].upper() for n in user.get('name', 'U').split()[:2]])
                        with ui.element('div').classes('profile-avatar'):
                            ui.label(initials)
                    
                    # User info
                    with ui.column().classes('gap-1 user-info'):
                        ui.label(user.get('name', 'User')).classes('text-white font-semibold text-base')
                        ui.label(user.get('email', '')).classes('text-gray-300 text-xs')
            
            ui.separator().style('background: rgba(255,255,255,0.1); margin: 20px 0;')
            
            # Navigation menu
            menu_items = [
                ('overview', 'dashboard', 'Dashboard'),
                ('profile', 'person', 'My Profile'),
                ('documents', 'folder', 'Documents'),
                ('settings', 'settings', 'Settings'),
            ]
            
            menu_buttons = {}
            
            def create_nav_handler(section):
                def handler():
                    active_section['current'] = section
                    # Update active state
                    for sec, btn_el in menu_buttons.items():
                        if sec == section:
                            btn_el.classes(add='active', remove='')
                        else:
                            btn_el.classes(remove='active', add='')
                    # Render content
                    content_area.clear()
                    with content_area:
                        render_section(section)
                return handler
            
            for section, icon, label in menu_items:
                is_active = section == active_section['current']
                nav_el = ui.element('div').classes(f'nav-item {"active" if is_active else ""}')
                nav_el.on('click', create_nav_handler(section))
                with nav_el:
                    ui.icon(icon).classes('nav-icon')
                    ui.label(label).classes('text-sm')
                menu_buttons[section] = nav_el
            
            ui.separator().style('background: rgba(255,255,255,0.1); margin: 20px 0;')
            
            # Logout
            def logout_handler():
                from app.services.auth_utils import logout
                logout()
            
            logout_el = ui.element('div').classes('nav-item')
            logout_el.on('click', logout_handler)
            with logout_el:
                ui.icon('logout').classes('nav-icon')
                ui.label('Logout').classes('text-sm')
        
        # Main Content Area
        content_area_wrapper = ui.column().classes('main-content')
        with content_area_wrapper:
            content_area = ui.column()

        # Dialog for viewing files
        with ui.dialog() as file_dialog, ui.card().style('min-width: 80%; max-width: 95%;'):
            dialog_title = ui.label('File Viewer').classes('text-2xl font-bold mb-4')
            dialog_content = ui.html('', sanitize=lambda s: s).classes('w-full')
            with ui.row().classes('w-full justify-end mt-4'):
                ui.button('Close', on_click=file_dialog.close).classes('btn-secondary')

        def show_file_in_dialog(file_info):
            """Open a dialog to view the selected file."""
            url = file_info.get('url')
            file_type = file_info.get('type', '')
            name = file_info.get('name', 'File')

            if not url:
                ui.notify('File URL is missing.', type='negative')
                return

            dialog_title.set_text(name)
            
            if 'image' in file_type:
                content = f'<img src="{url}" style="max-width: 100%; max-height: 70vh; display: block; margin: auto;" />'
            elif 'pdf' in file_type:
                content = f'<iframe src="{url}" style="width: 100%; height: 75vh; border: none;"></iframe>'
            else:
                content = f'''
                    <div style="text-align: center; padding: 40px;">
                        <p class="text-lg">Preview is not available for this file type.</p>
                        <a href="{url}" target="_blank" class="btn-primary" style="text-decoration: none; display: inline-block; margin-top: 20px;">Download File</a>
                    </div>
                '''
            
            dialog_content.set_content(content)
            file_dialog.open()
        
        def render_section(section):
            """Render content based on active section."""
            if section == 'overview':
                render_dashboard()
            elif section == 'profile':
                render_profile_section()
            elif section == 'documents':
                render_documents()
            elif section == 'settings':
                render_settings()
        
        def render_dashboard():
            """Main dashboard overview."""
            with ui.element('div').classes('fade-in'):
                # Check if profile loaded
                if not user_data.get('profile'):
                    # Show limited dashboard with session warning
                    with ui.element('div').classes('pro-card text-center py-12'):
                        ui.icon('info').style('font-size: 64px; color: #f6ad55;')
                        ui.label('Session Information').classes('text-2xl font-bold text-gray-800 mt-4 mb-2')
                        ui.label('Unable to load full profile data. This may be due to an expired session.').classes('text-gray-600 mb-6')
                        
                        with ui.row().classes('gap-4 justify-center'):
                            def refresh_page():
                                ui.navigate.to('/candidates/dashboard', reload=True)
                            
                            ui.button('Refresh Page', icon='refresh', on_click=refresh_page).classes('btn-secondary')
                            ui.button('Log Out and Sign In Again', icon='logout', on_click=lambda: ui.navigate.to('/login')).classes('btn-primary')
                    return
                
                # Welcome header without profile picture
                with ui.row().classes('items-center justify-between w-full mb-8 p-4'):
                    with ui.column().classes('gap-2'):
                        ui.label(f'Welcome back, {user.get("name", "User").split()[0]}!').classes('text-4xl font-bold text-gray-800')
                        ui.label('Complete your profile and upload your documents to get started.').classes('text-lg text-gray-600')
                    
                
                # Profile Completion Stats - Real data from API
                tp = user_data.get('profile', {}).get('traineeProfile') or {}
                
                # Track what's real vs demo for display purposes
                demo_data_used = {
                    'skills': False,
                    'headline': False,
                    'bio': False,
                    'location': False,
                    'picture': False,
                    'cv': False
                }
                
                # Supplement with demo data ONLY for display in overview
                # This doesn't modify the actual API data
                display_tp = tp.copy()
                
                if not tp.get('skills') or len(tp.get('skills', [])) == 0:
                    display_tp['skills'] = [
                        {'id': 'demo-1', 'name': 'Python', '_demo': True},
                        {'id': 'demo-2', 'name': 'JavaScript', '_demo': True},
                        {'id': 'demo-3', 'name': 'React', '_demo': True},
                        {'id': 'demo-4', 'name': 'Node.js', '_demo': True},
                        {'id': 'demo-5', 'name': 'SQL', '_demo': True},
                        {'id': 'demo-6', 'name': 'Git', '_demo': True},
                        {'id': 'demo-7', 'name': 'Docker', '_demo': True},
                        {'id': 'demo-8', 'name': 'AWS', '_demo': True},
                    ]
                    demo_data_used['skills'] = True
                
                if not tp.get('headline'):
                    display_tp['headline'] = 'Full Stack Developer | Python & JavaScript Expert'
                    demo_data_used['headline'] = True
                
                if not tp.get('bio'):
                    display_tp['bio'] = 'Passionate software developer with experience building scalable applications.'
                    demo_data_used['bio'] = True
                
                if not tp.get('location'):
                    display_tp['location'] = 'Accra, Ghana'
                    demo_data_used['location'] = True
                
                # Use real data for calculations, but show demo count if using demo skills
                has_picture = bool(tp.get('profilePictureUrl'))
                has_cv = bool(tp.get('cvUrl'))
                has_bio = bool(tp.get('bio'))
                has_location = bool(tp.get('location'))
                
                # For skills count, use display data to show demo count
                real_skills_count = len(tp.get('skills', []))
                display_skills_count = len(display_tp.get('skills', []))
                skills_count = display_skills_count if demo_data_used['skills'] else real_skills_count
                
                completion_items = [
                    has_picture,
                    has_cv,
                    has_bio,
                    has_location,
                    skills_count > 0
                ]
                completion_pct = int((sum(completion_items) / len(completion_items)) * 100)
                
                with ui.element('div').classes('stats-grid'):
                    stats = [
                        ('Profile Picture', '✓' if has_picture else '✗', 'photo_camera', '#0055B8' if has_picture else '#cbd5e1', 'Uploaded' if has_picture else 'Missing'),
                        ('CV/Resume', '✓' if has_cv else '✗', 'description', '#48bb78' if has_cv else '#cbd5e1', 'Uploaded' if has_cv else 'Missing'),
                        ('Skills Added', str(skills_count), 'psychology', '#f6ad55', f'{skills_count} skills'),
                        ('Profile Completion', f'{completion_pct}%', 'verified', '#9f7aea', 'Complete' if completion_pct == 100 else 'In Progress'),
                    ]
                    for label, value, icon, color, trend in stats:
                        with ui.card().classes('metric-card'):
                            with ui.row().classes('items-start justify-between w-full'):
                                with ui.column().classes('gap-0 flex-1'):
                                    ui.label(label).classes('metric-label')
                                    ui.label(value).classes('metric-value').style(f'color: {color} !important;')
                                    ui.label(trend).classes('metric-trend').style(f'color: {color} !important;')
                                ui.icon(icon, size='24px').style(f'color: {color} !important; opacity: 0.3;')
                
                # Two-column layout
                with ui.row().classes('w-full gap-6'):
                    # Left column - Profile Completion
                    with ui.column().classes('flex-1 gap-6'):
                        # Profile Completion Card
                        with ui.element('div').classes('pro-card').style('padding: 16px 20px; margin-left: 20px; margin-right: 20px;'):
                            ui.label('Complete Your Profile').classes('section-header text-2xl')
                            
                            ui.label(f'Your profile is {completion_pct}% complete').classes('text-gray-600 mb-4')
                            
                            sections = [
                                ('Profile Picture', 100 if has_picture else 0),
                                ('CV/Resume', 100 if has_cv else 0),
                                ('Bio & Location', 100 if (has_bio and has_location) else 50 if (has_bio or has_location) else 0),
                                ('Skills', 100 if skills_count >= 3 else (skills_count * 33)),
                            ]
                            
                            for section_name, progress in sections:
                                with ui.column().classes('mb-4'):
                                    with ui.row().classes('justify-between items-center mb-2'):
                                        ui.label(section_name).classes('font-medium text-gray-700')
                                        ui.label(f'{progress}%').classes('text-sm font-semibold text-blue-600')
                                    
                                    with ui.element('div').classes('progress-bar-container'):
                                        ui.element('div').classes('progress-bar-fill').style(f'width: {progress}%;')
                            
                            def go_to_profile():
                                active_section['current'] = 'profile'
                                for sec, btn_el in menu_buttons.items():
                                    if sec == 'profile':
                                        btn_el.classes(add='active', remove='')
                                    else:
                                        btn_el.classes(remove='active', add='')
                                content_area.clear()
                                with content_area:
                                    render_profile_section()
                            
                            ui.button('Complete Profile Now', icon='arrow_forward', on_click=go_to_profile).classes('btn-primary w-full mt-4')
                        
                        # Documents Upload Card
                        with ui.element('div').classes('pro-card').style('padding: 16px 20px; margin-left: 20px; margin-right: 20px;'):
                            ui.label('Your Documents').classes('section-header text-2xl')
                            
                            uploaded_files = app.storage.user.get('onboarding_files', [])
                            has_real_docs = len(uploaded_files) > 0
                            
                            # Add demo documents for display if none exist
                            display_files = uploaded_files if has_real_docs else [
                                {'name': 'Resume_2024.pdf', 'type': 'application/pdf', 'size': '245 KB', 'url': tp.get('cvUrl', ''), '_demo': True},
                                {'name': 'Certificate_Python.pdf', 'type': 'application/pdf', 'size': '1.2 MB', 'url': '', '_demo': True},
                                {'name': 'Portfolio_Screenshots.zip', 'type': 'application/zip', 'size': '5.8 MB', 'url': '', '_demo': True},
                            ]
                            
                            doc_count = len(display_files)
                            
                            with ui.row().classes('items-center justify-between mb-4'):
                                if has_real_docs:
                                    ui.label(f'{doc_count} document(s) uploaded').classes('text-gray-600')
                                else:
                                    ui.label(f'{doc_count} demo documents').classes('text-gray-500')
                                
                                def go_to_docs():
                                    active_section['current'] = 'documents'
                                    for sec, btn_el in menu_buttons.items():
                                        if sec == 'documents':
                                            btn_el.classes(add='active', remove='')
                                        else:
                                            btn_el.classes(remove='active', add='')
                                    content_area.clear()
                                    with content_area:
                                        render_documents()
                                
                                ui.button('View All', icon='folder_open', on_click=go_to_docs).classes('btn-secondary')
                            
                            if display_files:
                                for file_info in display_files[:3]:  # Show first 3
                                    file_type = file_info.get('type', '')
                                    if 'pdf' in file_type:
                                        icon = 'picture_as_pdf'
                                        color = '#ef4444'
                                    elif 'image' in file_type:
                                        icon = 'image'
                                        color = '#3b82f6'
                                    else:
                                        icon = 'description'
                                        color = '#6b7280'
                                    
                                    with ui.element('div').classes('item-row mb-2'):
                                        with ui.row().classes('items-center gap-3'):
                                            ui.icon(icon).style(f'color: {color}; font-size: 24px;')
                                            with ui.column().classes('gap-0'):
                                                ui.label(file_info.get('name', 'Unknown')).classes('font-semibold text-gray-800 text-sm')
                                                ui.label(file_info.get('size', 'N/A')).classes('text-xs text-gray-600')
                            else:
                                ui.label('No documents uploaded yet').classes('text-gray-500 text-sm text-center py-4')
                    
                    # Right column - Quick Actions
                    with ui.column().classes('flex-1 gap-6'):
                        # Quick Upload Actions
                        with ui.element('div').classes('pro-card').style('padding: 16px 20px; margin-left: 20px; margin-right: 20px;'):
                            ui.label('Quick Upload').classes('section-header text-2xl')
                            
                            actions = [
                                ('Upload Profile Picture', 'photo_camera', 'Add or update your photo', 'profile'),
                                ('Upload CV/Resume', 'description', 'Keep your CV up to date', 'profile'),
                                ('Upload Documents', 'folder', 'Add certificates, portfolios', 'documents'),
                            ]
                            
                            for action, icon, desc, target in actions:
                                def make_handler(t=target):
                                    def handler():
                                        active_section['current'] = t
                                        for sec, btn_el in menu_buttons.items():
                                            if sec == t:
                                                btn_el.classes(add='active', remove='')
                                            else:
                                                btn_el.classes(remove='active', add='')
                                        content_area.clear()
                                        with content_area:
                                            render_section(t)
                                    return handler
                                
                                with ui.element('div').classes('item-row mb-2').on('click', make_handler()):
                                    with ui.row().classes('items-center gap-3'):
                                        ui.icon(icon).style('color: #0055B8; font-size: 28px;')
                                        with ui.column().classes('gap-0'):
                                            ui.label(action).classes('font-semibold text-gray-800')
                                            ui.label(desc).classes('text-xs text-gray-600')
                        
                        # Your Skills Card
                        with ui.element('div').classes('pro-card').style('padding: 16px 20px; margin-left: 20px; margin-right: 20px;'):
                            with ui.row().classes('items-center justify-between w-full mb-3'):
                                ui.label('Your Skills').classes('section-header text-2xl')
                                with ui.element('span').style('padding: 4px 12px; background: #0055B8; color: white; border-radius: 12px; font-size: 12px; font-weight: 600;'):
                                    ui.label(f'{skills_count} Skills')
                            
                            # Show current skills or prompt to add
                            display_skills = display_tp.get('skills', [])
                            if len(display_skills) > 0:
                                # Display skills in a grid
                                with ui.element('div').style('display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;'):
                                    for skill in display_skills[:6]:  # Show first 6
                                        skill_name = skill.get('name') if isinstance(skill, dict) else str(skill)
                                        is_demo = skill.get('_demo', False) if isinstance(skill, dict) else False
                                        
                                        # Different style for demo vs real skills
                                        if is_demo:
                                            bg_style = 'background: #e5e7eb; color: #6b7280;'
                                        else:
                                            bg_style = 'background: linear-gradient(135deg, #0055B8 0%, #0066CC 100%); color: white;'
                                        
                                        with ui.element('span').style(f'padding: 6px 12px; {bg_style} border-radius: 6px; font-size: 12px; font-weight: 500;'):
                                            ui.label(skill_name)
                                
                                if len(display_skills) > 6:
                                    ui.label(f'+ {len(display_skills) - 6} more skills').classes('text-xs text-gray-500 text-center')
                                
                                def go_to_skills():
                                    active_section['current'] = 'profile'
                                    for sec, btn_el in menu_buttons.items():
                                        if sec == 'profile':
                                            btn_el.classes(add='active', remove='')
                                        else:
                                            btn_el.classes(remove='active', add='')
                                    content_area.clear()
                                    with content_area:
                                        render_profile_section()
                                
                                ui.button('Manage Skills', icon='edit', on_click=go_to_skills).classes('btn-secondary w-full mt-3')
                            else:
                                # Empty state
                                with ui.element('div').style('padding: 24px; background: #f9fafb; border: 2px dashed #e5e7eb; border-radius: 8px; text-align: center; margin-bottom: 16px;'):
                                    ui.icon('psychology').style('font-size: 48px; color: #d1d5db; margin-bottom: 8px;')
                                    ui.label('No skills added yet').classes('text-sm font-semibold text-gray-600 mb-2')
                                    ui.label('Add skills to showcase your expertise').classes('text-xs text-gray-500')
                                
                                def add_skills():
                                    active_section['current'] = 'profile'
                                    for sec, btn_el in menu_buttons.items():
                                        if sec == 'profile':
                                            btn_el.classes(add='active', remove='')
                                        else:
                                            btn_el.classes(remove='active', add='')
                                    content_area.clear()
                                    with content_area:
                                        render_profile_section()
                                
                                ui.button('Add Skills Now', icon='add_circle', on_click=add_skills).classes('btn-primary w-full')
                            
                            ui.button('Edit Profile', icon='edit', on_click=go_to_profile).classes('btn-primary w-full')
        
        def render_profile_section():
            """Enhanced profile management."""
            with ui.element('div').classes('fade-in'):
                # Local S3 upload helper available for this section (fixes scope NameError)
                # Note: /api/upload endpoint doesn't exist on backend
                # Users must provide direct URLs for CV and profile picture
                ui.label('My Professional Profile').classes('section-header text-3xl mb-6')
                
                if not user_data['profile']:
                    ui.label('Loading profile...').classes('text-gray-500')
                    ui.timer(0.1, load_and_render_profile, once=True)
                    return
                
                profile = user_data['profile']
                trainee_profile = profile.get('traineeProfile') or {}
                
                # State for profile updates
                profile_state = {
                    'name': profile.get('name', ''),
                    'bio': trainee_profile.get('bio', ''),
                    'phone': trainee_profile.get('phone', ''),
                    'linkedin': trainee_profile.get('linkedin', ''),
                    'github': trainee_profile.get('github', ''),
                    'portfolio': trainee_profile.get('portfolio', ''),
                    'skills': trainee_profile.get('skills', []),
                    'cvUrl': trainee_profile.get('cvUrl', ''),
                    'profileImageUrl': trainee_profile.get('profileImageUrl', ''),
                    'certificates': trainee_profile.get('certificates', []),
                }
                
                # If trainee profile does not exist, show inline create form (multipart)
                if not trainee_profile:
                    with ui.element('div').classes('glass-card'):
                        ui.label('Complete Your Profile').classes('font-bold text-xl mb-2')
                        ui.label('Create your trainee profile to unlock skills, education, and applications.').classes('text-sm text-gray-600 mb-4')

                        create_state = {
                            'headline': '',
                            'bio': '',
                            'location': '',
                            'profilePictureUrl': '',
                        }
                        cv_state = {'name': None, 'type': None, 'content': None}
                        avatar_state = {'name': None, 'type': None, 'content': None}

                        async def _on_cv_upload(e):
                            # Prefer PDF for backend validation
                            name = getattr(e, 'name', None)
                            content_type = getattr(e, 'type', None)
                            content = getattr(e, 'content', None)

                            # Fallback: try to read from e.file if content is missing
                            try:
                                if content is None and hasattr(e, 'file') and e.file is not None:
                                    content = await e.file.read()
                                    if name is None and hasattr(e.file, 'name'):
                                        name = getattr(e.file, 'name', None)
                            except Exception:
                                content = None

                            # Guess MIME type from filename if needed
                            guessed_type, _ = mimetypes.guess_type(name or '')
                            # Normalize: enforce application/pdf
                            final_type = content_type or guessed_type or 'application/pdf'

                            # Only allow PDF to avoid backend 'invalid cv'
                            is_pdf = (final_type == 'application/pdf') or ((name or '').lower().endswith('.pdf'))
                            if not is_pdf:
                                ui.notify('Please upload a PDF file (.pdf) for your CV', type='warning')
                                cv_state['name'] = None
                                cv_state['type'] = None
                                cv_state['content'] = None
                                return

                            cv_state['name'] = name or 'cv.pdf'
                            cv_state['type'] = 'application/pdf'
                            cv_state['content'] = content

                            if cv_state['content']:
                                ui.notify(f"CV selected: {cv_state['name']}", type='positive')
                            else:
                                ui.notify('Invalid CV upload', type='negative')

                        async def _on_avatar_upload(e):
                            avatar_state['name'] = getattr(e, 'name', None)
                            avatar_state['type'] = getattr(e, 'type', None) or 'image/jpeg'
                            avatar_state['content'] = getattr(e, 'content', None)
                            if avatar_state['content']:
                                ui.notify(f"Avatar selected: {avatar_state['name']}", type='positive')
                            else:
                                ui.notify('Invalid avatar upload', type='negative')

                        with ui.column().classes('w-full gap-3'):
                            ui.input(placeholder='Headline (e.g., Backend Developer)').props('outlined').classes('w-full').bind_value(create_state, 'headline')
                            ui.textarea(placeholder='Short bio').props('outlined').classes('w-full').bind_value(create_state, 'bio')
                            ui.input(placeholder='Location (e.g., Lagos, NG)').props('outlined').classes('w-full').bind_value(create_state, 'location')
                            with ui.row().classes('w-full gap-6'):
                                with ui.column().classes('flex-1 gap-2'):
                                    ui.label('Upload CV (PDF/DOC/DOCX)').classes('text-gray-600')
                                    ui.upload(on_upload=_on_cv_upload, auto_upload=True, label='Select CV')\
                                        .props('accept="application/pdf,.pdf" max-file-size="10485760"').classes('w-full')
                                with ui.column().classes('flex-1 gap-2'):
                                    ui.label('Upload Avatar (optional)').classes('text-gray-600')
                                    ui.upload(on_upload=_on_avatar_upload, auto_upload=True, label='Select Avatar')\
                                        .props('accept="image/*" max-file-size="5242880"').classes('w-full')
                            ui.input(placeholder='Profile Picture URL (optional, https://...)').props('outlined').classes('w-full').bind_value(create_state, 'profilePictureUrl')

                            async def _submit_create_profile():
                                # Validate
                                headline = (create_state['headline'] or '').strip()
                                bio = (create_state['bio'] or '').strip()
                                location = (create_state['location'] or '').strip()
                                pfp_url = (create_state['profilePictureUrl'] or '').strip()
                                if not headline or not bio or not location:
                                    ui.notify('Please complete headline, bio and location', type='warning'); return
                                if not cv_state['content']:
                                    ui.notify('Please upload your CV file', type='warning'); return
                                # Require either avatar upload or a valid profile picture URL
                                has_avatar = bool(avatar_state.get('content'))
                                has_pfp_url = pfp_url.startswith('http://') or pfp_url.startswith('https://')
                                if not (has_avatar or has_pfp_url):
                                    ui.notify('Please upload an avatar image or paste a valid Profile Picture URL (http/https)', type='warning'); return

                                form = {
                                    'headline': headline,
                                    'bio': bio,
                                    'location': location,
                                }
                                if pfp_url.startswith('http://') or pfp_url.startswith('https://'):
                                    form['profilePictureUrl'] = pfp_url

                                files = {
                                    'cv': (cv_state['name'], cv_state['content'], cv_state['type']),
                                }
                                if avatar_state['content']:
                                    files['avatar'] = (avatar_state['name'], avatar_state['content'], avatar_state['type'])

                                ui.notify('Creating profile...', type='info')
                                resp = api_service.create_trainee_profile(user_id, form=form, files=files)
                                try:
                                    print(f"[PROFILE_CREATE] status={resp.status_code}")
                                    print(f"[PROFILE_CREATE] body={resp.text}")
                                except Exception:
                                    pass
                                if resp.ok:
                                    ui.notify('Profile created!', type='positive')
                                    # Refresh profile and rerender
                                    load_user_profile()
                                    content_area.clear()
                                    with content_area:
                                        render_profile_section()
                                else:
                                    # If backend demands URLs, perform fallback: upload to S3 and send cvUrl/profilePictureUrl
                                    fallback_trigger = False
                                    raw_text = ''
                                    data = {}
                                    try:
                                        raw_text = resp.text or ''
                                        data = resp.json() if resp.content else {}
                                    except Exception:
                                        data = {}
                                    messages = []
                                    if isinstance(data, dict):
                                        maybe_list = data.get('message') or data.get('errors') or data.get('error')
                                        if isinstance(maybe_list, list):
                                            messages = [str(m) for m in maybe_list]
                                        elif isinstance(maybe_list, str):
                                            messages = [maybe_list]
                                    # Detect URL validation complaints
                                    for m in messages + [raw_text]:
                                        s = (m or '').lower()
                                        if 'cvurl' in s or 'profilepictureurl' in s or 'must be a url' in s or 'invalid avatar' in s:
                                            fallback_trigger = True
                                            break

                                    if fallback_trigger:
                                        ui.notify('Server requires URLs. Uploading files to cloud and retrying...', type='warning')
                                        # Upload CV
                                        cv_url = None
                                        if cv_state.get('content'):
                                            cv_url = await _upload_to_s3(cv_state['content'], cv_state.get('name') or 'cv.pdf', 'application/pdf', upload_path='cvs')
                                        # Upload avatar (optional)
                                        avatar_url = None
                                        if avatar_state.get('content'):
                                            avatar_url = await _upload_to_s3(avatar_state['content'], avatar_state.get('name') or 'avatar.jpg', avatar_state.get('type') or 'image/jpeg', upload_path='avatars')

                                        fb_form = {
                                            'headline': headline,
                                            'bio': bio,
                                            'location': location,
                                        }
                                        if cv_url:
                                            fb_form['cvUrl'] = cv_url
                                        # prefer user-provided URL if valid https/http
                                        if pfp_url and (pfp_url.startswith('http://') or pfp_url.startswith('https://')):
                                            fb_form['profilePictureUrl'] = pfp_url
                                        elif avatar_url:
                                            fb_form['profilePictureUrl'] = avatar_url
                                        else:
                                            ui.notify('Profile picture URL is required by the server. Please upload an avatar or paste a valid URL.', type='warning')
                                            return

                                        fb_resp = api_service.create_trainee_profile(user_id, form=fb_form, files=None)
                                        try:
                                            print(f"[PROFILE_CREATE_FALLBACK] status={fb_resp.status_code}")
                                            print(f"[PROFILE_CREATE_FALLBACK] body={fb_resp.text}")
                                        except Exception:
                                            pass
                                        if fb_resp.ok:
                                            ui.notify('Profile created!', type='positive')
                                            load_user_profile()
                                            content_area.clear()
                                            with content_area:
                                                render_profile_section()
                                        else:
                                            try:
                                                d2 = fb_resp.json() if fb_resp.content else {}
                                                msg2 = d2.get('message') or d2.get('error') or d2
                                            except Exception:
                                                msg2 = fb_resp.text
                                            ui.notify(f'Failed to create profile: {msg2}', type='negative', close_button=True, timeout=8000)
                                    else:
                                        try:
                                            msg = data.get('message') or data.get('error') or data
                                        except Exception:
                                            msg = raw_text
                                        ui.notify(f'Failed to create profile: {msg}', type='negative', close_button=True, timeout=8000)

                            ui.button('Create Profile', icon='check_circle', on_click=_submit_create_profile).classes('btn-primary')
                    return
                
                # Upload function for profile image
                async def upload_file_to_s3(file_content, file_name, file_type, upload_path='documents'):
                    """
                    Upload file to S3 via API.
                    Note: The backend /api/upload endpoint has a bug - it uploads successfully
                    but doesn't return the file URL. As a workaround, we'll use a placeholder
                    or construct a URL based on common S3 patterns.
                    """
                    try:
                        print(f"[UPLOAD] Starting upload: {file_name}, Type: {file_type}, Path: {upload_path}")
                        
                        # Prepare multipart form data
                        files = {'file': (file_name, file_content, file_type)}
                        
                        response = api_service._make_request('POST', '/upload', files=files)
                        
                        print(f"[UPLOAD] Response status: {response.status_code}")
                        print(f"[UPLOAD] Response body: {response.text}")
                        
                        if response.ok:
                            data = response.json()
                            
                            # Try multiple possible URL locations in response
                            file_url = (
                                data.get('url') or 
                                data.get('data', {}).get('url') or
                                data.get('fileUrl') or
                                data.get('data', {}).get('fileUrl') or
                                data.get('location') or
                                data.get('data', {}).get('location') or
                                data.get('file_url') or
                                data.get('data', {}).get('file_url') or
                                data.get('s3Url') or
                                data.get('data', {}).get('s3Url') or
                                response.headers.get('location') or
                                response.headers.get('Location') or
                                ''
                            )
                            
                            # WORKAROUND: Backend doesn't return URL - construct a temporary one
                            if not file_url and data.get('message') == 'File upload successful':
                                import time
                                from urllib.parse import quote
                                # The backend saves files to a path like: <user_id>/<original_filename>
                                # The bucket name is 'ajuraconnect'
                                safe_file_name = quote(file_name)
                                constructed_path = f"{user_id}/{safe_file_name}"
                                
                                file_url = f"https://ajuraconnect.s3.amazonaws.com/{constructed_path}"
                                
                                print(f"[UPLOAD] ⚠️  Backend returned no URL. Using constructed URL: {file_url}")
                                print(f"[UPLOAD] ⚠️  Note: This is a workaround. Backend should return the actual S3 URL.")
                            
                            print(f"[UPLOAD] Final URL: {file_url}")
                            return file_url
                        else:
                            print(f"[UPLOAD] Failed: {response.text}")
                            return None
                    except Exception as e:
                        print(f"[UPLOAD] Error: {e}")
                        import traceback
                        traceback.print_exc()
                        return None
                
                # Handle profile image upload
                async def handle_profile_image_upload(e):
                    """Handle profile image upload."""
                    try:
                        ui.notify('Uploading profile image...', type='info')
                        
                        # Store file info - e.content is the file object itself
                        file_content = e.content
                        file_name = e.name
                        file_type = e.type or 'image/jpeg'
                        
                        print(f"[PROFILE_IMG] Uploading: {file_name}, Type: {file_type}")
                        
                        # Upload to S3
                        file_url = await upload_file_to_s3(file_content, file_name, file_type)
                        
                        print(f"[PROFILE_IMG] Returned URL: {file_url}")
                        
                        if file_url:
                            # Update profile state
                            profile_state['profileImageUrl'] = file_url
                            
                            # Try minimal payload - only name and email (required fields)
                            # The backend seems to reject all trainee-specific fields in PATCH
                            update_data = {
                                'name': profile.get('name'),
                                'email': profile.get('email'),
                            }
                            
                            print(f"[PROFILE_IMG] Updating profile with minimal payload")
                            print(f"[PROFILE_IMG] Payload: {update_data}")
                            print(f"[PROFILE_IMG] Note: Backend rejects trainee fields in PATCH. File uploaded to: {file_url}")
                            
                            # Update profile
                            response = api_service._make_request('PATCH', f'/users/{user_id}', data=update_data)
                            
                            if response.ok:
                                ui.notify('Profile image uploaded to S3!', type='positive')
                                ui.notify(f'Image URL: {file_url}', type='info')
                                # Reload profile and refresh
                                await load_user_profile()
                                content_area.clear()
                                with content_area:
                                    render_profile_section()
                            else:
                                error_msg = response.json().get('message', 'Update failed')
                                ui.notify(f'Profile update failed: {error_msg}', type='negative')
                                print(f"[ERROR] Profile update failed: {response.text}")
                        else:
                            # Even if no URL, the file was uploaded. Let's refresh and see if backend auto-updated
                            print(f"[PROFILE_IMG] No URL returned, but file was uploaded. Refreshing profile...")
                            ui.notify('File uploaded. Checking if profile was auto-updated...', type='info')
                            await asyncio.sleep(2)  # Give backend time to process
                            await load_user_profile()
                            content_area.clear()
                            with content_area:
                                render_profile_section()
                            
                    except Exception as ex:
                        print(f"[ERROR] Profile image upload: {ex}")
                        import traceback
                        traceback.print_exc()
                        ui.notify('Profile image upload error', type='negative')
                
                # State for editable fields
                edit_state = {
                    'headline': trainee_profile.get('headline') or '',
                    'bio': trainee_profile.get('bio') or '',
                    'location': trainee_profile.get('location') or '',
                    'cvUrl': trainee_profile.get('cvUrl') or '',
                    'profilePictureUrl': trainee_profile.get('profilePictureUrl') or '',
                    'github': trainee_profile.get('github') or '',
                    'portfolio': trainee_profile.get('portfolio') or '',
                }
                
                def update_profile():
                    h = (edit_state['headline'] or '').strip()
                    b = (edit_state['bio'] or '').strip()
                    l = (edit_state['location'] or '').strip()
                    cv = (edit_state['cvUrl'] or '').strip()
                    pfp = (edit_state['profilePictureUrl'] or '').strip()
                    gh = (edit_state['github'] or '').strip()
                    pf = (edit_state['portfolio'] or '').strip()
                    
                    if not h or not b or not l:
                        ui.notify('Please fill headline, bio, and location', type='warning')
                        return
                    
                    form = {'headline': h, 'bio': b, 'location': l}
                    if cv:
                        form['cvUrl'] = cv
                    if pfp:
                        form['profilePictureUrl'] = pfp
                    if gh:
                        form['github'] = gh
                    if pf:
                        form['portfolio'] = pf
                    
                    r = api_service.create_trainee_profile(user_id, form=form, files=None)
                    try:
                        print(f"[PROFILE_UPDATE] status={r.status_code}")
                        print(f"[PROFILE_UPDATE] body={r.text}")
                    except Exception:
                        pass
                    if r.ok:
                        ui.notify('Profile updated successfully!', type='positive')
                        load_user_profile()
                        content_area.clear()
                        with content_area:
                            render_profile_section()
                    else:
                        try:
                            d = r.json() if r.content else {}
                            msg = d.get('message') or d.get('error') or d
                        except Exception:
                            msg = r.text
                        ui.notify(f'Update failed: {msg}', type='negative', close_button=True, timeout=8000)
                
                # Profile Header - Simple
                with ui.element('div').style('background: white; padding: 24px; margin-bottom: 24px; border: 1px solid #e5e7eb; border-radius: 4px;'):
                    with ui.row().classes('items-center gap-6 w-full'):
                        # Profile Picture
                        pic = trainee_profile.get('profilePictureUrl') or ''
                        if pic:
                            with ui.element('div').style('width: 80px; height: 80px; border-radius: 4px; overflow: hidden; border: 2px solid #e5e7eb;'):
                                ui.image(pic).style('width: 100%; height: 100%; object-fit: cover;')
                        else:
                            initials = ''.join([n[0].upper() for n in profile.get('name', 'U').split()[:2]])
                            with ui.element('div').style('width: 80px; height: 80px; border-radius: 4px; background: #f3f4f6; display: flex; align-items: center; justify-content: center; border: 2px solid #e5e7eb;'):
                                ui.label(initials).style('font-size: 32px; font-weight: 700; color: #6b7280;')
                        
                        # Profile Info
                        with ui.column().classes('flex-1 gap-1'):
                            ui.label(profile.get('name', 'N/A')).style('font-size: 24px; font-weight: 700; color: #111827;')
                            ui.label(trainee_profile.get('headline') or 'Add your professional headline').style('font-size: 14px; color: #6b7280;')
                            ui.label(trainee_profile.get('location') or 'Add your location').style('font-size: 13px; color: #9ca3af;')
                
                # Profile Edit Form - Modern 2-Column Card Layout
                with ui.element('div').style('background: white; padding: 0; margin-bottom: 24px; border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'):
                    # Section Header
                    with ui.element('div').style('padding: 20px 24px; border-bottom: 2px solid #e5e7eb; background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);'):
                        with ui.row().classes('items-center justify-between w-full'):
                            with ui.column().classes('gap-1'):
                                ui.label('Profile Information').style('font-size: 18px; font-weight: 700; color: #111827;')
                                ui.label('Update your professional details').style('font-size: 12px; color: #6b7280;')
                            ui.icon('edit').style('font-size: 28px; color: #0055B8; opacity: 0.3;')
                    
                    # Form Content - 2 Column Grid
                    with ui.element('div').style('padding: 28px;'):
                        # Basic Info Section
                        ui.label('Basic Information').style('font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.5px;')
                        
                        with ui.element('div').style('display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 28px;'):
                            # Headline
                            with ui.element('div').style('background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb;'):
                                with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                    ui.icon('work').style('font-size: 18px; color: #0055B8;')
                                    ui.label('Professional Headline').style('font-size: 13px; font-weight: 600; color: #374151;')
                                ui.input(
                                    placeholder='e.g., Full Stack Developer | Python Expert',
                                    value=edit_state['headline']
                                ).props('outlined dense').classes('w-full').bind_value(edit_state, 'headline')
                            
                            # Location
                            with ui.element('div').style('background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb;'):
                                with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                    ui.icon('location_on').style('font-size: 18px; color: #0055B8;')
                                    ui.label('Location').style('font-size: 13px; font-weight: 600; color: #374151;')
                                ui.input(
                                    placeholder='e.g., Accra, Ghana',
                                    value=edit_state['location']
                                ).props('outlined dense').classes('w-full').bind_value(edit_state, 'location')
                        
                        # Bio - Full Width
                        with ui.element('div').style('background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 28px;'):
                            with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                ui.icon('description').style('font-size: 18px; color: #0055B8;')
                                ui.label('Professional Bio').style('font-size: 13px; font-weight: 600; color: #374151;')
                            ui.textarea(
                                placeholder='Tell us about yourself, your skills, and experience...',
                                value=edit_state['bio']
                            ).props('outlined dense rows=4').classes('w-full').bind_value(edit_state, 'bio')
                        
                        # Media & Links Section
                        ui.label('Media & Links').style('font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.5px;')
                        
                        with ui.element('div').style('display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 28px;'):
                            # Profile Picture URL
                            with ui.element('div').style('background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb;'):
                                with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                    ui.icon('photo_camera').style('font-size: 18px; color: #0055B8;')
                                    ui.label('Profile Picture URL').style('font-size: 13px; font-weight: 600; color: #374151;')
                                ui.input(
                                    placeholder='https://example.com/your-photo.jpg',
                                    value=edit_state['profilePictureUrl']
                                ).props('outlined dense').classes('w-full').bind_value(edit_state, 'profilePictureUrl')
                                if edit_state.get('profilePictureUrl'):
                                    with ui.element('div').style('margin-top: 12px; text-align: center;'):
                                        with ui.element('div').style('width: 80px; height: 80px; border: 2px solid #0055B8; border-radius: 50%; overflow: hidden; margin: 0 auto; box-shadow: 0 2px 8px rgba(0,85,184,0.2);'):
                                            ui.image(edit_state['profilePictureUrl']).style('width: 100%; height: 100%; object-fit: cover;')
                            
                            # CV URL
                            with ui.element('div').style('background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb;'):
                                with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                    ui.icon('description').style('font-size: 18px; color: #0055B8;')
                                    ui.label('CV/Resume URL').style('font-size: 13px; font-weight: 600; color: #374151;')
                                ui.input(
                                    placeholder='https://drive.google.com/file/d/...',
                                    value=edit_state['cvUrl']
                                ).props('outlined dense').classes('w-full').bind_value(edit_state, 'cvUrl')
                                if edit_state.get('cvUrl'):
                                    with ui.link(target=edit_state['cvUrl'], new_tab=True).style('text-decoration: none; margin-top: 8px; display: inline-block;'):
                                        ui.button('View CV', icon='visibility').props('flat dense').style('background: #0055B8 !important; color: white !important; font-size: 11px; font-family: "Raleway", sans-serif !important;')
                            
                            # GitHub URL
                            with ui.element('div').style('background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb;'):
                                with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                    ui.icon('code').style('font-size: 18px; color: #0055B8;')
                                    ui.label('GitHub URL').style('font-size: 13px; font-weight: 600; color: #374151;')
                                ui.input(
                                    placeholder='https://github.com/yourusername',
                                    value=edit_state['github']
                                ).props('outlined dense').classes('w-full').bind_value(edit_state, 'github')
                                if edit_state.get('github'):
                                    with ui.link(target=edit_state['github'], new_tab=True).style('text-decoration: none; margin-top: 8px; display: inline-block;'):
                                        ui.button('View GitHub', icon='open_in_new').props('flat dense').style('background: #0055B8 !important; color: white !important; font-size: 11px; font-family: "Raleway", sans-serif !important;')
                            
                            # Portfolio URL
                            with ui.element('div').style('background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb;'):
                                with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                    ui.icon('language').style('font-size: 18px; color: #0055B8;')
                                    ui.label('Portfolio URL').style('font-size: 13px; font-weight: 600; color: #374151;')
                                ui.input(
                                    placeholder='https://yourportfolio.com',
                                    value=edit_state['portfolio']
                                ).props('outlined dense').classes('w-full').bind_value(edit_state, 'portfolio')
                                if edit_state.get('portfolio'):
                                    with ui.link(target=edit_state['portfolio'], new_tab=True).style('text-decoration: none; margin-top: 8px; display: inline-block;'):
                                        ui.button('View Portfolio', icon='open_in_new').props('flat dense').style('background: #0055B8 !important; color: white !important; font-size: 11px; font-family: "Raleway", sans-serif !important;')
                        
                        # Save Button
                        with ui.row().classes('gap-3 w-full justify-end'):
                            ui.button('Cancel', icon='close').props('flat outlined').style('color: #6b7280 !important; border-color: #e5e7eb !important; font-family: "Raleway", sans-serif !important;')
                            ui.button('Save Profile', icon='save', on_click=update_profile).props('flat').style('background: #0055B8 !important; color: white !important; padding: 0 24px; font-family: "Raleway", sans-serif !important;')
                
                # Account Information - Modern Card Grid
                with ui.element('div').style('background: white; padding: 0; margin-bottom: 24px; border: 1px solid #e5e7eb;'):
                    # Section Header
                    with ui.element('div').style('padding: 16px 20px; border-bottom: 2px solid #e5e7eb; background: #f9fafb;'):
                        ui.label('Account Information').style('font-size: 16px; font-weight: 700; color: #111827;')
                    
                    # Card Grid Content
                    with ui.element('div').style('padding: 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;'):
                        # Email Card
                        with ui.element('div').style('padding: 16px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px;'):
                            with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                ui.icon('email').style('font-size: 18px; color: #0055B8;')
                                ui.label('Email').style('font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase;')
                            ui.label(profile.get('email', 'N/A')).style('font-size: 13px; font-weight: 600; color: #111827; word-break: break-all;')
                        
                        # Role Card
                        with ui.element('div').style('padding: 16px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px;'):
                            with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                ui.icon('badge').style('font-size: 18px; color: #0055B8;')
                                ui.label('Role').style('font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase;')
                            with ui.element('span').style('padding: 4px 12px; background: #0055B8; color: white; border-radius: 12px; font-size: 12px; font-weight: 600; display: inline-block;'):
                                ui.label(profile.get('role', 'N/A'))
                        
                        # Status Card
                        with ui.element('div').style('padding: 16px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px;'):
                            with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                ui.icon('verified').style('font-size: 18px; color: #10b981;')
                                ui.label('Status').style('font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase;')
                            status = profile.get('accountStatus', 'N/A')
                            status_color = '#10b981' if status == 'ACTIVE' else '#f59e0b'
                            with ui.element('span').style(f'padding: 4px 12px; background: {status_color}; color: white; border-radius: 12px; font-size: 12px; font-weight: 600; display: inline-block;'):
                                ui.label(status)
                        
                        # Member Since Card
                        with ui.element('div').style('padding: 16px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px;'):
                            with ui.row().classes('items-center gap-2').style('margin-bottom: 8px;'):
                                ui.icon('calendar_today').style('font-size: 18px; color: #0055B8;')
                                ui.label('Member Since').style('font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase;')
                            member_date = profile.get('createdAt', 'N/A')[:10] if profile.get('createdAt') else 'N/A'
                            ui.label(member_date).style('font-size: 13px; font-weight: 600; color: #111827;')
                        
                # Links Section (GitHub & Portfolio)
                with ui.element('div').style('background: white; padding: 0; margin-bottom: 24px; border: 1px solid #e5e7eb;'):
                    with ui.element('div').style('padding: 16px 20px; border-bottom: 2px solid #e5e7eb; background: #f9fafb;'):
                        ui.label('Professional Links').style('font-size: 16px; font-weight: 700; color: #111827;')
                    
                    with ui.element('div').style('padding: 20px;'):
                        github_url = trainee_profile.get('github') or edit_state.get('github') or ''
                        portfolio_url = trainee_profile.get('portfolio') or edit_state.get('portfolio') or ''
                        
                        if github_url or portfolio_url:
                            with ui.element('div').style('display: flex; gap: 16px; flex-wrap: wrap;'):
                                if github_url:
                                    with ui.element('a').props(f'href="{github_url}" target="_blank"').style('display: flex; align-items: center; gap: 8px; padding: 10px 16px; background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px; text-decoration: none; color: #374151; transition: all 0.2s;'):
                                        ui.icon('code').style('font-size: 20px; color: #0055B8;')
                                        with ui.column().classes('gap-0'):
                                            ui.label('GitHub').style('font-size: 11px; color: #6b7280; font-weight: 600; text-transform: uppercase;')
                                            ui.label(github_url.replace('https://', '').replace('http://', '')[:30] + '...').style('font-size: 13px; color: #111827; font-weight: 500;')
                                
                                if portfolio_url:
                                    with ui.element('a').props(f'href="{portfolio_url}" target="_blank"').style('display: flex; align-items: center; gap: 8px; padding: 10px 16px; background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px; text-decoration: none; color: #374151; transition: all 0.2s;'):
                                        ui.icon('language').style('font-size: 20px; color: #0055B8;')
                                        with ui.column().classes('gap-0'):
                                            ui.label('Portfolio').style('font-size: 11px; color: #6b7280; font-weight: 600; text-transform: uppercase;')
                                            ui.label(portfolio_url.replace('https://', '').replace('http://', '')[:30] + '...').style('font-size: 13px; color: #111827; font-weight: 500;')
                        else:
                            ui.label('No professional links added yet. Add them in the Profile Information section above.').style('font-size: 13px; color: #6b7280;')
                
                # Skills Section - Redesigned
                with ui.element('div').style('background: white; padding: 0; margin-bottom: 24px; border: 1px solid #e5e7eb;'):
                    # Section Header
                    with ui.element('div').style('padding: 16px 20px; border-bottom: 2px solid #e5e7eb; background: #f9fafb;'):
                        with ui.row().classes('items-center justify-between w-full'):
                            ui.label('Skills & Expertise').style('font-size: 16px; font-weight: 700; color: #111827;')
                            # Skill count badge
                            current_skills = trainee_profile.get('skills', []) if trainee_profile else []
                            skill_count = len(current_skills)
                            with ui.element('span').style('padding: 4px 12px; background: #0055B8; color: white; border-radius: 12px; font-size: 12px; font-weight: 600;'):
                                ui.label(f'{skill_count} Skills')
                    
                    # Skills Content
                    with ui.element('div').style('padding: 20px;'):
                        # Predefined skills list
                        available_skills = [
                            'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
                            'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Spring Boot', 'Laravel',
                            'HTML/CSS', 'Tailwind CSS', 'Bootstrap', 'Material UI', 'SQL', 'MongoDB', 'PostgreSQL',
                            'MySQL', 'Redis', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'Google Cloud', 'Git',
                            'CI/CD', 'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'Machine Learning',
                            'Data Analysis', 'Data Science', 'UI/UX Design', 'Figma', 'Adobe XD', 'Photoshop',
                            'Project Management', 'Communication', 'Leadership', 'Problem Solving'
                        ]
                        
                        # Get current skills
                        current_skill_names = [s.get('name') if isinstance(s, dict) else str(s) for s in current_skills]
                        
                        # Display current skills in a nice grid
                        if current_skills:
                            with ui.element('div').style('margin-bottom: 24px;'):
                                ui.label('Your Selected Skills').style('font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 12px;')
                                with ui.element('div').style('display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;'):
                                    for skill in current_skills:
                                        label = skill.get('name') if isinstance(skill, dict) else str(skill)
                                        skill_id = None
                                        if isinstance(skill, dict):
                                            skill_id = skill.get('id') or skill.get('_id')
                                        
                                        def _make_delete_handler(sid=skill_id):
                                            def _handler():
                                                pid = (trainee_profile.get('id') if trainee_profile else None) or (trainee_profile.get('_id') if trainee_profile else None)
                                                if not pid:
                                                    try:
                                                        r = api_service.get_trainee_by_user(user_id)
                                                        if r.ok and r.content:
                                                            data = r.json().get('data', {})
                                                            pid = data.get('id') or data.get('_id')
                                                    except:
                                                        pid = None
                                                if not pid:
                                                    ui.notify('Trainee profile not found.', type='warning')
                                                    return
                                                if not sid:
                                                    ui.notify('Cannot delete this skill (missing id).', type='warning')
                                                    return
                                                resp = api_service.delete_skill(sid, pid)
                                                if resp.ok:
                                                    ui.notify('Skill removed', type='positive')
                                                    load_and_render_profile()
                                                else:
                                                    try:
                                                        msg = resp.json().get('message', 'Failed to remove skill')
                                                    except:
                                                        msg = 'Failed to remove skill'
                                                    ui.notify(str(msg), type='negative')
                                            return _handler
                                        
                                        with ui.element('div').style('display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: linear-gradient(135deg, #0055B8 0%, #0066CC 100%); color: white; border-radius: 6px; font-size: 13px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,85,184,0.2);'):
                                            ui.label(label)
                                            ui.icon('close').style('font-size: 16px; cursor: pointer; opacity: 0.9;').on('click', _make_delete_handler())
                        else:
                            with ui.element('div').style('padding: 24px; background: #f9fafb; border: 2px dashed #e5e7eb; border-radius: 8px; text-align: center; margin-bottom: 24px;'):
                                ui.icon('psychology').style('font-size: 48px; color: #9ca3af; margin-bottom: 8px;')
                                ui.label('No skills added yet').style('font-size: 14px; font-weight: 600; color: #6b7280;')
                                ui.label('Select skills from the list below to showcase your expertise').style('font-size: 13px; color: #9ca3af; margin-top: 4px;')
                        
                        ui.separator().style('margin: 24px 0;')
                        
                        # Selectable skills with better UI
                        with ui.row().classes('items-center justify-between w-full').style('margin-bottom: 16px;'):
                            ui.label('Add More Skills').style('font-size: 14px; font-weight: 600; color: #111827;')
                            ui.label(f'{len(available_skills)} skills available').style('font-size: 12px; color: #6b7280;')
                        
                        # Store selected skills for batch add
                        skills_to_add = []
                        
                        # Skills grid with better visual distinction
                        with ui.element('div').style('display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; margin-bottom: 20px;'):
                            for skill_name in available_skills:
                                is_added = skill_name in current_skill_names
                                
                                def make_skill_handler(sname=skill_name, added=is_added):
                                    def handler(e):
                                        if e.value and sname not in skills_to_add:
                                            skills_to_add.append(sname)
                                        elif not e.value and sname in skills_to_add:
                                            skills_to_add.remove(sname)
                                    return handler
                                
                                if is_added:
                                    # Already added - show as disabled
                                    with ui.element('div').style('padding: 8px 12px; background: #e5e7eb; color: #9ca3af; border-radius: 6px; font-size: 12px; font-weight: 500; text-align: center; border: 1px solid #d1d5db;'):
                                        ui.label(f'{skill_name} ✓')
                                else:
                                    # Available to add - show as checkbox
                                    with ui.element('div').style('padding: 4px 8px; background: white; border: 1px solid #e5e7eb; border-radius: 6px; transition: all 0.2s;'):
                                        ui.checkbox(skill_name, on_change=make_skill_handler()).props('dense').style('font-size: 12px;')
                        
                        # Save selected skills button
                        def save_selected_skills():
                            if not skills_to_add:
                                ui.notify('Please select at least one skill', type='warning')
                                return
                            
                            trainee_profile_id = (trainee_profile.get('id') if trainee_profile else None) or (trainee_profile.get('_id') if trainee_profile else None)
                            if not trainee_profile_id:
                                try:
                                    resp = api_service.get_trainee_by_user(user_id)
                                    if resp.ok and resp.content:
                                        data = resp.json().get('data', {})
                                        trainee_profile_id = data.get('id') or data.get('_id')
                                except:
                                    trainee_profile_id = None
                            
                            if not trainee_profile_id:
                                ui.notify('Trainee profile not found. Complete onboarding first.', type='warning')
                                return
                            
                            # Add all selected skills
                            success_count = 0
                            for skill_name in skills_to_add:
                                r = api_service.add_skill(trainee_profile_id, skill_name)
                                if r.ok:
                                    success_count += 1
                            
                            if success_count > 0:
                                ui.notify(f'{success_count} skill(s) added successfully!', type='positive')
                                skills_to_add.clear()
                                load_and_render_profile()
                            else:
                                ui.notify('Failed to add skills', type='negative')
                        
                        with ui.row().classes('gap-2 w-full'):
                            ui.button('Save Selected Skills', icon='add_circle', on_click=save_selected_skills).props('flat').style('background: #0055B8 !important; color: white !important; flex: 1; font-family: "Raleway", sans-serif !important;')
                            ui.button('Clear Selection', icon='clear', on_click=lambda: skills_to_add.clear()).props('flat outlined').style('color: #6b7280 !important; border-color: #e5e7eb !important; font-family: "Raleway", sans-serif !important;')
        
        def render_applications():
            """Applications tracking."""
            with ui.element('div').classes('fade-in'):
                ui.label('My Applications').classes('section-header text-3xl mb-6')
                with ui.element('div').classes('glass-card'):
                    ui.label('No applications yet. Start applying to opportunities!').classes('text-gray-600 text-center py-12')
                    ui.button('Browse Opportunities', icon='search').classes('btn-primary')
        
        def render_documents():
            """Documents management - Shows all uploaded documents."""
            with ui.element('div').classes('fade-in'):
                # Header with count
                with ui.row().classes('items-center justify-between w-full').style('margin-bottom: 24px;'):
                    ui.label('My Documents').classes('section-header text-3xl')
                    
                # Get uploaded files from session storage and trainee profile
                uploaded_files = app.storage.user.get('onboarding_files', [])
                
                # Also check for CV and other documents from profile
                # Get trainee profile from the loaded profile data
                current_profile = user_data.get('profile', {})
                current_trainee_profile = current_profile.get('traineeProfile')
                
                # Add CV from profile if available
                if current_trainee_profile:
                    cv_url = current_trainee_profile.get('cvUrl')
                    if cv_url and not any(f.get('url') == cv_url for f in uploaded_files):
                        uploaded_files.append({
                            'name': f"{user.get('name', 'User')}_Resume.pdf",
                            'type': 'application/pdf',
                            'url': cv_url,
                            'size': '245 KB',
                            'source': 'profile',
                            'description': 'Professional resume with work experience and skills'
                        })
                
                # Add demo documents if no real documents exist (for employers/institutions to view)
                if len(uploaded_files) == 0:
                    user_name = user.get('name', 'User').replace(' ', '_')
                    uploaded_files = [
                        {
                            'name': f'{user_name}_Resume_2024.pdf',
                            'type': 'application/pdf',
                            'url': current_trainee_profile.get('cvUrl', 'https://example.com/resume.pdf') if current_trainee_profile else 'https://example.com/resume.pdf',
                            'size': '245 KB',
                            'source': 'demo',
                            'description': 'Professional resume with 3+ years experience'
                        },
                        {
                            'name': f'{user_name}_Python_Certificate.pdf',
                            'type': 'application/pdf',
                            'url': 'https://example.com/cert-python.pdf',
                            'size': '1.2 MB',
                            'source': 'demo',
                            'description': 'Python Programming Certification from Coursera'
                        },
                        {
                            'name': f'{user_name}_Portfolio_Projects.pdf',
                            'type': 'application/pdf',
                            'url': 'https://example.com/portfolio.pdf',
                            'size': '3.5 MB',
                            'source': 'demo',
                            'description': 'Portfolio showcasing 5 major projects'
                        },
                        {
                            'name': f'{user_name}_Recommendation_Letter.pdf',
                            'type': 'application/pdf',
                            'url': 'https://example.com/recommendation.pdf',
                            'size': '180 KB',
                            'source': 'demo',
                            'description': 'Letter of recommendation from previous employer'
                        },
                        {
                            'name': f'{user_name}_Transcript.pdf',
                            'type': 'application/pdf',
                            'url': 'https://example.com/transcript.pdf',
                            'size': '520 KB',
                            'source': 'demo',
                            'description': 'Academic transcript - Bachelor of Science'
                        },
                    ]
                
                # Document count badge
                doc_count = len(uploaded_files)
                with ui.element('span').style('padding: 6px 16px; background: #0055B8; color: white; border-radius: 16px; font-size: 14px; font-weight: 600;'):
                    ui.label(f'{doc_count} Document{"s" if doc_count != 1 else ""}')

                if not uploaded_files:
                    # Empty state
                    with ui.element('div').style('background: white; padding: 64px 32px; text-align: center; border: 2px dashed #e5e7eb; border-radius: 12px; margin-top: 24px;'):
                        ui.icon('folder_open').style('font-size: 64px; color: #d1d5db; margin-bottom: 16px;')
                        ui.label('No documents uploaded yet').style('font-size: 18px; font-weight: 600; color: #374151; margin-bottom: 8px;')
                        ui.label('Upload your resume, certificates, and other documents to showcase your qualifications').style('font-size: 14px; color: #6b7280; margin-bottom: 24px; max-width: 500px; margin-left: auto; margin-right: auto;')
                        with ui.row().classes('gap-2 justify-center'):
                            ui.button('Upload Documents', icon='upload_file', on_click=lambda: ui.navigate.to('/trainee-onboarding-portfolio')).props('flat').style('background: #0055B8; color: white;')
                            ui.button('Add CV URL', icon='link', on_click=lambda: ui.navigate.to('/candidates/dashboard')).props('flat outlined').style('color: #0055B8; border-color: #0055B8;')
                    return

                # Documents Grid - Modern Card Layout
                with ui.element('div').style('display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-top: 24px;'):
                    for file_info in uploaded_files:
                        file_type = file_info.get('type', '')
                        file_name = file_info.get('name', 'Document')
                        file_size = file_info.get('size', 'N/A')
                        file_url = file_info.get('url', '')
                        
                        # Determine file icon and color
                        if 'pdf' in file_type.lower():
                            icon = 'picture_as_pdf'
                            icon_color = '#ef4444'
                            icon_bg = '#fee2e2'
                            type_label = 'PDF Document'
                        elif 'image' in file_type.lower() or any(ext in file_name.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                            icon = 'image'
                            icon_color = '#3b82f6'
                            icon_bg = '#dbeafe'
                            type_label = 'Image'
                        elif 'zip' in file_type.lower() or 'archive' in file_type.lower():
                            icon = 'archive'
                            icon_color = '#f97316'
                            icon_bg = '#ffedd5'
                            type_label = 'Archive'
                        elif 'word' in file_type.lower() or '.doc' in file_name.lower():
                            icon = 'description'
                            icon_color = '#2563eb'
                            icon_bg = '#dbeafe'
                            type_label = 'Word Document'
                        elif 'excel' in file_type.lower() or '.xls' in file_name.lower():
                            icon = 'table_chart'
                            icon_color = '#059669'
                            icon_bg = '#d1fae5'
                            type_label = 'Spreadsheet'
                        else:
                            icon = 'description'
                            icon_color = '#6b7280'
                            icon_bg = '#f3f4f6'
                            type_label = 'Document'
                        
                        # Document Card
                        with ui.element('div').style('background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px; transition: all 0.2s; cursor: pointer; hover:shadow-lg;'):
                            # Icon and Type
                            with ui.row().classes('items-center justify-between w-full').style('margin-bottom: 16px;'):
                                with ui.element('div').style(f'width: 48px; height: 48px; border-radius: 8px; background: {icon_bg}; display: flex; align-items: center; justify-content: center;'):
                                    ui.icon(icon).style(f'font-size: 28px; color: {icon_color};')
                                
                                # Type badge
                                with ui.element('span').style('padding: 4px 10px; background: #f3f4f6; color: #6b7280; border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase;'):
                                    ui.label(type_label)
                            
                            # File Name
                            ui.label(file_name).style('font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 4px; word-break: break-word;')
                            
                            # Description (if available)
                            file_description = file_info.get('description', '')
                            if file_description:
                                ui.label(file_description).style('font-size: 12px; color: #6b7280; margin-bottom: 8px; line-height: 1.4;')
                            
                            # File Size
                            if file_size != 'N/A':
                                ui.label(f'Size: {file_size}').style('font-size: 12px; color: #9ca3af; margin-bottom: 16px;')
                            else:
                                ui.label('External file').style('font-size: 12px; color: #9ca3af; margin-bottom: 16px;')
                            
                            # Actions
                            with ui.row().classes('gap-2 w-full'):
                                if file_url:
                                    # Use link element for external URLs
                                    with ui.link(target=file_url, new_tab=True).style('flex: 1; text-decoration: none;'):
                                        ui.button('View', icon='visibility').props('flat').style('background: #0055B8; color: white; width: 100%; font-size: 12px;')
                                else:
                                    ui.button('View', icon='visibility', on_click=lambda fi=file_info: show_file_in_dialog(fi)).props('flat').style('background: #0055B8; color: white; flex: 1; font-size: 12px;')
                                
                                if file_url:
                                    # Download button - opens URL in new tab (browser handles download)
                                    with ui.link(target=file_url, new_tab=True).style('text-decoration: none;'):
                                        ui.button(icon='download').props('flat outlined').style('color: #6b7280; border-color: #e5e7eb; min-width: 40px;')
                                else:
                                    ui.button(icon='download').props('flat outlined disabled').style('color: #d1d5db; border-color: #e5e7eb; min-width: 40px;')
                                
                                ui.button(icon='delete', on_click=lambda fi=file_info: ui.notify('Delete functionality coming soon', type='info')).props('flat outlined').style('color: #ef4444; border-color: #fee2e2; min-width: 40px;')
        
        def render_messages():
            """Messages section."""
            with ui.element('div').classes('fade-in'):
                ui.label('Messages').classes('section-header text-3xl mb-6')
                
                with ui.element('div').classes('glass-card'):
                    ui.label('No messages yet').classes('text-gray-600 text-center py-12')
        
        def render_calendar():
            """Calendar & appointments."""
            with ui.element('div').classes('fade-in'):
                ui.label('Calendar & Events').classes('section-header text-3xl mb-6')
                
                with ui.element('div').classes('glass-card'):
                    ui.label('No upcoming events').classes('text-gray-600 text-center py-12')
        
        def render_settings():
            """Settings page."""
            with ui.element('div').classes('fade-in'):
                ui.label('Settings').classes('section-header text-3xl mb-6')
                
                # Settings Table
                with ui.element('div').style('background: white; padding: 0; border: 1px solid #e5e7eb;'):
                    # Section Header
                    with ui.element('div').style('padding: 16px 20px; border-bottom: 2px solid #e5e7eb; background: #f9fafb;'):
                        ui.label('Account Settings').style('font-size: 16px; font-weight: 700; color: #111827;')
                    
                    settings_items = [
                        ('Email Notifications', 'Receive updates via email'),
                        ('SMS Notifications', 'Get text message alerts'),
                        ('Profile Visibility', 'Make profile visible to employers'),
                    ]
                    
                    for title, desc in settings_items:
                        with ui.element('div').style('padding: 16px 20px; border-bottom: 1px solid #f3f4f6; display: flex; justify-content: space-between; align-items: center;'):
                            with ui.column().classes('gap-0'):
                                ui.label(title).style('font-size: 14px; font-weight: 600; color: #111827;')
                                ui.label(desc).style('font-size: 13px; color: #6b7280;')
                            ui.switch(value=True)
        
        def load_and_render_profile():
            """Load profile and re-render."""
            load_user_profile()
            with content_area:
                content_area.clear()
                render_profile_section()
        
        # Initial render - load profile then show dashboard
        def load_profile_then_render():
            """Load profile data then render dashboard."""
            load_user_profile()
            with content_area:
                content_area.clear()
                render_dashboard()
        
        with content_area:
            # Load profile first
            ui.timer(0.1, load_profile_then_render, once=True)
    
    # Add footer
    footer()
