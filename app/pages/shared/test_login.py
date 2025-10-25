"""
Test Login page for easy access to different user roles with prefilled credentials.
"""

from nicegui import ui, app

def test_login_page():
    """Creates a test login page with quick access buttons for different roles."""
    
    # Test credentials for each role
    test_credentials = {
        'EMPLOYER': {
            'email': 'pygmy25440@mailshan.com',
            'password': 'Employer@2025',
            'name': 'ABC Trust',
            'color': '#0055B8'
        },
        'TRAINEE': {
            'email': 'vole59305@aminating.com',
            'password': 'Myke@2322',
            'name': 'Michael Abraham',
            'color': '#10b981'
        },
        'INSTITUTION': {
            'email': 'newt73321@aminating.com',
            'password': 'MEST@Ghana2025',
            'name': 'MEST Ghana',
            'color': '#8b5cf6'
        }
    }
    
    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body, .raleway-font { font-family: 'Raleway', sans-serif !important; }
            
            body {
                background: radial-gradient(1200px 600px at 10% -10%, rgba(0,85,184,0.08), transparent 60%),
                            radial-gradient(900px 500px at 110% 20%, rgba(16,185,129,0.06), transparent 60%),
                            linear-gradient(180deg, #F2F7FB 0%, #F8FAFC 100%);
            }
            
            .test-card {
                background: #ffffff;
                border-radius: 18px;
                box-shadow: 0 16px 40px rgba(2, 48, 99, 0.10), 0 6px 16px rgba(0, 85, 184, 0.06);
                border: 1px solid rgba(0, 85, 184, 0.12);
                overflow: hidden;
            }
            
            .role-button {
                border-radius: 12px;
                border: 2px solid transparent;
                transition: all .2s ease;
                cursor: pointer;
            }
            
            .role-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0, 85, 184, 0.25);
            }
            
            .badge {
                background: rgba(0, 85, 184, 0.1);
                color: #0055B8;
                font-weight: 700;
                padding: 4px 12px;
                border-radius: 9999px;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        </style>
    ''')
    
    with ui.column().classes('w-full min-h-screen flex items-center justify-center py-16 px-4'):
        with ui.column().classes('w-full max-w-7xl mx-auto gap-6'):
            # Header
            with ui.column().classes('text-center gap-3 mb-4'):
                ui.label('Quick Login').classes('text-4xl font-bold text-gray-800 raleway-font')
                ui.label('Select a role to prefill login credentials and test the dashboards').classes('text-gray-600 raleway-font')
                with ui.row().classes('justify-center gap-2 mt-2'):
                    ui.label('DEMO').classes('badge')
            
            # Two-column layout: Login cards on left, video on right
            with ui.row().classes('w-full gap-6 items-start').style('display: flex; flex-wrap: wrap;'):
                # Left column - Test login cards
                with ui.column().classes('flex-1').style('min-width: 400px; max-width: 600px;'):
                    # Test login cards
                    with ui.card().classes('test-card w-full p-8'):
                        with ui.column().classes('w-full gap-4'):
                            # Employer
                            with ui.card().classes('role-button w-full p-6 cursor-pointer').on('click', 
                                lambda: prefill_and_navigate('EMPLOYER', test_credentials['EMPLOYER'])):
                                with ui.row().classes('w-full items-center gap-4'):
                                    with ui.column().classes('flex-shrink-0'):
                                        ui.icon('business', size='48px').classes('text-[#0055B8]')
                                    with ui.column().classes('flex-grow gap-1'):
                                        ui.label('Login as Employer').classes('text-xl font-bold text-gray-800 raleway-font')
                                        ui.label('ABC Trust').classes('text-sm text-gray-600 raleway-font')
                                        with ui.row().classes('gap-2 mt-2'):
                                            ui.label(f'📧 {test_credentials["EMPLOYER"]["email"]}').classes('text-xs text-gray-500 raleway-font')
                                    ui.icon('arrow_forward', size='24px').classes('text-gray-400')
                            
                            # Candidate/Trainee
                            with ui.card().classes('role-button w-full p-6 cursor-pointer').on('click', 
                                lambda: prefill_and_navigate('TRAINEE', test_credentials['TRAINEE'])):
                                with ui.row().classes('w-full items-center gap-4'):
                                    with ui.column().classes('flex-shrink-0'):
                                        ui.icon('person', size='48px').classes('text-[#10b981]')
                                    with ui.column().classes('flex-grow gap-1'):
                                        ui.label('Login as Candidate').classes('text-xl font-bold text-gray-800 raleway-font')
                                        ui.label('Michael Abraham').classes('text-sm text-gray-600 raleway-font')
                                        with ui.row().classes('gap-2 mt-2'):
                                            ui.label(f'📧 {test_credentials["TRAINEE"]["email"]}').classes('text-xs text-gray-500 raleway-font')
                                    ui.icon('arrow_forward', size='24px').classes('text-gray-400')
                            
                            # Institution
                            with ui.card().classes('role-button w-full p-6 cursor-pointer').on('click', 
                                lambda: prefill_and_navigate('INSTITUTION', test_credentials['INSTITUTION'])):
                                with ui.row().classes('w-full items-center gap-4'):
                                    with ui.column().classes('flex-shrink-0'):
                                        ui.icon('school', size='48px').classes('text-[#8b5cf6]')
                                    with ui.column().classes('flex-grow gap-1'):
                                        ui.label('Login as Institution').classes('text-xl font-bold text-gray-800 raleway-font')
                                        ui.label('MEST Ghana').classes('text-sm text-gray-600 raleway-font')
                                        with ui.row().classes('gap-2 mt-2'):
                                            ui.label(f'📧 {test_credentials["INSTITUTION"]["email"]}').classes('text-xs text-gray-500 raleway-font')
                                    ui.icon('arrow_forward', size='24px').classes('text-gray-400')
                    
                    # Regular login link
                    with ui.row().classes('w-full justify-center mt-4'):
                        ui.label('Or').classes('text-gray-500 raleway-font')
                        ui.link('use regular login', '/auth-form').classes('text-[#0055B8] font-semibold raleway-font ml-2')
                
                # Right column - Video embed
                with ui.column().classes('flex-1').style('min-width: 400px; max-width: 600px;'):
                    with ui.card().classes('test-card w-full p-0 overflow-hidden').style('min-height: 400px;'):
                        video_container = ui.element('div').style('position:relative; width:100%; height:0px; padding-bottom:56.250%;')
                        with video_container:
                            ui.element('iframe').props(
                                'src="https://streamable.com/e/wca103?autoplay=1&nocontrols=1" '
                                'allow="fullscreen;autoplay" '
                                'allowfullscreen '
                                'frameborder="0"'
                            ).style(
                                'border:none; width:100%; height:100%; position:absolute; left:0px; top:0px; overflow:hidden;'
                            )

def prefill_and_navigate(role, credentials):
    """Store credentials in session and navigate to login page with prefilled data."""
    # Store credentials in app storage for the login page to use
    app.storage.user['prefill_email'] = credentials['email']
    app.storage.user['prefill_password'] = credentials['password']
    app.storage.user['prefill_role'] = role
    
    ui.notify(f"Redirecting to login as {credentials['name']}...", color='info')
    
    # Navigate to auth page
    ui.navigate.to('/auth-form')
