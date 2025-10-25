"""
Authentication page for TalentConnect Africa, directly interacting with the backend API.
"""

from nicegui import ui, app
import asyncio
import re
from app.services.api_service import api_service
from app.state import auth_events

def auth_page(initial_tab: str = 'login', role: str = 'candidate'):
    """Creates a tabbed authentication page for login and registration."""
    # (Styling remains the same)
    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
            /* Brand Typography */
            :root { --brand-primary: #0055B8; --brand-primary-600: #00479a; --brand-primary-700: #003d82; --brand-primary-bg: #EEF6FF; }
            body, .raleway-font { font-family: 'Raleway', sans-serif !important; }

            /* Soft gradient background with subtle pattern */
            body {
                background: radial-gradient(1200px 600px at 10% -10%, rgba(0,85,184,0.08), transparent 60%),
                            radial-gradient(900px 500px at 110% 20%, rgba(16,185,129,0.06), transparent 60%),
                            linear-gradient(180deg, #F2F7FB 0%, #F8FAFC 100%);
            }

            /* Auth card visual uplift */
            .auth-card {
                background: #ffffff;
                border-radius: 18px;
                box-shadow: 0 16px 40px rgba(2, 48, 99, 0.10), 0 6px 16px rgba(0, 85, 184, 0.06);
                border: 1px solid rgba(0, 85, 184, 0.12);
                overflow: hidden;
                margin: 0 auto;
            }

            /* Inputs: keep structure, enhance visuals */
            .modern-input {
                border-radius: 12px;
                border: 2px solid rgba(0, 85, 184, 0.18);
                background: rgba(0, 85, 184, 0.03);
                transition: box-shadow .2s ease, border-color .2s ease;
            }
            .modern-input:focus-within {
                border-color: var(--brand-primary);
                box-shadow: 0 0 0 4px rgba(0, 85, 184, 0.18);
            }

            /* Stronger specificity to override Quasar defaults */
            .gradient-btn, .q-btn.gradient-btn {
                background: var(--brand-primary) !important;
                color: #ffffff !important;
                border-radius: 12px !important;
                border: 0 !important;
                font-weight: 700 !important;
                letter-spacing: .2px !important;
                transition: background .15s ease, box-shadow .2s ease, transform .12s ease !important;
            }
            .q-btn.gradient-btn .q-btn__content { color: #ffffff !important; }
            .gradient-btn:hover, .q-btn.gradient-btn:hover { background: var(--brand-primary-600) !important; box-shadow: 0 8px 20px rgba(0, 85, 184, 0.25) !important; transform: translateY(-1px) !important; }
            .gradient-btn:active, .q-btn.gradient-btn:active { background: var(--brand-primary-700) !important; box-shadow: 0 4px 12px rgba(0, 85, 184, 0.20) !important; transform: translateY(0) !important; }
            .gradient-btn:focus, .q-btn.gradient-btn:focus { outline: none !important; box-shadow: 0 0 0 4px rgba(0, 85, 184, 0.18) !important; }
            .gradient-btn[disabled], .q-btn.gradient-btn[disabled], .q-btn.gradient-btn.q-btn--disabled { opacity: 0.7 !important; filter: grayscale(10%) !important; box-shadow: none !important; cursor: not-allowed !important; }

            /* Tabs aesthetics (active underlines and weight already set) */
            .q-tabs { background: #F8FAFC; border-bottom: 1px solid #E2E8F0; }
            .q-tab { color: #475569; font-weight: 600; }
            .tab-active { color: var(--brand-primary) !important; font-weight: 700 !important; }
            .q-tabs__content { gap: 2px; }

            /* Small helper text consistency */
            .text-primary { color: var(--brand-primary) !important; }

            /* Header links above card */
            .auth-header { color: #475569; }
            .auth-link {
                padding: 8px 14px;
                border-radius: 9999px;
                font-weight: 700;
                color: #0f172a;
                transition: background .2s ease, color .2s ease, transform .15s ease;
            }
            .auth-link:hover { background: #EEF2F7; color: #0b1324; transform: translateY(-1px); }
            .auth-link-primary { background: var(--brand-primary-bg); color: var(--brand-primary); }

            /* Role tabs (Trainee/Employer/Institution) branding */
            .role-tabs { background: var(--brand-primary-bg); border: 1px solid rgba(0,85,184,0.18); border-radius: 12px; padding: 4px; }
            .role-tab { color: var(--brand-primary); font-weight: 700; border-radius: 10px; }
            .role-active { background: var(--brand-primary); color: #ffffff !important; }
            .role-tabs .q-tab__indicator { display: none !important; }

            /* Hero panel */
            .auth-hero {
                background: radial-gradient(900px 500px at -10% 0%, rgba(0,85,184,0.10), transparent 60%),
                            radial-gradient(700px 400px at 120% 20%, rgba(16,185,129,0.08), transparent 60%),
                            linear-gradient(180deg, #ffffff 0%, #F2F7FB 100%);
                border: 1px solid rgba(0, 85, 184, 0.10);
                border-radius: 16px;
                box-shadow: 0 8px 28px rgba(2,48,99,0.08);
            }
            .hero-badge { background: #EEF6FF; color: #066CE0; font-weight: 700; padding: 6px 12px; border-radius: 9999px; font-size: 12px; display: inline-flex; align-items: center; gap: 6px; }
            .hero-title { font-size: 28px; line-height: 1.2; font-weight: 800; color: #0f172a; }
            .hero-sub { color: #475569; }
            .hero-bullets li { display: flex; align-items: start; gap: 10px; margin: 8px 0; color: #334155; }
            .hero-dot { width: 8px; height: 8px; border-radius: 50%; background: #0055B8; margin-top: 6px; }

            /* Progress bar on submit */
            .submit-progress { height: 3px; background: linear-gradient(90deg, #0055B8, #10b981); border-radius: 2px; transition: opacity .2s ease; }

            /* Responsive split without Tailwind utilities */
            .auth-split { display: flex; flex-direction: column; gap: 2rem; }
            @media (min-width: 900px) { .auth-split { flex-direction: row; } }
            .auth-hero-container { display: none; }
            @media (min-width: 900px) { .auth-hero-container { display: flex; width: 50%; } }
            .auth-form-container { width: 100%; }
            @media (min-width: 900px) { .auth-form-container { width: 50%; }
            }
        </style>
    ''')

    with ui.column().classes('w-full py-16 px-8 min-h-screen flex items-center justify-center bg-[#F2F7FB]'):
        # Small page title
        with ui.row().classes('justify-center mb-6'):
            ui.label('Sign in or create your Dompell account').classes('text-sm text-gray-600 raleway-font')

        # Centered forms (no hero)
        with ui.column().classes('w-full max-w-lg mx-auto'):
            # Main auth card
            with ui.card().classes('auth-card w-full p-0 mx-auto'):
                with ui.tabs().props(f'model-value="{initial_tab}"').classes('w-full') as tabs:
                    ui.tab('login', 'Log In').classes('flex-1 raleway-font py-4')
                    ui.tab('signup', 'Sign Up').classes('flex-1 raleway-font py-4')

                tabs.props('active-class="tab-active" indicator-color="primary"')

                with ui.tab_panels(tabs, value=initial_tab).classes('w-full'):
                    with ui.tab_panel('login').classes('p-6 md:p-8'):
                        _create_login_form()

                    with ui.tab_panel('signup').classes('p-6 md:p-8'):
                        _create_signup_form(role)

def _create_login_form():
    """Creates the login form."""
    state = {"email": "", "password": "", "remember_me": False, "is_submitting": False}
    
    async def handle_login():
        if state["is_submitting"]: return

        if not state["email"] or '@' not in state["email"]:
            ui.notify("Please enter a valid email address.", color='negative')
            return
        if not state["password"]:
            ui.notify("Password is required.", color='negative')
            return

        state["is_submitting"] = True
        submit_button.props('loading=true')
        ui.notify("Signing in...", color='info')

        try:
            # Normalize credentials
            email = (state["email"] or "").strip().lower()
            password = (state["password"] or "").strip()
            response = api_service.login(email, password)
            
            print(f"[LOGIN] Response status: {response.status_code}")
            print(f"[LOGIN] Response content: {response.text}")
            
            if response.ok:
                response_data = response.json()
                print(f"[LOGIN] Response data: {response_data}")
                
                # Extract data from nested structure: data.user and data.token.{accessToken, refreshToken}
                data = response_data.get('data', {})
                user_data = data.get('user', {})
                token_data = data.get('token', {})
                token = token_data.get('accessToken')
                refresh_token = token_data.get('refreshToken')
                
                print(f"[LOGIN] User data: {user_data}")
                print(f"[LOGIN] Token: {token[:50] if token else 'None'}...")
                
                ui.notify("Login successful! Redirecting...", color='positive')
                
                if state["remember_me"]:
                    app.storage.user['remember_me'] = True
                
                # Use the auth_events to signal a successful login (include refresh token)
                auth_events.trigger('login', user_data, token, refresh_token)
                
                await asyncio.sleep(1)
                # Redirect based on role after login
                role = user_data.get('role', 'TRAINEE').upper()
                if role == 'ADMIN':
                    ui.navigate.to('/admin/dashboard')
                elif role == 'EMPLOYER':
                    # Always redirect to dashboard
                    ui.navigate.to('/employers/dashboard')
                elif role == 'INSTITUTION':
                    ui.navigate.to('/institutions/dashboard')
                else:  # TRAINEE or default
                    # Redirect directly to dashboard (no onboarding required)
                    ui.navigate.to('/candidates/dashboard')

            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', 'Login failed. Please check your credentials.')
                except:
                    error_msg = f'Login failed with status {response.status_code}. Please try again.'
                
                ui.notify(error_msg, color='negative')
                
                # Handle specific error cases
                if 'verify' in error_msg.lower() or 'verification' in error_msg.lower():
                    app.storage.user['verification_email'] = state["email"].strip().lower()
                    ui.notify("Please verify your account first.", color='info')
                    await asyncio.sleep(2)
                    ui.navigate.to('/account-verification')

        except Exception as e:
            print(f"[LOGIN] Unexpected error: {e}")
            ui.notify("An unexpected error occurred during login.", color='negative')
        
        finally:
            state["is_submitting"] = False
            submit_button.props('loading=false')

    with ui.column().classes('w-full px-8 py-10 gap-5'):
        # Subtle progress bar (visual only)
        progress = ui.element('div').classes('submit-progress').style('opacity: 0;')
        ui.label('Welcome Back!').classes('text-2xl font-semibold text-gray-800 text-center raleway-font')
        
        def update_email(value):
            state['email'] = value
            # Real-time email validation
            if value and '@' not in value:
                email_input.props('error error-message="Please enter a valid email address"')
            else:
                email_input.props('error=false')
        
        def update_password(value):
            state['password'] = value
            # Real-time password validation
            if value and len(value) < 6:
                password_input.props('error error-message="Password must be at least 6 characters"')
            else:
                password_input.props('error=false')
        
        email_input = ui.input(placeholder='Email Address', on_change=lambda e: update_email(e.value))\
            .props('outlined dense').classes('w-full modern-input')
        email_chip = ui.label('').classes('text-xs raleway-font')
        
        password_input = ui.input(placeholder='Password', password=True, password_toggle_button=True, on_change=lambda e: update_password(e.value))\
            .props('outlined dense').classes('w-full modern-input')

        with ui.row().classes('w-full justify-between items-center mt-3'):
            ui.checkbox('Remember me').bind_value(state, 'remember_me')
            ui.link('Forgot Password?', '/forgot-password').classes('text-sm text-primary raleway-font')
        
        submit_button = ui.button('Log In', on_click=handle_login).classes('w-full h-12 gradient-btn text-white mt-4')
        
        with ui.row().classes('w-full justify-center items-center gap-2 mt-8'):
            ui.label("Don't have an account?").classes('text-gray-600 raleway-font')
            ui.link('Sign Up', '#').classes('text-primary font-semibold raleway-font').on('click', lambda: app.get_client().run_javascript("document.querySelector('[role=tablist] button:nth-child(2)').click()"))

        password_input.on('keydown.enter', handle_login)

        # Tie progress bar to submission
        def _update_progress(active: bool):
            progress.style(f'opacity: {1 if active else 0};')
        submit_button.on('click', lambda: _update_progress(True))

def _create_signup_form(role='candidate'):
    """Creates the signup form with strict API alignment based on Dompell API requirements"""
    
    # Map incoming role to API role format (must be exact)
    role_mapping = {
        'candidate': 'TRAINEE',
        'trainee': 'TRAINEE', 
        'employer': 'EMPLOYER', 
        'institution': 'INSTITUTION'
    }
    
    # State matching exact API field names and requirements
    state = {
        "name": "",                    # API expects: letters and single spaces only, min 2 chars
        "email": "",                   # API expects: valid email format
        "password": "",                # API expects: min 8 chars, uppercase, lowercase, number, special char
        "confirmPassword": "",         # API expects: must match password (camelCase!)
        "role": role_mapping.get(role.lower(), 'TRAINEE'),  # API expects: TRAINEE, EMPLOYER, INSTITUTION, ADMIN
        "terms_agreed": False,
        "is_submitting": False
    }

    async def handle_signup():
        if state["is_submitting"]: return

        # Strict API validation based on Dompell requirements
        # Name validation: letters and single spaces only, min 2 chars
        name = state["name"].strip()
        if len(name) < 2:
            ui.notify("Name must be at least 2 characters.", color='negative')
            return
        if not re.match(r"^[a-zA-Z]+(?:\s[a-zA-Z]+)*$", name):
            ui.notify("Name must contain only letters and single spaces between words.", color='negative')
            return
        
        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", state["email"]):
            ui.notify("Please enter a valid email address.", color='negative')
            return
        
        # Password validation: min 8 chars, uppercase, lowercase, number, special char
        password = state["password"]
        if len(password) < 8:
            ui.notify("Password must be at least 8 characters long.", color='negative')
            return
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]", password):
            ui.notify("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.", color='negative')
            return
        
        # Confirm password validation
        if state["password"] != state["confirmPassword"]:
            ui.notify("Confirm password must match password.", color='negative')
            return
        
        # Terms validation
        if not state["terms_agreed"]:
            ui.notify("You must agree to the terms and conditions.", color='negative')
            return

        state["is_submitting"] = True
        submit_button.props('loading=true')
        ui.notify("Creating your account...", color='info')

        try:
            # Prepare data exactly as API expects (based on API testing)
            valid_roles = ['TRAINEE', 'EMPLOYER', 'INSTITUTION', 'ADMIN']
            user_role = state["role"] if state["role"] in valid_roles else 'TRAINEE'
            
            # Send data with EXACT field names the API expects
            user_data = {
                "name": state["name"].strip(),                    # Single name field
                "email": state["email"].strip().lower(),         # Lowercase email
                "password": state["password"],                   # Plain password
                "confirmPassword": state["confirmPassword"],     # camelCase confirmPassword!
                "role": user_role                                # Valid role
            }
            
            response = api_service.register(user_data)
            
            print(f"[REGISTRATION] Response status: {response.status_code}")
            print(f"[REGISTRATION] Response content: {response.text}")
            
            if response.ok:
                # Parse the response to extract the verification token
                response_data = response.json()
                print(f"[DEBUG] Registration successful, status: {response.status_code}")
                print(f"[DEBUG] Full response data: {response_data}")
                
                # Store email for verification page
                app.storage.user['verification_email'] = user_data["email"]
                app.storage.user['registration_name'] = user_data["name"]
                print(f"[DEBUG] Stored email: {app.storage.user.get('verification_email')}")
                
                # Extract and store the verification token from response
                # Format: {"status": 201, "message": "...", "data": {"token": "..."}}
                print(f"[DEBUG] Checking for token in response...")
                print(f"[DEBUG] 'data' in response_data: {'data' in response_data}")
                if 'data' in response_data:
                    print(f"[DEBUG] response_data['data']: {response_data['data']}")
                    print(f"[DEBUG] 'token' in response_data['data']: {'token' in response_data['data']}")
                
                if 'data' in response_data and 'token' in response_data['data']:
                    verification_token = response_data['data']['token']
                    app.storage.user['verification_token'] = verification_token
                    print(f"[DEBUG] ✅ Stored verification token: {verification_token[:50]}...")
                    print(f"[DEBUG] ✅ Verification from storage: {app.storage.user.get('verification_token', 'NONE')[:50]}...")
                else:
                    print(f"[DEBUG] ❌ No token found in registration response")
                    print(f"[DEBUG] ❌ Response structure: {list(response_data.keys())}")
                    if 'data' in response_data:
                        print(f"[DEBUG] ❌ Data keys: {list(response_data['data'].keys())}")
                
                ui.notify("Account created successfully! Redirecting to verification...", color='positive')
                print(f"[REGISTRATION] Redirecting to verification page...")
                await asyncio.sleep(1)  # Reduced from 2 to 1 second
                ui.navigate.to('/account-verification')
                print(f"[REGISTRATION] Navigation command executed")
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', 'Registration failed. Please try again.')
                    
                    # Handle different error message formats
                    if isinstance(error_msg, list):
                        error_msg = ". ".join(error_msg)
                    elif isinstance(error_msg, dict):
                        # Handle validation error objects
                        errors = []
                        for field, msgs in error_msg.items():
                            if isinstance(msgs, list):
                                errors.extend(msgs)
                            else:
                                errors.append(str(msgs))
                        error_msg = ". ".join(errors) if errors else 'Registration failed'
                    
                    ui.notify(error_msg, color='negative')
                except:
                    ui.notify(f'Registration failed with status {response.status_code}. Please try again.', color='negative')

        except Exception as e:
            print(f"[SIGNUP] Unexpected error: {e}")
            ui.notify("An unexpected error occurred during registration.", color='negative')
        
        finally:
            state["is_submitting"] = False
            submit_button.props('loading=false')

    with ui.column().classes('w-full px-8 py-10 gap-5'):
        # Subtle progress bar (visual only)
        progress = ui.element('div').classes('submit-progress').style('opacity: 0;')
        ui.label('Create Your Account').classes('text-2xl font-semibold text-gray-800 text-center raleway-font')

        with ui.column().classes('w-full gap-3'):
            ui.label('I am a:').classes('text-sm font-medium text-gray-700 raleway-font')
            with ui.tabs().props(f'model-value={role.lower()}').classes('w-full role-tabs') as user_type_tabs:
                ui.tab('trainee', 'Trainee/Candidate').classes('flex-1 role-tab')
                ui.tab('employer', 'Employer').classes('flex-1 role-tab')
                ui.tab('institution', 'Institution').classes('flex-1 role-tab')
            user_type_tabs.props('active-class="role-active"')
            
            def on_role_change(e):
                role_mapping = {
                    'trainee': 'TRAINEE', 
                    'employer': 'EMPLOYER', 
                    'institution': 'INSTITUTION'
                }
                state['role'] = role_mapping.get(e.value, 'TRAINEE')
            
            user_type_tabs.on('update:model-value', on_role_change)

        def update_name(value):
            state['name'] = value
            # API requirement: letters and single spaces only, min 2 chars
            if value:
                if len(value.strip()) < 2:
                    name_input.props('error error-message="Name must be at least 2 characters"')
                elif not re.match(r"^[a-zA-Z]+(?:\s[a-zA-Z]+)*$", value.strip()):
                    name_input.props('error error-message="Name must contain only letters and single spaces between words"')
                else:
                    name_input.props('error=false')
            else:
                name_input.props('error=false')
        
        def update_email(value):
            state['email'] = value
            if value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                email_input.props('error error-message="Please enter a valid email address"')
            else:
                email_input.props('error=false')
        
        def update_password(value):
            state['password'] = value
            # API requirement: min 8 chars, uppercase, lowercase, number, special char
            if value:
                if len(value) < 8:
                    password_input.props('error error-message="Password must be at least 8 characters long"')
                elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]", value):
                    password_input.props('error error-message="Password must contain uppercase, lowercase, number, and special character"')
                else:
                    password_input.props('error=false')
            else:
                password_input.props('error=false')
            
            # Also validate confirm password when password changes
            if state['confirmPassword']:
                if value != state['confirmPassword']:
                    confirm_password_input.props('error error-message="Confirm password must match password"')
                else:
                    confirm_password_input.props('error=false')
        
        def update_confirm_password(value):
            state['confirmPassword'] = value
            if value and value != state['password']:
                confirm_password_input.props('error error-message="Confirm password must match password"')
            else:
                confirm_password_input.props('error=false')
        
        name_input = ui.input(placeholder='Full Name (letters and spaces only)', on_change=lambda e: update_name(e.value))\
            .props('outlined dense').classes('w-full modern-input')
        name_chip = ui.label('').classes('text-xs raleway-font')
        
        email_input = ui.input(placeholder='Email Address', on_change=lambda e: update_email(e.value))\
            .props('outlined dense').classes('w-full modern-input')
        email_chip = ui.label('').classes('text-xs raleway-font')
        
        password_input = ui.input(placeholder='Create Password', password=True, on_change=lambda e: update_password(e.value))\
            .props('outlined dense').classes('w-full modern-input')
        # Password requirements helper text
        ui.label('Password must be at least 8 characters with uppercase, lowercase, number, and special character (@$!%*?&)').classes('text-xs text-gray-600')
        # Visual-only password strength meter
        strength_track = ui.element('div').style('height: 8px; background:#E2E8F0; border-radius: 6px; overflow:hidden;')
        strength_bar = ui.element('div').style('height:100%; width:0%; background:linear-gradient(90deg,#ef4444,#f59e0b,#10b981); transition:width .25s ease;')
        strength_label = ui.label('Password strength').classes('text-xs text-gray-500 mt-1')
        
        confirm_password_input = ui.input(placeholder='Confirm Password', password=True, password_toggle_button=True, on_change=lambda e: update_confirm_password(e.value))\
            .props('outlined dense').classes('w-full modern-input')
        confirm_chip = ui.label('').classes('text-xs raleway-font')

        with ui.row().classes('w-full items-center mt-3'):
            terms_checkbox = ui.checkbox('I agree to the Terms and Privacy Policy.').bind_value(state, 'terms_agreed')

        submit_button = ui.button('Create Account', on_click=handle_signup).classes('w-full h-12 gradient-btn text-white mt-5')
        
        with ui.row().classes('w-full justify-center items-center gap-2 mt-8'):
            ui.label("Already have an account?").classes('text-gray-600 raleway-font')
            ui.link('Log In', '#').classes('text-primary font-semibold raleway-font').on('click', lambda: app.get_client().run_javascript("document.querySelector('[role=tablist] button:nth-child(1)').click()"))

        confirm_password_input.on('keydown.enter', handle_signup)

        # Tie progress bar to submission
        def _update_progress(active: bool):
            progress.style(f'opacity: {1 if active else 0};')
        submit_button.on('click', lambda: _update_progress(True))

        # Inline chips and strength updates (visual only)
        def set_chip(lbl, text, ok):
            lbl.text = text
            lbl.classes('text-xs raleway-font ' + ('text-green-600' if ok else 'text-red-600'))

        def compute_strength(pw: str) -> int:
            score = 0
            if len(pw) >= 8: score += 1
            if re.search(r'[a-z]', pw): score += 1
            if re.search(r'[A-Z]', pw): score += 1
            if re.search(r'\d', pw): score += 1
            if re.search(r'[@$!%*?&]', pw): score += 1
            return score

        # Extend existing validators to update chips/strength (no API changes)
        def update_name(value):
            state['name'] = value
            if value:
                if len(value.strip()) < 2:
                    name_input.props('error error-message="Name must be at least 2 characters"')
                    set_chip(name_chip, 'Too short', False)
                elif not re.match(r"^[a-zA-Z]+(?:\s[a-zA-Z]+)*$", value.strip()):
                    name_input.props('error error-message="Name must contain only letters and single spaces between words"')
                    set_chip(name_chip, 'Only letters and single spaces', False)
                else:
                    name_input.props('error=false')
                    set_chip(name_chip, 'Looks good', True)
            else:
                name_input.props('error=false')
                set_chip(name_chip, '', True)

        def update_email(value):
            state['email'] = value
            if value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                email_input.props('error error-message="Please enter a valid email address"')
                set_chip(email_chip, 'Invalid email format', False)
            else:
                email_input.props('error=false')
                set_chip(email_chip, 'Looks good', True) if value else set_chip(email_chip, '', True)

        def update_password(value):
            state['password'] = value
            if value:
                if len(value) < 8:
                    password_input.props('error error-message="Password must be at least 8 characters long"')
                elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]", value):
                    password_input.props('error error-message="Password must contain uppercase, lowercase, number, and special character"')
                else:
                    password_input.props('error=false')
            else:
                password_input.props('error=false')
            # Update strength bar
            s = compute_strength(value or '')
            pct = [0, 20, 40, 60, 80, 100][s]
            strength_bar.style(f'width:{pct}%;')
            strength_label.text = 'Weak' if s <= 2 else ('Fair' if s == 3 else ('Good' if s == 4 else 'Strong'))
            strength_label.classes('text-xs ' + ('text-red-600' if s <= 2 else ('text-amber-600' if s == 3 else 'text-green-600')))
            # Validate confirm against new password
            if state['confirmPassword']:
                if value != state['confirmPassword']:
                    confirm_password_input.props('error error-message="Confirm password must match password"')
                    set_chip(confirm_chip, 'Passwords do not match', False)
                else:
                    confirm_password_input.props('error=false')
                    set_chip(confirm_chip, 'Passwords match', True)

        def update_confirm_password(value):
            state['confirmPassword'] = value
            if value and value != state['password']:
                confirm_password_input.props('error error-message="Confirm password must match password"')
                set_chip(confirm_chip, 'Passwords do not match', False)
            else:
                confirm_password_input.props('error=false')
                set_chip(confirm_chip, 'Passwords match', True) if value else set_chip(confirm_chip, '', True)
