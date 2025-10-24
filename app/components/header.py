from nicegui import ui
from app.services.auth_utils import is_authenticated, get_current_user, logout


def _allow_all_html(*args):
    return args[-1] if args else ''


def _build_resources_html(current_page: str, links: list[dict]) -> str:
    items = []
    for link in links:
        active_class = "active" if current_page.startswith(link["path"]) else ""
        items.append(
            f'<a href="{link["path"]}" class="nav-dropdown-btn {active_class}">{link["name"]}</a>'
        )
    return '<div class="flex flex-col p-2">' + ''.join(items) + '</div>'

def add_global_styles():
    """Add global styles - call this once per page that needs it"""
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    ui.add_head_html(r'''
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        /* Brand typography - excludes icons to prevent font override */
        *:not(.material-icons):not(.q-icon):not([class*="material-icons"]):not(i) {
            font-family: 'Raleway', sans-serif !important;
        }

        /* Material Icons properties */
        .material-icons {
            font-family: 'Material Icons' !important;
            font-weight: normal;
            font-style: normal;
            font-size: 24px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
            -webkit-font-feature-settings: 'liga';
        }

        /* Ensure header styling takes precedence */
        header {
            background-color: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(8px) !important;
            border-bottom: 1px solid #e5e7eb !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 1000 !important;
            height: 64px !important;
        }

        /* Button styling protection - Brand Guidelines */
        .q-btn, button {
            font-family: 'Raleway', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            transition: all 0.2s ease !important;
        }
        
        .q-btn:hover, button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 85, 184, 0.2);
        }

        /* Primary button styles - Brand Guidelines */
        .brand-primary-btn {
            background-color: #0055B8 !important;
            color: white !important;
            border: none !important;
        }
        
        .brand-primary-btn:hover {
            background-color: #004494 !important;
            opacity: 0.9 !important;
        }
        
        .brand-secondary-btn {
            background-color: white !important;
            color: #0055B8 !important;
            border: 2px solid #0055B8 !important;
        }
        
        .brand-secondary-btn:hover {
            background-color: #F2F7FB !important;
        }

        /* Secondary button styles */
        .bg-gray-200 {
            background-color: #f3f4f6 !important;
            color: #1f2937 !important;
        }

        .bg-gray-200:hover, .hover\:bg-gray-300:hover {
            background-color: #e5e7eb !important;
        }

        /* Danger button styles */
        .bg-red-600 {
            background-color: #dc2626 !important;
            color: white !important;
        }

        .bg-red-600:hover, .hover\:bg-red-700:hover {
            background-color: #b91c1c !important;
        }

        /* Ensure header is always visible */
        header {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        .nicegui-content,
        .nicegui-column {
            display: block !important;
            flex-direction: unset !important;
            align-items: unset !important;
            gap: 0 !important;
            padding: 0 !important;
        }

        /* Typography classes */
        .heading-1 { font-size: 3rem; font-weight: 700; line-height: 1.1; }
        .heading-2 { font-size: 2.25rem; font-weight: 600; line-height: 1.2; }
        .sub-heading { font-size: 1.5rem; font-weight: 500; line-height: 1.4; }
        .body-text { font-size: 1rem; font-weight: 400; line-height: 1.6; }
        .button-label { font-size: 0.875rem; font-weight: 600; }
        .caption { font-size: 0.75rem; font-weight: 400; }

        /* Brand colors */
        .brand-primary { color: #0055B8; }
        .brand-charcoal { color: #1A1A1A; }
        .brand-slate { color: #4D4D4D; }
        .brand-light-mist { background-color: #F2F7FB; }
        .brand-primary-bg { background-color: #0055B8; }

        /* Content spacing to prevent overlap with fixed header */
        .main-content {
            margin-top: 4rem !important; /* 64px to match header height */
            padding-top: 1rem !important;
        }

        /* Ensure all page containers have proper spacing */
        .q-page, .page-container, .nicegui-content > div:first-child {
            margin-top: 4rem !important;
        }

        /* Override any conflicting padding/margin on main content areas */
        .nicegui-content .q-page-container,
        .nicegui-content > .q-column,
        .nicegui-content > div.flex.flex-col {
            padding-top: 4rem !important;
        }

        /* Fix header overlap issue - increase pt-20 to account for fixed header */
        .pt-20 {
            padding-top: 4.375rem !important; /* 70px - 64px header + 6px spacing */
        }

        /* Desktop navigation visibility */
        @media (min-width: 1024px) {
            .lg\:\!flex {
                display: flex !important;
            }
        }
        
        /* Mobile responsive styles */
        @media (max-width: 1023px) {
            header {
                padding: 0 1rem !important;
            }
            
            .logo-text {
                font-size: 1.125rem !important;
            }
        }
        
        @media (max-width: 640px) {
            header {
                padding: 0 0.75rem !important;
            }
            
            .logo-text {
                font-size: 1rem !important;
            }
            
            .logo-icon {
                font-size: 1.5rem !important;
            }
        }

        /* Mobile drawer styles */
        .q-drawer {
            background: white !important;
            z-index: 10000 !important;
        }
        
        .q-drawer--right {
            right: 0 !important;
        }
        
        .q-drawer__backdrop {
            z-index: 9999 !important;
        }
        
        /* Menu styles */
        .q-menu {
            background: white !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
            padding: 8px 0 !important;
            min-width: 200px !important;
        }

        .q-item {
            padding: 12px 16px !important;
            color: #374151 !important;
            font-family: 'Raleway', sans-serif !important;
            font-weight: 400 !important;
            transition: background-color 0.2s ease !important;
            cursor: pointer !important;
        }

        .q-item:hover {
            background-color: #f3f4f6 !important;
            color: #0055B8 !important;
        }

        /* Hover dropdown styles */
        .dropdown-hover {
            position: relative;
        }

        .dropdown-hover .dropdown-content {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            padding: 8px 0;
            min-width: 200px;
            z-index: 1000;
        }

        .dropdown-hover:hover .dropdown-content {
            display: block;
        }

        .dropdown-content a {
            display: block;
            padding: 12px 16px;
            color: #374151;
            text-decoration: none;
            font-family: 'Raleway', sans-serif;
            font-weight: 400;
            transition: background-color 0.2s ease;
        }

        .dropdown-content a:hover {
            background-color: #f3f4f6;
            color: #0055B8;
        }

        /* Navigation button styles */
        .nav-dropdown-btn {
            background: transparent !important;
            border: none !important;
            color: #334155 !important; /* slate-700 */
            font-weight: 600 !important;
            font-family: 'Raleway', sans-serif !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
        }

        .nav-dropdown-btn:hover {
            color: #0f172a !important; /* slate-900 */
            background-color: #f8fafb !important;
        }

        .dropdown-toggle {
            display: flex !important;
            align-items: center !important;
            gap: 4px !important;
            color: #4b5563 !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
            background: transparent !important;
            border: none !important;
            font-family: 'Raleway', sans-serif !important;
        }

        .dropdown-toggle:hover {
            color: #1f2937 !important;
            background-color: #f9fafb !important;
        }

        /* Ensure dropdown menus are always visible */
        .q-btn-dropdown {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Active navigation states */
        /* Top-level link styles */
        .top-nav-link {
            color: #334155 !important;
            font-weight: 600 !important;
            padding: 6px 10px !important;
            border-radius: 6px !important;
            text-decoration: none !important;
            transition: color .2s ease, background .2s ease !important;
        }

        .top-nav-link:hover {
            color: #0f172a !important;
            background: #f8fafb !important;
        }

        .nav-active {
            color: #0055B8 !important;
            font-weight: 700 !important;
            position: relative;
        }

        .nav-active::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            right: 0;
            height: 3px;
            background-color: #0055B8;
            border-radius: 2px;
        }

        .dropdown-active {
            color: #0055B8 !important;
            font-weight: 600 !important;
        }

        .dropdown-active .dropdown-icon {
            color: #0055B8 !important;
        }

        /* Active dropdown content item */
        .dropdown-content a.active {
            background-color: #f0f8ff !important;
            color: #0055B8 !important;
            font-weight: 500 !important;
            border-left: 3px solid #0055B8;
            padding-left: 13px !important;
        }
    </style>
    ''')

def header(current_page: str = ''):
    add_global_styles()
    resource_links = [
        {'name': 'Contact Us', 'path': '/contact'},
        {'name': 'Trainings/Bootcamps', 'path': '/training-program-directory'},
        {'name': 'Success Stories', 'path': '/candidates/success-stories'},
        {'name': 'Help & Support', 'path': '/help-and-support'},
    ]

    # Determine active states for navigation highlighting
    home_active = current_page == '/'
    about_active = current_page == '/about'
    how_active = current_page.startswith('/how-it-works')
    resources_active = any(current_page.startswith(link['path']) for link in resource_links)

    # Authentication context
    authenticated = is_authenticated()
    user = get_current_user() if authenticated else None
    user_name = user.get('name', user.get('email', 'User')) if user else 'User'
    user_role = user.get('role', 'USER') if user else 'USER'
    profile_pic_url = ''
    if user:
        trainee_profile = user.get('traineeProfile', {})
        profile_pic_url = trainee_profile.get('profilePictureUrl', '') if trainee_profile else ''

    mobile_drawer = ui.drawer('right', value=False).props('overlay bordered').classes('!w-80 pt-6 pr-4 pl-4').style('z-index: 10000 !important;')

    def close_drawer() -> None:
        mobile_drawer.value = False
        mobile_drawer.update()

    def open_drawer() -> None:
        mobile_drawer.value = True
        mobile_drawer.update()

    def navigate_and_close(path: str) -> None:
        ui.navigate.to(path)
        close_drawer()

    def logout_and_close() -> None:
        logout()
        close_drawer()

    def mobile_nav_link(label: str, path: str, active: bool = False) -> None:
        base_classes = 'block w-full px-4 py-3 rounded-lg text-base font-medium text-slate-700 hover:bg-blue-50 hover:text-blue-600 transition'
        active_classes = ' bg-blue-50 text-blue-600 font-semibold' if active else ''
        link = ui.link(label, path)
        link.classes(base_classes + active_classes)
        link.on('click', lambda _: navigate_and_close(path))

    with mobile_drawer:
        with ui.column().classes('h-full w-full justify-between gap-6'):
            with ui.column().classes('w-full gap-4'):
                ui.button(icon='close', on_click=close_drawer).props('flat round dense').classes('self-end text-gray-500 hover:text-gray-800')

                mobile_nav_items = [
                    ('Home', '/', home_active),
                    ('About Us', '/about', about_active),
                    ('How it works', '/how-it-works', how_active),
                ]

                for label, path, active in mobile_nav_items:
                    mobile_nav_link(label, path, active)

                # Resources dropdown in mobile menu
                if resource_links:
                    ui.separator().classes('my-2')
                    
                    with ui.expansion('Resources', icon='menu_book').classes('w-full') as resources_expansion:
                        resources_expansion.classes('bg-transparent')
                        resources_expansion.props('dense')
                        
                        # Style the expansion header
                        resources_expansion.classes('text-slate-700 font-medium')
                        
                        with ui.column().classes('w-full gap-1 pt-2'):
                            for link in resource_links:
                                active = current_page.startswith(link['path'])
                                base_classes = 'block w-full px-4 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:bg-blue-50 hover:text-blue-600 transition'
                                active_classes = ' bg-blue-50 text-blue-600 font-semibold' if active else ''
                                
                                # Create a closure to capture the current link path
                                def create_link_handler(path):
                                    return lambda _: navigate_and_close(path)
                                
                                sub_link = ui.link(link['name'], link['path'])
                                sub_link.classes(base_classes + active_classes)
                                sub_link.on('click', create_link_handler(link['path']))

            with ui.column().classes('w-full gap-3 pb-6'):
                if not authenticated:
                    ui.button('Login', on_click=lambda: navigate_and_close('/login')).props('unelevated').classes('w-full bg-white text-base font-semibold rounded-lg transition').style('color: #0055B8 !important; border: 2px solid #0055B8 !important;')
                    ui.button('Register', on_click=lambda: navigate_and_close('/login?tab=Sign+Up')).props('unelevated').classes('w-full text-white text-base font-semibold rounded-lg transition').style('background-color: #0055B8 !important;')
                else:
                    ui.separator().classes('my-2')
                    
                    # User account dropdown in mobile menu
                    with ui.expansion(f'{user_name}', icon='account_circle').classes('w-full') as account_expansion:
                        account_expansion.classes('bg-blue-50 text-blue-600 font-medium')
                        account_expansion.props('dense')
                        
                        with ui.column().classes('w-full gap-1 pt-2'):
                            # Role-specific dashboard links
                            if user_role == 'ADMIN':
                                mobile_nav_link('Admin Dashboard', '/admin/dashboard')
                            elif user_role == 'TRAINEE':
                                mobile_nav_link('My Dashboard', '/candidates/dashboard')
                            elif user_role == 'EMPLOYER':
                                mobile_nav_link('Employer Dashboard', '/employers/dashboard')
                                mobile_nav_link('Job Postings', '/employer/job-posting')
                            
                            mobile_nav_link('Profile Settings', '/settings/profile')
                            
                            ui.separator().classes('my-2')
                            
                            ui.button('Logout', icon='logout', on_click=logout_and_close).props('unelevated').classes('w-full bg-gray-100 text-base font-semibold rounded-lg transition').style('color: #1A1A1A !important;')

    with ui.element('header').classes('fixed top-0 left-0 right-0 w-full px-4 sm:px-6 lg:px-8 shadow-md border-b').style('background-color: rgba(255, 255, 255, 0.95) !important; backdrop-filter: blur(8px) !important; border-bottom: 1px solid #e5e7eb !important; height: 64px !important; display: flex !important; align-items: center !important; z-index: 9999 !important; visibility: visible !important;'):
        with ui.row().classes('w-full max-w-7xl mx-auto items-center justify-between gap-2 sm:gap-4'):
            # Left: Logo section (clickable -> Home)
            with ui.row().classes('items-center gap-2 sm:gap-3 cursor-pointer flex-shrink-0').on('click', lambda: ui.navigate.to('/')):
                ui.icon('hub').classes('logo-icon').style('color: #0055B8 !important; font-size: 2rem;')
                ui.label('Dompell').classes('logo-text text-lg sm:text-xl font-semibold whitespace-nowrap').style('color: #1A1A1A !important; font-family: "Raleway", sans-serif;')

            # Desktop navigation (shows on desktop, hidden on mobile/tablet)
            with ui.row().classes('items-center gap-1 xl:gap-2 flex-grow justify-center').style('display: none;') as desktop_nav:
                desktop_nav.classes('lg:!flex')
                home_classes = 'nav-active' if home_active else ''
                about_classes = 'nav-active' if about_active else ''
                how_classes = 'nav-active' if how_active else ''

                ui.link('Home', '/').classes(f'top-nav-link {home_classes}')
                ui.link('About Us', '/about').classes(f'top-nav-link {about_classes}')
                ui.link('How it works', '/how-it-works').classes(f'top-nav-link {how_classes}')

                resources_classes = 'dropdown-hover dropdown-active' if resources_active else 'dropdown-hover'
                with ui.element('div').classes(resources_classes).style('padding: 8px 12px;'):
                    label_style = 'font-family: "Raleway", sans-serif; font-weight: 600; color: #0055B8;' if resources_active else 'font-family: "Raleway", sans-serif; font-weight: 500; color: #4b5563;'
                    icon_style = 'color: #0055B8; font-size: 20px;' if resources_active else 'color: #4b5563; font-size: 20px;'

                    with ui.row().classes('items-center gap-1 cursor-pointer'):
                        ui.label('Resources').style(label_style)
                        ui.icon('arrow_drop_down').classes('dropdown-icon').style(icon_style)

                    with ui.element('div').classes('dropdown-content'):
                        html_content = _build_resources_html(current_page, resource_links)
                        ui.html(html_content, sanitize=_allow_all_html)

            # Right side actions (desktop + mobile trigger)
            with ui.row().classes('items-center gap-2 sm:gap-3 flex-shrink-0'):
                with ui.row().classes('items-center gap-2 xl:gap-3').style('display: none;') as desktop_actions:
                    desktop_actions.classes('lg:!flex')
                    if not authenticated:
                        ui.button('Login', on_click=lambda: ui.navigate.to('/login')).classes('bg-white text-sm xl:text-base px-4 xl:px-6 font-semibold rounded-lg transition').style('color: #0055B8 !important; border: 2px solid #0055B8 !important;')
                        ui.button('Register', on_click=lambda: ui.navigate.to('/login?tab=Sign+Up')).classes('text-white text-sm xl:text-base px-4 xl:px-6 font-semibold rounded-lg transition').style('background-color: #0055B8 !important;')
                    else:
                        ui.icon('notifications', size='1.5rem').classes('cursor-pointer text-gray-600 hover:text-blue-600 transition-colors')

                        with ui.menu() as menu:
                            if user_role == 'ADMIN':
                                ui.menu_item('Admin Dashboard', on_click=lambda: ui.navigate.to('/admin/dashboard'))
                            elif user_role == 'TRAINEE':
                                ui.menu_item('My Dashboard', on_click=lambda: ui.navigate.to('/candidates/dashboard'))
                            elif user_role == 'EMPLOYER':
                                ui.menu_item('Employer Dashboard', on_click=lambda: ui.navigate.to('/employers/dashboard'))
                                ui.menu_item('Job Postings', on_click=lambda: ui.navigate.to('/employer/job-posting'))

                            ui.menu_item('Profile Settings', on_click=lambda: ui.navigate.to('/settings/profile'))
                            ui.separator()
                            ui.menu_item(f'Logout ({user_name})', on_click=logout)

                        if profile_pic_url and profile_pic_url.strip():
                            with ui.element('div').style('width: 36px; height: 36px; border-radius: 50%; overflow: hidden; border: 2px solid #0055B8; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.15);').on('click', menu.open):
                                ui.image(profile_pic_url).style('width: 100%; height: 100%; object-fit: cover; object-position: center;')
                        else:
                            initials = ''.join([n[0].upper() for n in user_name.split()[:2]])
                            with ui.element('div').style('width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0055B8 0%, #0066CC 100%); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 14px; cursor: pointer; box-shadow: 0 2px 6px rgba(0,85,184,0.3);').on('click', menu.open):
                                ui.label(initials)

                # Hamburger menu button - visible on mobile/tablet only
                with ui.button(icon='menu', on_click=open_drawer).props('flat round').classes('lg:hidden text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors') as menu_btn:
                    menu_btn.style('cursor: pointer !important;')
