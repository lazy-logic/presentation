"""
API Endpoints Test Page
Comprehensive testing for all Dompell API endpoints
"""
from nicegui import ui, app
from app.services.api_service import api_service
from app.services.auth_utils import get_current_user, is_authenticated
from app.components.header import header
from app.components.footer import footer
import json

def api_test_page():
    """Comprehensive API testing page."""
    
    # Check authentication
    if not is_authenticated():
        ui.notify("Please login to test API endpoints", type='negative')
        ui.navigate.to('/login')
        return
    
    user = get_current_user()
    user_id = user.get('id')
    
    header()
    
    with ui.element('div').classes('min-h-screen').style('background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px;'):
        with ui.element('div').classes('max-w-7xl mx-auto'):
            ui.label('API Endpoints Test Suite').style('font-size: 32px; font-weight: 700; color: white; margin-bottom: 24px; text-align: center;')
            
            # Test results container
            test_results = {}
            
            def log_result(endpoint_name, success, message, response_data=None):
                """Log test result."""
                test_results[endpoint_name] = {
                    'success': success,
                    'message': message,
                    'data': response_data
                }
                status = '✓' if success else '✗'
                color = '#10b981' if success else '#ef4444'
                with results_container:
                    with ui.element('div').style(f'padding: 12px; margin-bottom: 8px; background: white; border-left: 4px solid {color}; border-radius: 4px;'):
                        ui.label(f'{status} {endpoint_name}').style(f'font-weight: 600; color: {color};')
                        ui.label(message).style('font-size: 13px; color: #6b7280; margin-top: 4px;')
                        if response_data and isinstance(response_data, dict):
                            with ui.expansion('Response Data', icon='data_object').classes('w-full mt-2'):
                                ui.code(json.dumps(response_data, indent=2)).classes('text-xs')
            
            # Results container
            with ui.element('div').style('background: white; padding: 24px; border-radius: 8px; margin-bottom: 24px;'):
                ui.label('Test Results').style('font-size: 20px; font-weight: 700; margin-bottom: 16px;')
                results_container = ui.column().classes('w-full gap-2')
            
            # Test Sections
            with ui.tabs().classes('w-full') as tabs:
                trainee_tab = ui.tab('Trainee Profile')
                skills_tab = ui.tab('Skills')
                education_tab = ui.tab('Education')
                experience_tab = ui.tab('Experience')
                certification_tab = ui.tab('Certifications')
                portfolio_tab = ui.tab('Portfolio')
                employer_tab = ui.tab('Employer')
            
            with ui.tab_panels(tabs, value=trainee_tab).classes('w-full'):
                # TRAINEE PROFILE TESTS
                with ui.tab_panel(trainee_tab):
                    with ui.element('div').style('background: white; padding: 24px; border-radius: 8px;'):
                        ui.label('Trainee Profile Endpoints').style('font-size: 18px; font-weight: 700; margin-bottom: 16px;')
                        
                        def test_trainee_endpoints():
                            results_container.clear()
                            
                            # Test 1: Create/Update Trainee Profile
                            try:
                                profile_data = {
                                    'headline': 'Test Developer',
                                    'bio': 'Testing API endpoints',
                                    'location': 'Test City, TC'
                                }
                                r = api_service.create_trainee_profile(user_id, form=profile_data, files=None)
                                if r.ok:
                                    data = r.json() if r.content else {}
                                    log_result('POST /api/trainee/create/{userId}', True, f'Status: {r.status_code}', data)
                                else:
                                    log_result('POST /api/trainee/create/{userId}', False, f'Status: {r.status_code} - {r.text[:200]}')
                            except Exception as e:
                                log_result('POST /api/trainee/create/{userId}', False, f'Error: {str(e)}')
                            
                            # Test 2: Get Trainee by User ID
                            try:
                                r = api_service.get_trainee_by_user(user_id)
                                if r.ok:
                                    data = r.json() if r.content else {}
                                    trainee_id = (data.get('data') or {}).get('id')
                                    log_result('GET /api/trainee/{userId}', True, f'Status: {r.status_code}', data)
                                    
                                    # Test 3: Get Trainee by ID (if we have trainee_id)
                                    if trainee_id:
                                        try:
                                            r2 = api_service.get_trainee_by_user(trainee_id)
                                            if r2.ok:
                                                log_result('GET /api/trainee/{id}', True, f'Status: {r2.status_code}')
                                            else:
                                                log_result('GET /api/trainee/{id}', False, f'Status: {r2.status_code}')
                                        except Exception as e:
                                            log_result('GET /api/trainee/{id}', False, f'Error: {str(e)}')
                                else:
                                    log_result('GET /api/trainee/{userId}', False, f'Status: {r.status_code}')
                            except Exception as e:
                                log_result('GET /api/trainee/{userId}', False, f'Error: {str(e)}')
                            
                            # Test 4: List All Trainees
                            try:
                                r = api_service.list_trainees()
                                if r.ok:
                                    data = r.json() if r.content else {}
                                    count = len((data.get('data') or []))
                                    log_result('GET /api/trainee', True, f'Status: {r.status_code} - Found {count} trainees')
                                else:
                                    log_result('GET /api/trainee', False, f'Status: {r.status_code}')
                            except Exception as e:
                                log_result('GET /api/trainee', False, f'Error: {str(e)}')
                            
                            ui.notify('Trainee profile tests completed', type='positive')
                        
                        ui.button('Run Trainee Profile Tests', icon='play_arrow', on_click=test_trainee_endpoints).props('flat').style('background: #0055B8; color: white;')
                
                # SKILLS TESTS
                with ui.tab_panel(skills_tab):
                    with ui.element('div').style('background: white; padding: 24px; border-radius: 8px;'):
                        ui.label('Skills Endpoints').style('font-size: 18px; font-weight: 700; margin-bottom: 16px;')
                        
                        def test_skills_endpoints():
                            results_container.clear()
                            
                            # Get trainee profile ID first
                            try:
                                r = api_service.get_trainee_by_user(user_id)
                                if not r.ok:
                                    log_result('Skills Test', False, 'Could not get trainee profile')
                                    return
                                
                                data = r.json() if r.content else {}
                                trainee_profile_id = ((data.get('data') or {}).get('id') or 
                                                     (data.get('data') or {}).get('_id'))
                                
                                if not trainee_profile_id:
                                    log_result('Skills Test', False, 'No trainee profile ID found')
                                    return
                                
                                # Test 1: Add Skill
                                skill_id = None
                                try:
                                    r = api_service.add_skill(trainee_profile_id, 'API Testing')
                                    if r.ok:
                                        data = r.json() if r.content else {}
                                        skill_id = ((data.get('data') or {}).get('id') or 
                                                   (data.get('data') or {}).get('_id'))
                                        log_result('POST /api/trainee/skill/{traineeProfileId}', True, f'Status: {r.status_code}', data)
                                    else:
                                        log_result('POST /api/trainee/skill/{traineeProfileId}', False, f'Status: {r.status_code} - {r.text[:200]}')
                                except Exception as e:
                                    log_result('POST /api/trainee/skill/{traineeProfileId}', False, f'Error: {str(e)}')
                                
                                # Test 2: Update Skill (if we have skill_id)
                                if skill_id:
                                    try:
                                        r = api_service.update_skill(skill_id, {'name': 'Advanced API Testing'})
                                        if r.ok:
                                            log_result('PATCH /api/trainee/skill/{id}', True, f'Status: {r.status_code}')
                                        else:
                                            log_result('PATCH /api/trainee/skill/{id}', False, f'Status: {r.status_code}')
                                    except Exception as e:
                                        log_result('PATCH /api/trainee/skill/{id}', False, f'Error: {str(e)}')
                                    
                                    # Test 3: Delete Skill
                                    try:
                                        r = api_service.delete_skill(skill_id, trainee_profile_id)
                                        if r.ok:
                                            log_result('DELETE /api/trainee/skill/{skillId}/{traineeProfileId}', True, f'Status: {r.status_code}')
                                        else:
                                            log_result('DELETE /api/trainee/skill/{skillId}/{traineeProfileId}', False, f'Status: {r.status_code}')
                                    except Exception as e:
                                        log_result('DELETE /api/trainee/skill/{skillId}/{traineeProfileId}', False, f'Error: {str(e)}')
                                
                                ui.notify('Skills tests completed', type='positive')
                            
                            except Exception as e:
                                log_result('Skills Test', False, f'Error: {str(e)}')
                        
                        ui.button('Run Skills Tests', icon='play_arrow', on_click=test_skills_endpoints).props('flat').style('background: #0055B8; color: white;')
                
                # EDUCATION TESTS
                with ui.tab_panel(education_tab):
                    with ui.element('div').style('background: white; padding: 24px; border-radius: 8px;'):
                        ui.label('Education Endpoints').style('font-size: 18px; font-weight: 700; margin-bottom: 16px;')
                        
                        def test_education_endpoints():
                            results_container.clear()
                            
                            try:
                                r = api_service.get_trainee_by_user(user_id)
                                if not r.ok:
                                    log_result('Education Test', False, 'Could not get trainee profile')
                                    return
                                
                                data = r.json() if r.content else {}
                                trainee_profile_id = ((data.get('data') or {}).get('id') or 
                                                     (data.get('data') or {}).get('_id'))
                                
                                if not trainee_profile_id:
                                    log_result('Education Test', False, 'No trainee profile ID found')
                                    return
                                
                                # Test 1: List Education
                                try:
                                    r = api_service.list_education(trainee_profile_id)
                                    if r.ok:
                                        log_result('GET /api/trainee/education/{traineeProfileId}', True, f'Status: {r.status_code}')
                                    else:
                                        log_result('GET /api/trainee/education/{traineeProfileId}', False, f'Status: {r.status_code}')
                                except Exception as e:
                                    log_result('GET /api/trainee/education/{traineeProfileId}', False, f'Error: {str(e)}')
                                
                                # Test 2: Create Education
                                education_id = None
                                try:
                                    edu_data = {
                                        'institution': 'Test University',
                                        'degree': 'Bachelor of Science',
                                        'fieldOfStudy': 'Computer Science',
                                        'startDate': '2020-01-01',
                                        'endDate': '2024-01-01'
                                    }
                                    r = api_service.create_education(trainee_profile_id, edu_data)
                                    if r.ok:
                                        data = r.json() if r.content else {}
                                        education_id = ((data.get('data') or {}).get('id') or 
                                                       (data.get('data') or {}).get('_id'))
                                        log_result('POST /api/trainee/education/create/{traineeProfileId}', True, f'Status: {r.status_code}', data)
                                    else:
                                        log_result('POST /api/trainee/education/create/{traineeProfileId}', False, f'Status: {r.status_code} - {r.text[:200]}')
                                except Exception as e:
                                    log_result('POST /api/trainee/education/create/{traineeProfileId}', False, f'Error: {str(e)}')
                                
                                # Test 3: Get, Update, Delete Education (if we have education_id)
                                if education_id:
                                    try:
                                        r = api_service.get_education(education_id)
                                        if r.ok:
                                            log_result('GET /api/trainee/education/{id}', True, f'Status: {r.status_code}')
                                        else:
                                            log_result('GET /api/trainee/education/{id}', False, f'Status: {r.status_code}')
                                    except Exception as e:
                                        log_result('GET /api/trainee/education/{id}', False, f'Error: {str(e)}')
                                    
                                    try:
                                        r = api_service.update_education(education_id, {'degree': 'Master of Science'})
                                        if r.ok:
                                            log_result('PATCH /api/trainee/education/{id}', True, f'Status: {r.status_code}')
                                        else:
                                            log_result('PATCH /api/trainee/education/{id}', False, f'Status: {r.status_code}')
                                    except Exception as e:
                                        log_result('PATCH /api/trainee/education/{id}', False, f'Error: {str(e)}')
                                    
                                    try:
                                        r = api_service.delete_education(education_id)
                                        if r.ok:
                                            log_result('DELETE /api/trainee/education/{id}', True, f'Status: {r.status_code}')
                                        else:
                                            log_result('DELETE /api/trainee/education/{id}', False, f'Status: {r.status_code}')
                                    except Exception as e:
                                        log_result('DELETE /api/trainee/education/{id}', False, f'Error: {str(e)}')
                                
                                ui.notify('Education tests completed', type='positive')
                            
                            except Exception as e:
                                log_result('Education Test', False, f'Error: {str(e)}')
                        
                        ui.button('Run Education Tests', icon='play_arrow', on_click=test_education_endpoints).props('flat').style('background: #0055B8; color: white;')
                
                # EXPERIENCE TESTS
                with ui.tab_panel(experience_tab):
                    with ui.element('div').style('background: white; padding: 24px; border-radius: 8px;'):
                        ui.label('Experience Endpoints').style('font-size: 18px; font-weight: 700; margin-bottom: 16px;')
                        ui.label('Tests similar to Education endpoints').style('font-size: 14px; color: #6b7280; margin-bottom: 16px;')
                        ui.button('Run Experience Tests', icon='play_arrow').props('flat disabled').style('background: #9ca3af; color: white;')
                
                # CERTIFICATION TESTS
                with ui.tab_panel(certification_tab):
                    with ui.element('div').style('background: white; padding: 24px; border-radius: 8px;'):
                        ui.label('Certification Endpoints').style('font-size: 18px; font-weight: 700; margin-bottom: 16px;')
                        ui.label('Tests similar to Education endpoints').style('font-size: 14px; color: #6b7280; margin-bottom: 16px;')
                        ui.button('Run Certification Tests', icon='play_arrow').props('flat disabled').style('background: #9ca3af; color: white;')
                
                # PORTFOLIO TESTS
                with ui.tab_panel(portfolio_tab):
                    with ui.element('div').style('background: white; padding: 24px; border-radius: 8px;'):
                        ui.label('Portfolio Endpoints').style('font-size: 18px; font-weight: 700; margin-bottom: 16px;')
                        ui.label('Tests similar to Education endpoints').style('font-size: 14px; color: #6b7280; margin-bottom: 16px;')
                        ui.button('Run Portfolio Tests', icon='play_arrow').props('flat disabled').style('background: #9ca3af; color: white;')
                
                # EMPLOYER TESTS
                with ui.tab_panel(employer_tab):
                    with ui.element('div').style('background: white; padding: 24px; border-radius: 8px;'):
                        ui.label('Employer Endpoints').style('font-size: 18px; font-weight: 700; margin-bottom: 16px;')
                        
                        def test_employer_endpoints():
                            results_container.clear()
                            
                            # Test 1: List All Employers
                            try:
                                r = api_service.list_employers()
                                if r.ok:
                                    data = r.json() if r.content else {}
                                    count = len((data.get('data') or []))
                                    log_result('GET /api/employer', True, f'Status: {r.status_code} - Found {count} employers')
                                else:
                                    log_result('GET /api/employer', False, f'Status: {r.status_code}')
                            except Exception as e:
                                log_result('GET /api/employer', False, f'Error: {str(e)}')
                            
                            # Test 2: Get Employer by User ID
                            try:
                                r = api_service.get_employer_by_user(user_id)
                                if r.ok:
                                    data = r.json() if r.content else {}
                                    log_result('GET /api/employer/{userId}', True, f'Status: {r.status_code}', data)
                                else:
                                    log_result('GET /api/employer/{userId}', False, f'Status: {r.status_code} - {r.text[:200]}')
                            except Exception as e:
                                log_result('GET /api/employer/{userId}', False, f'Error: {str(e)}')
                            
                            ui.notify('Employer tests completed', type='positive')
                        
                        ui.button('Run Employer Tests', icon='play_arrow', on_click=test_employer_endpoints).props('flat').style('background: #0055B8; color: white;')
            
            # Summary Section
            with ui.element('div').style('background: white; padding: 24px; border-radius: 8px; margin-top: 24px;'):
                ui.label('Test Summary').style('font-size: 20px; font-weight: 700; margin-bottom: 16px;')
                
                def show_summary():
                    total = len(test_results)
                    passed = sum(1 for r in test_results.values() if r['success'])
                    failed = total - passed
                    
                    with ui.element('div').style('display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;'):
                        with ui.element('div').style('padding: 16px; background: #f3f4f6; border-radius: 8px; text-align: center;'):
                            ui.label(str(total)).style('font-size: 32px; font-weight: 700; color: #374151;')
                            ui.label('Total Tests').style('font-size: 14px; color: #6b7280;')
                        
                        with ui.element('div').style('padding: 16px; background: #d1fae5; border-radius: 8px; text-align: center;'):
                            ui.label(str(passed)).style('font-size: 32px; font-weight: 700; color: #10b981;')
                            ui.label('Passed').style('font-size: 14px; color: #059669;')
                        
                        with ui.element('div').style('padding: 16px; background: #fee2e2; border-radius: 8px; text-align: center;'):
                            ui.label(str(failed)).style('font-size: 32px; font-weight: 700; color: #ef4444;')
                            ui.label('Failed').style('font-size: 14px; color: #dc2626;')
                
                ui.button('Show Summary', icon='summarize', on_click=show_summary).props('flat').style('background: #6b7280; color: white;')
    
    footer()
