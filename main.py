import asyncio
import sys
import warnings

# Suppress Windows-specific asyncio errors (Python 3.13 compatibility)
if sys.platform == 'win32':
    # Suppress asyncio connection reset errors
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    warnings.filterwarnings('ignore', category=RuntimeWarning, module='asyncio')

from nicegui import ui, app

# Import pages
from app.pages.shared.home import home_page
from app.pages.shared.about import about_page
from app.pages.shared.auth import auth_page
from app.pages.shared.test_login import test_login_page
from app.pages.shared.jobs import jobs_page
from app.pages.candidates.redesigned_dashboard import redesigned_candidate_dashboard
from app.pages.admin.admin_management import admin_management_page
from app.pages.employers.employer_dashboard import employer_dashboard_page
from app.pages.employers.job_posting import job_posting_page
from app.pages.employers.employer_pricing import employer_pricing_page
from app.pages.employers.company_onboarding_profile import company_onboarding_profile_page
from app.pages.employers.company_onboarding_roles import company_onboarding_roles_page
from app.pages.employers.candidates_management import candidates_management_page
from app.pages.shared.help_and_support import help_and_support_page
from app.pages.shared.how_it_works import how_it_works_page
from app.pages.institutions.institution_dashboard import institution_dashboard_page
from app.pages.institutions.modern_institution_dashboard import modern_institution_dashboard
from app.pages.institutions.institution_program_listing import institution_program_listing_page
from app.pages.institutions.institution_program_create import institution_program_create_page
from app.pages.institutions.institution_onboarding_profile import institution_onboarding_profile_page
from app.pages.candidates.application_tracking import application_tracking_page
from app.pages.shared.messaging import messaging_page
from app.pages.admin.notification_management import notification_management_page
from app.pages.shared.search import search_page
from app.services.auth_utils import get_current_user

# Import all new pages
# Authentication & User Management
from app.pages.shared.user_registration_1 import user_registration_1_page
from app.pages.shared.user_registration_2 import user_registration_2_page
from app.pages.shared.forgot_password import forgot_password_page
from app.pages.shared.reset_password import reset_password_page as new_reset_password_page
from app.pages.shared.account_verification import account_verification_page

# Trainee/Candidate Pages
from app.pages.candidates.trainee_onboarding_availability import trainee_onboarding_availability_page
from app.pages.candidates.trainee_onboarding_portfolio_new import trainee_onboarding_portfolio_page
from app.pages.candidates.trainee_documents import trainee_documents_page
from app.pages.shared.application_submission_confirmation import application_submission_confirmation_page

# Job & Application Management
from app.pages.shared.detailed_company_view import detailed_company_view_page
from app.pages.shared.training_program_directory import training_program_directory_page
from app.pages.shared.training_program_application import training_program_application_page
from app.pages.shared.detailed_training_program_view import detailed_training_program_view_page
from app.pages.institutions.post_training_program import post_training_program_page
from app.pages.employers.company_trainee_directory import company_trainee_directory_page
from app.pages.institutions.institution_analytics import institution_analytics_page
from app.pages.institutions.institution_students import institution_students_page
from app.pages.institutions.institution_settings import institution_settings_page
from app.pages.candidates.candidates_success_stories import candidates_success_stories_page
from app.pages.candidates.candidates_browse import candidates_browse_page
from app.pages.shared.api_test import api_test_page

# Communication & Interviews
from app.pages.shared.interview_booking_scheduling import interview_booking_scheduling_page
from app.pages.shared.notification_center import notification_center_page
from app.pages.shared.in_app_messaging_interface import in_app_messaging_interface_page

# Experience & Management
from app.pages.shared.immersion_experience_feedback import immersion_experience_feedback_page
from app.pages.shared.immersion_management_tracking import immersion_management_tracking_page
from app.pages.shared.edit_staff_details import edit_staff_details_page

# Admin & Settings
from app.pages.admin.admin_onboarding import admin_onboarding_page
from app.pages.admin.email_template_system import email_template_system_page
from app.pages.shared.user_settings_profile_management import user_settings_profile_management_page

# from app.pages.trainee_profile import trainee_profile_page  # Empty file
from app.components.header import header
from app.components.footer import footer


# Register all page routes
@ui.page('/')
def index():
    header('/')
    home_page()
    footer()

@ui.page('/test-login')
def test_login():
    """Test login page for quick access to different roles."""
    test_login_page()

@ui.page('/login')
def login(tab: str = None):
    """Redirect to test login page for easy role selection."""
    test_login_page()

@ui.page('/auth-form')
def auth_form(tab: str = None):
    """Actual login/signup form page."""
    header('/login')
    # Handle tab parameter from URL (e.g., /auth-form?tab=Sign+Up)
    initial_tab = 'login'  # default
    if tab and 'sign' in tab.lower():
        initial_tab = 'signup'
    
    print(f"[DEBUG] Auth form page accessed with tab parameter: {tab}, setting initial_tab to: {initial_tab}")
    auth_page(initial_tab=initial_tab)
    footer()

@ui.page('/signup')
def signup():
    """Signup route - redirects to enhanced registration"""
    ui.navigate.to('/user-registration-1')

@ui.page('/register')
def register():
    """Handle registration with role parameter."""
    from nicegui import app
    from fastapi import Request
    
    # Get role from query parameters, default to 'candidate'
    role = 'candidate'
    try:
        # Access the FastAPI request object to get query parameters
        request: Request = app.storage.request
        if request and hasattr(request, 'query_params'):
            role = request.query_params.get('role', 'candidate')
    except:
        role = 'candidate'
    
    # Normalize role names for consistency
    if role == 'trainee':
        role = 'candidate'
    elif role == 'institutions':
        role = 'institution'
    
    # Redirect to enhanced registration flow
    ui.navigate.to(f'/user-registration-1?role={role}')

@ui.page('/reset-password')
def reset_password(token: str = None):
    header()
    new_reset_password_page()
    # Pass reset token to the page - API expects JWT token, not email/resetCode
    app.storage.user['query_params'] = {'token': token}
    footer()

# Authentication & User Management Routes
@ui.page('/user-registration-1')
def user_registration_1():
    header()
    user_registration_1_page()
    footer()

@ui.page('/user-registration-2')
def user_registration_2():
    header()
    user_registration_2_page()
    footer()

@ui.page('/forgot-password')
def forgot_password():
    header()
    forgot_password_page()
    footer()

@ui.page('/account-verification')
def account_verification(token: str = None):
    header()
    # Don't store tokens - force manual code entry
    # This ensures users must enter the 6-digit code manually
    account_verification_page()
    footer()

@ui.page('/search')
def search():
    header()
    search_page()
    footer()

@ui.page('/jobs')
def jobs():
    header('/jobs')
    jobs_page()
    footer()

@ui.page('/dashboard')
def dashboard():
    # Route to role-specific dashboard
    user = get_current_user()
    if not user:
        ui.navigate.to('/login')
        return
    
    role = user.get('role', '').upper()
    if role == 'EMPLOYER':
        ui.navigate.to('/employers/dashboard')
    elif role == 'TRAINEE' or role == 'CANDIDATE':
        ui.navigate.to('/trainee/dashboard')
    elif role == 'ADMIN':
        ui.navigate.to('/admin/dashboard')
    elif role == 'INSTITUTION':
        ui.navigate.to('/institution/dashboard')
    else:
        header()
        ui.label('Dashboard').classes('text-2xl font-bold')
        ui.label('Your dashboard will be available soon.')
        footer()

# Role-based dashboard routes that our auth system expects
@ui.page('/admin/dashboard')
def admin_dashboard():
    # Check if user is authenticated
    user = get_current_user()
    print(f"[DEBUG] admin_dashboard - user: {user}")
    if not user:
        print("[DEBUG] No user found, redirecting to login")
        ui.navigate.to('/login')
        return
    
    # Strict role check - only ADMIN allowed
    if user.get('role') != 'ADMIN':
        print(f"[DEBUG] Access denied: User role {user.get('role')} not authorized for admin dashboard")
        ui.notify(f"Access denied. This dashboard is for administrators only. You are logged in as {user.get('role')}", color='negative')
        # Redirect to their appropriate dashboard
        role = user.get('role', '').upper()
        if role == 'TRAINEE':
            ui.navigate.to('/candidates/dashboard')
        elif role == 'EMPLOYER':
            ui.navigate.to('/employers/dashboard')
        elif role == 'INSTITUTION':
            ui.navigate.to('/institutions/dashboard')
        else:
            ui.navigate.to('/login')
        return
    
    print(f"[DEBUG] User {user.get('email')} accessing admin dashboard")
    header('/admin/dashboard')
    admin_management_page()
    footer()

@ui.page('/candidates/dashboard')
def candidates_dashboard():
    # Check if user is authenticated
    user = get_current_user()
    print(f"[DEBUG] candidates_dashboard - user: {user}")  # Debug info
    if not user:
        print("[DEBUG] No user found, redirecting to login")
        ui.navigate.to('/login')
        return
    
    # Strict role check - only TRAINEE and ADMIN allowed
    if user.get('role') not in ['TRAINEE', 'ADMIN']:
        print(f"[DEBUG] Access denied: User role {user.get('role')} not authorized for candidates dashboard")
        ui.notify(f"Access denied. This dashboard is for trainees only. You are logged in as {user.get('role')}", color='negative')
        # Redirect to their appropriate dashboard
        role = user.get('role', '').upper()
        if role == 'EMPLOYER':
            ui.navigate.to('/employers/dashboard')
        elif role == 'INSTITUTION':
            ui.navigate.to('/institutions/dashboard')
        else:
            ui.navigate.to('/login')
        return
    
    print(f"[DEBUG] User {user.get('email')} accessing candidates dashboard")
    redesigned_candidate_dashboard()  # Redesigned modern dashboard with enhanced UI/UX

@ui.page('/employers/dashboard')  
def employers_dashboard():
    # Check if user is authenticated
    user = get_current_user()
    print(f"[DEBUG] employers_dashboard - user: {user}")
    if not user:
        print("[DEBUG] No user found, redirecting to login")
        ui.navigate.to('/login')
        return
    
    # Strict role check - only EMPLOYER and ADMIN allowed
    if user.get('role') not in ['EMPLOYER', 'ADMIN']:
        print(f"[DEBUG] Access denied: User role {user.get('role')} not authorized for employers dashboard")
        ui.notify(f"Access denied. This dashboard is for employers only. You are logged in as {user.get('role')}", color='negative')
        # Redirect to their appropriate dashboard
        role = user.get('role', '').upper()
        if role == 'TRAINEE':
            ui.navigate.to('/candidates/dashboard')
        elif role == 'INSTITUTION':
            ui.navigate.to('/institutions/dashboard')
        else:
            ui.navigate.to('/login')
        return
    
    print(f"[DEBUG] User {user.get('email')} accessing employers dashboard")
    from app.pages.employers.modern_employer_dashboard import modern_employer_dashboard
    modern_employer_dashboard()

@ui.page('/institutions/dashboard')
def institutions_dashboard():
    # Check if user is authenticated
    user = get_current_user()
    print(f"[DEBUG] institutions_dashboard - user: {user}")
    if not user:
        print("[DEBUG] No user found, redirecting to login")
        ui.navigate.to('/login')
        return
    
    # Strict role check - only INSTITUTION and ADMIN allowed
    if user.get('role') not in ['INSTITUTION', 'ADMIN']:
        print(f"[DEBUG] Access denied: User role {user.get('role')} not authorized for institutions dashboard")
        ui.notify(f"Access denied. This dashboard is for institutions only. You are logged in as {user.get('role')}", color='negative')
        # Redirect to their appropriate dashboard
        role = user.get('role', '').upper()
        if role == 'TRAINEE':
            ui.navigate.to('/candidates/dashboard')
        elif role == 'EMPLOYER':
            ui.navigate.to('/employers/dashboard')
        else:
            ui.navigate.to('/login')
        return
    
    print(f"[DEBUG] User {user.get('email')} accessing institutions dashboard")
    header('/institutions/dashboard')
    modern_institution_dashboard()
    footer()

# Modern About Us Page
@ui.page('/about')
def about():
    header('/about')
    about_page()
    footer()


@ui.page('/contact')
def contact_page():
    """Creates the 'Contact Us' page based on the provided template."""
    header('/contact')
    with ui.element('div').classes('w-full'):
        ui.add_head_html('''
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Inter', sans-serif; background: #F7FAFC; color: #1A202C; }
                .contact-hero {
                    background: linear-gradient(135deg, #1A1A1A 0%, #0055B8 100%);
                    color: white;
                    padding: 64px 20px 48px 20px;
                    text-align: center;
                    border-radius: 0 0 32px 32px;
                    position: relative;
                    overflow: hidden;
                }
                .contact-hero h1 { font-size: 48px; font-weight: 900; margin-bottom: 16px; letter-spacing: -0.02em; }
                .contact-hero p { font-size: 20px; font-weight: 400; opacity: 0.95; max-width: 700px; margin: 0 auto; }
                .contact-main { max-width: 1200px; margin: 48px auto 0 auto; padding: 0 20px; display: flex; flex-wrap: wrap; gap: 32px; }
                .contact-form, .contact-info { flex: 1 1 340px; min-width: 320px; }
                .contact-title { font-size: 28px; font-weight: 800; color: #1A202C; margin-bottom: 16px; }
                .contact-card { background: white; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); padding: 32px; margin-bottom: 32px; }
                .contact-label { font-size: 16px; font-weight: 700; color: #0055B8; margin-bottom: 6px; }
                .contact-value { font-size: 16px; color: #2D3748; margin-bottom: 12px; }
                .map-section { max-width: 1200px; margin: 0 auto 48px auto; padding: 0 20px; }
                .map-title { font-size: 22px; font-weight: 700; color: #1A202C; margin-bottom: 12px; }
                .map-embed { width: 100%; height: 420px; border: none; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
                @media (max-width: 900px) {
                    .contact-main { flex-direction: column; gap: 24px; }
                }
            </style>
        ''')

        # Hero Section
        ui.html('''
        <section class="contact-hero">
            <h1>Contact Us</h1>
            <p>We'd love to hear from you! Reach out to our team for support, partnership, or general inquiries.</p>
        </section>
        ''', sanitize=lambda s: s)

        # Main Section: Form + Info
        ui.html('''
        <section class="contact-main">
            <div class="contact-form contact-card">
                <div class="contact-title">Send Us a Message</div>
                <form>
                    <div style="margin-bottom:20px;"><input type="text" placeholder="Your Name" style="width:100%;padding:14px 16px;border-radius:10px;border:2px solid #e2e8f0;font-size:16px;"></div>
                    <div style="margin-bottom:20px;"><input type="email" placeholder="Your Email" style="width:100%;padding:14px 16px;border-radius:10px;border:2px solid #e2e8f0;font-size:16px;"></div>
                    <div style="margin-bottom:20px;"><input type="text" placeholder="Subject" style="width:100%;padding:14px 16px;border-radius:10px;border:2px solid #e2e8f0;font-size:16px;"></div>
                    <div style="margin-bottom:20px;"><textarea placeholder="Your Message" style="width:100%;padding:14px 16px;border-radius:10px;border:2px solid #e2e8f0;font-size:16px;min-height:120px;"></textarea></div>
                    <button type="submit" style="width:100%;padding:16px 0;background:#0055B8;color:white;font-size:16px;font-weight:700;border:none;border-radius:10px;cursor:pointer;">Send Message</button>
                </form>
            </div>
            <div class="contact-info contact-card">
                <div class="contact-title">Get in Touch</div>
                <div class="contact-label">Email</div>
                <div class="contact-value"><a href="mailto:support@dompell.com">support@dompell.com</a></div>
                <div class="contact-label">Phone</div>
                <div class="contact-value">+233275320000</div>
                <div class="contact-label">Office Address</div>
                <div class="contact-value">Accra, Ghana</div>
                <div class="contact-label">Office Hours</div>
                <div class="contact-value">Monday - Friday, 9:00am - 5:00pm (GMT, Ghana)</div>
            </div>
        </section>
        ''', sanitize=lambda s: s)

        # Map Section (Ghana)
        ui.html('''
        <section class="map-section">
            <div class="map-title">Our Location (Ghana)</div>
            <iframe class="map-embed" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3971.993964024052!2d-0.1869646846759642!3d5.614818395929095!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xfdf9b1b1b1b1b1b%3A0x1b1b1b1b1b1b1b1b!2sAccra%2C%20Ghana!5e0!3m2!1sen!2sgh!4v1660000000000!5m2!1sen!2sgh" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </section>
        ''', sanitize=lambda s: s)
    footer()


def _create_contact_form():
    with ui.column().classes('flex flex-col gap-6 p-4'):
        ui.input(label='Your Name', placeholder='Enter your name').classes('w-full').props('outlined')
        ui.input(label='Your Email', placeholder='Enter your email address').classes('w-full').props('outlined')
        ui.input(label='Subject', placeholder='Enter subject of your inquiry').classes('w-full').props('outlined')
        ui.textarea(label='Your Message', placeholder='Enter your message').classes('w-full').props('outlined')
        ui.button('Submit Message').classes('w-full h-12 bg-[#066ce0] text-slate-50 text-base font-bold rounded-lg')
        ui.label('By submitting this form, you agree to our Privacy Policy.').classes('text-xs text-[#47709e] mt-2')

def _create_contact_info():
    with ui.column().classes('flex flex-col gap-8 p-4'):
        with ui.column().classes('space-y-4'):
            ui.label('Contact Information').classes('text-xl font-bold text-[#0d141c]')
            _contact_item('mail', 'Email', ['General Inquiries: info@dompell.africa', 'Support: support@dompell.africa', 'Partnerships: partnerships@dompell.africa'])
            _contact_item('call', 'Phone', ['Main Line: +233275320000'])
            _contact_item('location_on', 'Address', ['Dompell Africa Headquarters', 'Accra, Ghana'])
        
        with ui.column().classes('w-full h-64 rounded-lg overflow-hidden'):
            ui.html('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d127641.17105267332!2d36.73809623837929!3d-1.3031976077366114!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x182f1172d84d49a7%3A0xf7cf0254b297924c!2sNairobi%2C%20Kenya!5e0!3m2!1sen!2sus!4v1680000000000!5m2!1sen!2sus" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>', sanitize=lambda s: s)

def _contact_item(icon: str, title: str, lines: list):
    with ui.row().classes('flex items-start gap-4'):
        with ui.column():
            ui.label(title).classes('font-medium text-[#0d141c]')
            for line in lines:
                ui.label(line).classes('text-[#47709e]')


@ui.page('/admin/users')
def admin_users():
    header()
    admin_management_page()
    footer()

@ui.page('/employer/dashboard')
def employer_dashboard_route():
    header()
    employer_dashboard_page()
    footer()

@ui.page('/employer/post-job')
def job_posting_route():
    header()
    job_posting_page()
    footer()

@ui.page('/employer/job-posting')
def job_posting_route_alt():
    header()
    job_posting_page()
    footer()

@ui.page('/employer/trainee-directory')
def employer_trainee_directory_route():
    header()
    company_trainee_directory_page()
    footer()

@ui.page('/employer/pricing')
def employer_pricing_route():
    header('/employer/pricing')
    employer_pricing_page()
    footer()

@ui.page('/employer/onboarding/profile')
def employer_onboarding_profile():
    header()
    company_onboarding_profile_page()
    footer()

@ui.page('/employer/onboarding/roles')
def employer_onboarding_roles():
    header()
    company_onboarding_roles_page()
    footer()

@ui.page('/help')
def help_route():
    header()
    help_and_support_page()
    footer()

@ui.page('/help-and-support')
def help_and_support_route():
    header('/help-and-support')
    help_and_support_page()
    footer()

@ui.page('/how-it-works')
def how_it_works_route():
    header('/how-it-works')
    how_it_works_page()
    footer()

@ui.page('/institution/dashboard')
def institution_dashboard_route():
    header()
    modern_institution_dashboard()
    footer()

@ui.page('/institution/program-listing')
def institution_program_listing_route():
    header()
    institution_program_listing_page()
    footer()

@ui.page('/institution/programs')
def institution_programs_route():
    header()
    institution_program_listing_page()
    footer()

@ui.page('/institution/program/create')
def institution_program_create_route():
    institution_program_create_page()

@ui.page('/institution/onboarding/profile')
def institution_onboarding_profile_route():
    institution_onboarding_profile_page()

@ui.page('/institution/settings')
def institution_settings_route():
    header()
    institution_settings_page()
    footer()

@ui.page('/application-tracking')
def application_tracking_route():
    header()
    application_tracking_page()
    footer()

@ui.page('/messages')
def messaging_route():
    header()
    messaging_page()
    footer()

@ui.page('/settings/notifications')
def notification_management_route():
    header()
    notification_management_page()
    footer()

# @ui.page('/trainee/profile')\n# def trainee_profile_route():\n#     header()\n#     trainee_profile_page()\n#     footer()\n
@ui.page('/profile')
def profile():
    from app.pages.shared.user_profile import user_profile_page
    header()
    user_profile_page()
    footer()

@ui.page('/organizations')
def organizations():
    from app.pages.shared.organization_management import organization_management_page
    header()
    organization_management_page()
    footer()

@ui.page('/training-programs')
def training_programs():
    from app.pages.shared.training_programs import training_programs_page
    header()
    training_programs_page()
    footer()

@ui.page('/file-upload')
def file_upload():
    from app.pages.shared.file_upload import file_upload_page
    header()
    file_upload_page()
    footer()

@ui.page('/user-directory')
def user_directory():
    from app.pages.shared.user_directory import user_directory_page
    header()
    user_directory_page()
    footer()

# Trainee/Candidate Routes
@ui.page('/trainee-onboarding-availability')
def trainee_onboarding_availability():
    header()
    trainee_onboarding_availability_page()
    footer()

@ui.page('/trainee-onboarding-portfolio')
def trainee_onboarding_portfolio():
    header()
    trainee_onboarding_portfolio_page()
    footer()

@ui.page('/trainee/documents')
def trainee_documents():
    header('/trainee/documents')
    trainee_documents_page()
    footer()

@ui.page('/application-submission-confirmation')
def application_submission_confirmation():
    header()
    application_submission_confirmation_page()
    footer()

# Job & Application Management Routes
@ui.page('/detailed-company-view')
def detailed_company_view():
    header()
    detailed_company_view_page()
    footer()

@ui.page('/training-program-directory')
def training_program_directory():
    header('/training-program-directory')
    training_program_directory_page()
    footer()

@ui.page('/training-program-application')
def training_program_application():
    header()
    training_program_application_page()
    footer()

@ui.page('/detailed-training-program-view')
def detailed_training_program_view():
    header()
    detailed_training_program_view_page()
    footer()

@ui.page('/post-training-program')
def post_training_program():
    header()
    post_training_program_page()
    footer()

# Communication & Interview Routes
@ui.page('/interview-booking-scheduling')
def interview_booking_scheduling():
    header()
    interview_booking_scheduling_page()
    footer()

@ui.page('/notification-center')
def notification_center():
    header()
    notification_center_page()
    footer()

@ui.page('/in-app-messaging-interface')
def in_app_messaging_interface():
    header()
    in_app_messaging_interface_page()
    footer()

# Experience & Management Routes
@ui.page('/immersion-experience-feedback')
def immersion_experience_feedback():
    header()
    immersion_experience_feedback_page()
    footer()

@ui.page('/immersion-management-tracking')
def immersion_management_tracking():
    header()
    immersion_management_tracking_page()
    footer()

@ui.page('/edit-staff-details')
def edit_staff_details():
    header()
    edit_staff_details_page()
    footer()

# Admin & Settings Routes
@ui.page('/admin-onboarding')
def admin_onboarding():
    header()
    admin_onboarding_page()
    footer()

@ui.page('/email-template-system')
def email_template_system():
    header()
    email_template_system_page()
    footer()

@ui.page('/user-settings-profile-management')
def user_settings_profile_management():
    header()
    user_settings_profile_management_page()
    footer()

# Add missing routes for 404 pages
@ui.page('/training-programs')
def training_programs():
    header('/training-programs')
    training_program_directory_page()
    footer()

@ui.page('/employer/browse-candidates')
def employer_browse_candidates():
    header('/employer/browse-candidates')
    company_trainee_directory_page()
    footer()

@ui.page('/employer/candidates')
def employer_candidates_management():
    header('/employer/candidates')
    candidates_management_page()
    footer()

@ui.page('/institution/analytics')
def institution_analytics():
    header('/institution/analytics')
    institution_analytics_page()
    footer()

@ui.page('/institution/students')
def institution_students():
    header('/institution/students')
    institution_students_page()
    footer()

@ui.page('/institutions/programs')
def institutions_programs():
    header('/institutions/programs')
    training_program_directory_page()
    footer()

@ui.page('/candidates/success-stories')
def candidates_success_stories():
    header('/candidates/success-stories')
    candidates_success_stories_page()
    footer()

@ui.page('/candidates/browse')
def candidates_browse():
    header('/candidates/browse')
    candidates_browse_page()
    footer()

@ui.page('/api-test')
def api_test():
    """API endpoints test page."""
    api_test_page()

if __name__ in {"__main__", "__mp_main__"}:
    # Run the application
    print("=" * 60)
    print("Dompell Africa Platform")
    print("=" * 60)
    print("Starting server on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Add storage_secret to enable session persistence
    # Note: reload=False to avoid global UI scope issues
    ui.run(reload=True, port=8001, storage_secret='Dompell-Session-Secret-Key-2025')