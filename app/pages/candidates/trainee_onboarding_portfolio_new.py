"""
Trainee Onboarding - Portfolio Upload - FUNCTIONAL VERSION
Interactive onboarding with real file uploads and form handling.
"""

from nicegui import ui, app
import asyncio
from urllib.parse import urlparse
import mimetypes

def trainee_onboarding_portfolio_page():
    """Functional trainee onboarding portfolio upload page."""
    
    # Get user data from session - check multiple possible storage locations
    user = app.storage.user.get('user_data') # CORRECTED KEY
    token = app.storage.user.get('token')
    refresh_token = app.storage.user.get('refresh_token')
    
    # Debug logging
    print(f"[ONBOARDING] User data: {user}")
    print(f"[ONBOARDING] Token exists: {bool(token)}")
    print(f"[ONBOARDING] Storage keys: {list(app.storage.user.keys())}")
    
    if not user or not token:
        print(f"[ONBOARDING] Authentication missing - redirecting to login")
        ui.notify('Please log in to continue', type='warning')
        ui.navigate.to('/login')
        return
    
    user_id = user.get('id')
    if not user_id:
        print(f"[ONBOARDING] No user ID found - redirecting to login")
        ui.notify('Session error. Please log in again.', type='warning')
        ui.navigate.to('/login')
        return
    
    print(f"[ONBOARDING] User authenticated: {user.get('email')}, ID: {user_id}")
    
    # Initialize API service
    from app.services.api_service import api_service
    api_service.set_auth_token(token)
    if refresh_token:
        api_service.set_refresh_token(refresh_token)
    
    # State management
    uploaded_files = []
    form_state = {"headline": "", "bio": "", "location": "", "cvUrl": "", "profilePictureUrl": ""}
    files_state = {"cv": None, "avatar": None}
    upload_mode = {"value": "url"}  # 'url' or 'files'

    def is_valid_url(s: str) -> bool:
        s = (s or '').strip()
        try:
            u = urlparse(s)
            return u.scheme in ('http', 'https') and bool(u.netloc)
        except Exception:
            return False
    
    def _extract_upload_meta(e):
        """Return (file_like, name, mime) from NiceGUI upload event.
        file_like can be a FileUpload (with async read()) or a dict with raw bytes.
        """
        # Prefer single file
        file_obj = getattr(e, 'file', None)
        if file_obj is not None:
            if isinstance(file_obj, dict):
                name = file_obj.get('name') or file_obj.get('filename')
                mime = file_obj.get('type') or file_obj.get('content_type') or 'application/octet-stream'
            else:
                name = getattr(file_obj, 'name', None) or getattr(file_obj, 'filename', None)
                mime = getattr(file_obj, 'content_type', None) or getattr(file_obj, 'type', None) or 'application/octet-stream'
            return file_obj, name, mime

        # Multi-file: return first
        files = getattr(e, 'files', None)
        if files and len(files) > 0:
            f = files[0]
            if isinstance(f, dict):
                name = f.get('name') or f.get('filename')
                mime = f.get('type') or f.get('content_type') or 'application/octet-stream'
            else:
                name = getattr(f, 'name', None) or getattr(f, 'filename', None)
                mime = getattr(f, 'content_type', None) or getattr(f, 'type', None) or 'application/octet-stream'
            return f, name, mime

        # Fallback: event-level (rare)
        name = getattr(e, 'name', None) or getattr(e, 'filename', None)
        mime = getattr(e, 'type', None) or getattr(e, 'content_type', None) or 'application/octet-stream'
        return None, name, mime

    # File upload handler
    async def upload_file_to_s3(file_content, file_name, file_type):
        """Upload file to S3 via API."""
        try:
            print(f"[ONBOARDING] Uploading: {file_name}")
            files = {'file': (file_name, file_content, file_type)}
            response = api_service._make_request('POST', '/upload', files=files)
            
            if response.ok:
                from urllib.parse import quote
                # Construct S3 URL (backend doesn't return it)
                # The backend saves files to a path like: <user_id>/<original_filename>
                # The bucket name is 'ajuraconnect'
                safe_file_name = quote(file_name)
                constructed_path = f"{user_id}/{safe_file_name}"
                
                file_url = f"https://ajuraconnect.s3.amazonaws.com/{constructed_path}"
                print(f"[ONBOARDING] File uploaded. Constructed URL: {file_url}")
                return file_url
            else:
                try:
                    print(f"[ONBOARDING] Upload failed: status={response.status_code}, body={response.text}")
                except Exception:
                    pass
                return None
        except Exception as e:
            print(f"[ONBOARDING] Upload error: {e}")
            return None
    
    async def handle_cv_upload(e):
        file_like, name, mime = _extract_upload_meta(e)
        content = None
        if file_like is not None:
            # dict with raw bytes
            if isinstance(file_like, dict):
                content = file_like.get('content')
            # FileUpload object with async read
            elif hasattr(file_like, 'read'):
                content = await file_like.read()
        if name is None or content is None:
            try:
                print('[UPLOAD_DEBUG] CV event had no file; dir(e)=', dir(e))
                print('[UPLOAD_DEBUG] CV event .__dict__=', getattr(e, '__dict__', {}))
            except Exception:
                pass
            ui.notify('Invalid CV upload event', type='negative')
            return
        # Normalize content to bytes
        try:
            if not isinstance(content, (bytes, bytearray)):
                content = bytes(content)
        except Exception:
            pass
        # Enforce PDF-only: backend rejects other formats as 'invalid cv'
        guessed, _ = mimetypes.guess_type(name or '')
        final_type = mime or guessed or 'application/pdf'
        is_pdf = (final_type == 'application/pdf') or ((name or '').lower().endswith('.pdf'))
        if not is_pdf:
            ui.notify('Please upload a PDF file (.pdf) for your CV', type='warning')
            return
        # Force MIME to application/pdf
        files_state["cv"] = {"name": name or 'cv.pdf', "content": content, "type": 'application/pdf'}
        ui.notify(f'CV selected: {name}', type='positive')
        try:
            render_step_content.refresh()
            actions_bar.refresh()
        except Exception:
            pass

    async def handle_avatar_upload(e):
        file_like, name, mime = _extract_upload_meta(e)
        content = None
        if file_like is not None:
            if isinstance(file_like, dict):
                content = file_like.get('content')
            elif hasattr(file_like, 'read'):
                content = await file_like.read()
        if not (name and content):
            try:
                print('[UPLOAD_DEBUG] Avatar event had no file; dir(e)=', dir(e))
                print('[UPLOAD_DEBUG] Avatar event .__dict__=', getattr(e, '__dict__', {}))
            except Exception:
                pass
            ui.notify('Invalid avatar upload event', type='negative')
            return
        files_state["avatar"] = {"name": name, "content": content, "type": mime}
        ui.notify(f'Avatar selected: {name}', type='positive')
        try:
            render_step_content.refresh()
            actions_bar.refresh()
        except Exception:
            pass

    # Handle file uploads
    async def handle_file_upload(e):
        try:
            handled_any = False
            items = []
            files = getattr(e, 'files', None)
            if files and isinstance(files, (list, tuple)) and len(files) > 0:
                for f in files:
                    if isinstance(f, dict):
                        name = f.get('name') or f.get('filename')
                        mime = f.get('type') or f.get('content_type') or 'application/octet-stream'
                        content = f.get('content')
                    else:
                        name = getattr(f, 'name', None) or getattr(f, 'filename', None)
                        mime = getattr(f, 'content_type', None) or getattr(f, 'type', None) or 'application/octet-stream'
                        content = await f.read() if hasattr(f, 'read') else None
                    if (name is not None) and (content is not None):
                        items.append((name, content, mime))
            else:
                file_obj, name, mime = _extract_upload_meta(e)
                content = None
                if file_obj is not None:
                    if isinstance(file_obj, dict):
                        content = file_obj.get('content')
                    elif hasattr(file_obj, 'read'):
                        content = await file_obj.read()
                if (name is not None) and (content is not None):
                    items.append((name, content, mime))

            if not items:
                ui.notify('No files to upload', type='warning')
                return

            for name, content, mime in items:
                ui.notify(f'Uploading {name}...', type='info')
                file_url = await upload_file_to_s3(content, name, mime)
                if file_url:
                    size_kb = f"{len(content) / 1024:.1f} KB" if hasattr(content, '__len__') else 'Unknown'
                    uploaded_files.append({'name': name, 'url': file_url, 'type': mime, 'size': size_kb})
                    ui.notify(f'{name} uploaded successfully!', type='positive')
                    ui.notify(f'URL: {file_url}', type='info', close_button=True, timeout=8000)
                    handled_any = True
                else:
                    ui.notify(f'Upload failed for {name}', type='negative')

            if handled_any:
                try:
                    render_step_content.refresh()
                except Exception:
                    pass
        except Exception as ex:
            print(f"[ERROR] File upload: {ex}")
            import traceback
            traceback.print_exc()
            ui.notify('Upload error', type='negative')
    
    # Complete onboarding
    def complete_onboarding():
        if len(uploaded_files) < 1:
            ui.notify('Please upload at least one file (CV, certificate, or project file)', type='warning')
            return
        
        # Store uploaded files in session storage to pass to the dashboard
        app.storage.user['onboarding_files'] = uploaded_files
        
        ui.notify('Files uploaded successfully! Redirecting to dashboard...', type='positive')
        ui.timer(2.0, lambda: ui.navigate.to('/candidates/dashboard'), once=True)
    
    async def handle_submit_profile():
        try:
            if not form_state["headline"] or not form_state["bio"] or not form_state["location"]:
                ui.notify('Please fill headline, bio and location.', type='warning')
                return
            # Mode-specific validations
            if upload_mode['value'] == 'url':
                if not is_valid_url(form_state.get("cvUrl", "")):
                    ui.notify('Please provide a valid CV URL (http/https).', type='warning')
                    return
                if not is_valid_url(form_state.get("profilePictureUrl", "")):
                    ui.notify('Please provide a valid Profile Picture URL (http/https).', type='warning')
                    return
            else:
                if not files_state["cv"]:
                    ui.notify('Please upload your CV file.', type='warning')
                    return

            # Trim inputs
            headline = (form_state["headline"] or "").strip()
            bio = (form_state["bio"] or "").strip()
            location = (form_state["location"] or "").strip()
            cv_url = (form_state.get("cvUrl", "") or "").strip()
            pfp_url = (form_state.get("profilePictureUrl", "") or "").strip()

            # Build request according to mode
            form = {
                "headline": headline,
                "bio": bio,
                "location": location,
            }
            if upload_mode['value'] == 'url':
                form["cvUrl"] = cv_url
                form["profilePictureUrl"] = pfp_url

            # Preflight: if profile already exists, treat as success
            try:
                pre = api_service.get_trainee_by_user(user_id)
                if pre.ok and pre.content:
                    pdata = pre.json().get('data')
                    if pdata:
                        user_store = app.storage.user.get('user_data', {})
                        user_store['traineeProfile'] = pdata
                        app.storage.user['user_data'] = user_store
                        ui.notify('Profile already exists. Redirecting to dashboard...', type='positive')
                        await asyncio.sleep(0.6)
                        ui.navigate.to('/candidates/dashboard')
                        return
            except Exception:
                pass

            # Submit based on mode
            if upload_mode['value'] == 'files':
                files = {
                    "cv": (files_state["cv"]["name"], files_state["cv"]["content"], files_state["cv"]["type"]),
                }
                if files_state["avatar"]:
                    files["avatar"] = (files_state["avatar"]["name"], files_state["avatar"]["content"], files_state["avatar"]["type"])
                if is_valid_url(pfp_url):
                    form["profilePictureUrl"] = pfp_url
                resp = api_service.create_trainee_profile(user_id, form=form, files=files)
                try:
                    print(f"[ONBOARDING] Create trainee (multipart) status={resp.status_code}")
                    print(f"[ONBOARDING] Create trainee (multipart) body={resp.text}")
                except Exception:
                    pass
                # Fallback for servers that require URLs (cvUrl/profilePictureUrl)
                if not resp.ok:
                    fallback_trigger = False
                    raw_text = ''
                    data_json = {}
                    try:
                        raw_text = resp.text or ''
                        data_json = resp.json() if resp.content else {}
                    except Exception:
                        data_json = {}
                    messages = []
                    if isinstance(data_json, dict):
                        maybe_list = data_json.get('message') or data_json.get('errors') or data_json.get('error')
                        if isinstance(maybe_list, list):
                            messages = [str(m) for m in maybe_list]
                        elif isinstance(maybe_list, str):
                            messages = [maybe_list]
                    for m in messages + [raw_text]:
                        s = (m or '').lower()
                        if 'cvurl' in s or 'profilepictureurl' in s or 'must be a url' in s or 'invalid avatar' in s:
                            fallback_trigger = True
                            break
                    if fallback_trigger:
                        ui.notify('Server requires URLs. Uploading files to cloud and retrying...', type='warning')
                        # Upload CV to S3 to obtain URL
                        cv_url2 = None
                        try:
                            cv_url2 = await upload_file_to_s3(files_state['cv']['content'], files_state['cv']['name'] or 'cv.pdf', 'application/pdf')
                        except Exception:
                            cv_url2 = None
                        # Upload avatar if provided; else use user-provided URL if valid
                        avatar_url2 = None
                        if files_state.get('avatar'):
                            try:
                                avatar_url2 = await upload_file_to_s3(files_state['avatar']['content'], files_state['avatar']['name'] or 'avatar.jpg', files_state['avatar']['type'] or 'image/jpeg')
                            except Exception:
                                avatar_url2 = None
                        fb_form = {
                            'headline': headline,
                            'bio': bio,
                            'location': location,
                        }
                        if cv_url2:
                            fb_form['cvUrl'] = cv_url2
                        # Prefer user-provided URL if valid; otherwise avatar URL
                        if is_valid_url(pfp_url):
                            fb_form['profilePictureUrl'] = pfp_url
                        elif avatar_url2:
                            fb_form['profilePictureUrl'] = avatar_url2
                        else:
                            ui.notify('Profile picture URL is required by the server. Please upload an avatar or paste a valid URL.', type='warning')
                            return
                        # Retry with JSON (no files)
                        resp2 = api_service.create_trainee_profile(user_id, form=fb_form, files=None)
                        try:
                            print(f"[ONBOARDING_FALLBACK] status={resp2.status_code}")
                            print(f"[ONBOARDING_FALLBACK] body={resp2.text}")
                        except Exception:
                            pass
                        if resp2.ok:
                            resp = resp2
                        else:
                            # Keep original resp for subsequent handling
                            pass
            else:
                resp = api_service.create_trainee_profile(user_id, form=form, files=None)
                try:
                    print(f"[ONBOARDING] Create trainee (json) status={resp.status_code}")
                    print(f"[ONBOARDING] Create trainee (json) body={resp.text}")
                except Exception:
                    pass
            if resp.ok:
                try:
                    created = resp.json().get('data') if resp.content else None
                    if created:
                        user_store = app.storage.user.get('user_data', {})
                        user_store['traineeProfile'] = created
                        app.storage.user['user_data'] = user_store
                    else:
                        prof_resp = api_service.get_trainee_by_user(user_id)
                        if prof_resp.ok and prof_resp.content:
                            app.storage.user['user_data']['traineeProfile'] = prof_resp.json().get('data')
                except:
                    pass
                ui.notify('Profile created successfully!', type='positive')
                await asyncio.sleep(1)
                ui.navigate.to('/candidates/dashboard')
            else:
                # Fallback 1: retry as form-encoded (application/x-www-form-urlencoded)
                if upload_mode['value'] == 'url':
                    try:
                        url = f"{api_service.base_url}/trainee/create/{user_id}"
                        hdrs = {}
                        if api_service.token:
                            hdrs['Authorization'] = f"Bearer {api_service.token}"
                        f1 = api_service.session.post(url, data=form, headers=hdrs, timeout=30)
                        try:
                            print(f"[ONBOARDING] Fallback form status={f1.status_code}")
                            print(f"[ONBOARDING] Fallback form body={f1.text}")
                        except Exception:
                            pass
                        if f1.ok:
                            try:
                                created = f1.json().get('data') if f1.content else None
                                if created:
                                    user_store = app.storage.user.get('user_data', {})
                                    user_store['traineeProfile'] = created
                                    app.storage.user['user_data'] = user_store
                                else:
                                    prof_resp = api_service.get_trainee_by_user(user_id)
                                    if prof_resp.ok and prof_resp.content:
                                        app.storage.user['user_data']['traineeProfile'] = prof_resp.json().get('data')
                            except:
                                pass
                            ui.notify('Profile created successfully!', type='positive')
                            await asyncio.sleep(1)
                            ui.navigate.to('/candidates/dashboard')
                            return
                    except Exception as fe:
                        try:
                            print(f"[ONBOARDING] Fallback form error: {fe}")
                        except Exception:
                            pass
                try:
                    data = resp.json() if resp.content else {}
                    server_msg = data.get('message') or data.get('error') or data
                except Exception:
                    server_msg = resp.text
                # Fallback: maybe the server created the profile despite 500
                try:
                    post = api_service.get_trainee_by_user(user_id)
                    if post.ok and post.content:
                        pdata = post.json().get('data')
                        if pdata:
                            user_store = app.storage.user.get('user_data', {})
                            user_store['traineeProfile'] = pdata
                            app.storage.user['user_data'] = user_store
                            ui.notify('Profile created (despite server error). Redirecting...', type='warning')
                            await asyncio.sleep(0.6)
                            ui.navigate.to('/candidates/dashboard')
                            return
                except Exception:
                    pass
                ui.notify(f'Failed to create profile: {resp.status_code} {server_msg}', type='negative', close_button=True, timeout=8000)
        except Exception as ex:
            ui.notify(f'Error: {ex}', type='negative')

    # Skip onboarding
    def skip_onboarding():
        ui.notify('You can complete your profile later from the dashboard', type='info')
        ui.navigate.to('/candidates/dashboard')
    
    # UI
    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *:not(.material-icons):not(.q-icon):not([class*="material-icons"]):not(i) {
            font-family: 'Raleway', sans-serif !important;
        }
        .onboarding-container {
            background: linear-gradient(135deg, #F2F7FB 0%, #E8F4F8 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .onboarding-card {
            background: white;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 8px 24px rgba(0,85,184,0.1);
            margin-bottom: 24px;
        }
        .file-item {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
        }
    </style>
    ''')
    
    current_step = {'value': 1}
    steps_meta = [
        (1, 'Profile Basics', 'Tell us who you are'),
        (2, 'CV & Avatar', 'Upload your resume and photo'),
        (3, 'Review & Submit', 'Confirm and finish'),
    ]

    @ui.refreshable
    def render_step_content():
        step = current_step['value']
        with ui.column().classes('w-full gap-6'):
            if step == 1:
                with ui.card().classes('onboarding-card'):
                    ui.label('🧩 Profile Basics').classes('text-2xl font-bold text-gray-800 mb-2')
                    with ui.column().classes('w-full gap-4'):
                        ui.input(placeholder='Headline (e.g., Backend Developer)').classes('w-full').props('outlined').bind_value(form_state, 'headline')
                        ui.textarea(placeholder='Short bio').classes('w-full').props('outlined').bind_value(form_state, 'bio')
                        ui.input(placeholder='Location (e.g., Lagos, NG)').classes('w-full').props('outlined').bind_value(form_state, 'location')
            elif step == 2:
                with ui.card().classes('onboarding-card'):
                    ui.label('🖼️ CV & Avatar').classes('text-2xl font-bold text-gray-800 mb-2')
                    with ui.column().classes('w-full gap-3'):
                        t = ui.toggle({"url": "Paste URLs", "files": "Upload Files"}).bind_value(upload_mode, 'value')
                        try:
                            t.on_value_change(lambda _: (render_step_content.refresh(), actions_bar.refresh()))
                        except Exception:
                            pass
                        if upload_mode['value'] == 'url':
                            with ui.column().classes('w-full gap-2'):
                                ui.label('Both fields are required. Paste full URLs starting with https://').classes('text-sm text-gray-500')
                                ui.input(placeholder='CV URL (https://...)').props('outlined').classes('w-full').bind_value(form_state, 'cvUrl')
                                ui.input(placeholder='Profile Picture URL (https://...)').props('outlined').classes('w-full').bind_value(form_state, 'profilePictureUrl')
                        else:
                            with ui.row().classes('w-full gap-6'):
                                with ui.column().classes('flex-1 gap-2'):
                                    ui.label('Upload CV (PDF only)').classes('text-gray-600')
                                    ui.upload(on_upload=handle_cv_upload, auto_upload=True, label='Select CV').props('accept="application/pdf,.pdf" max-file-size="10485760"').classes('w-full')
                                    if files_state['cv']:
                                        ui.label(f"Selected: {files_state['cv']['name']}").classes('text-sm text-gray-600')
                                with ui.column().classes('flex-1 gap-2'):
                                    ui.label('Upload Avatar (Image)').classes('text-gray-600')
                                    ui.upload(on_upload=handle_avatar_upload, auto_upload=True, label='Select Avatar').props('accept="image/*" max-file-size="5242880"').classes('w-full')
                                    if files_state['avatar']:
                                        ui.label(f"Selected: {files_state['avatar']['name']}").classes('text-sm text-gray-600')
                            with ui.column().classes('w-full gap-2'):
                                ui.label('Optional: Or paste a Profile Picture URL (https://...) if not uploading avatar').classes('text-sm text-gray-500')
                                ui.input(placeholder='Profile Picture URL (optional, https://...)').props('outlined').classes('w-full').bind_value(form_state, 'profilePictureUrl')
            elif step == 3:
                with ui.card().classes('onboarding-card'):
                    ui.label('✅ Review & Submit').classes('text-2xl font-bold text-gray-800 mb-2')
                    with ui.column().classes('w-full gap-3'):
                        ui.label(f"Headline: {form_state['headline'] or '—'}").classes('text-gray-700')
                        ui.label(f"Location: {form_state['location'] or '—'}").classes('text-gray-700')
                        ui.label(f"Bio: {(form_state['bio'] or '')[:140]}{'...' if (form_state['bio'] and len(form_state['bio'])>140) else ''}").classes('text-gray-700')
                        ui.separator()
                        if upload_mode['value'] == 'url':
                            ui.label(f"CV URL: {form_state['cvUrl'] or 'Not provided'}").classes('text-gray-700')
                            ui.label(f"Profile Picture URL: {form_state['profilePictureUrl'] or 'Not provided'}").classes('text-gray-700')
                        else:
                            ui.label(f"CV File: {files_state['cv']['name'] if files_state['cv'] else 'Not selected'}").classes('text-gray-700')
                            ui.label(f"Avatar File: {files_state['avatar']['name'] if files_state['avatar'] else 'Not selected'}").classes('text-gray-700')
                        ui.label('Note: You can add skills, education, experience, certifications, and portfolio after creating your profile.').classes('text-gray-600')

    @ui.refreshable
    def actions_bar():
        with ui.row().classes('w-full max-w-5xl justify-between items-center mt-6'):
            ui.button('Skip for Now', icon='arrow_forward', on_click=skip_onboarding).props('flat').classes('text-gray-600')

            def go_prev():
                if current_step['value'] > 1:
                    current_step['value'] -= 1
                    render_step_content.refresh()
                    actions_bar.refresh()

            def go_next():
                if current_step['value'] == 1 and (not form_state['headline'] or not form_state['bio'] or not form_state['location']):
                    ui.notify('Please complete profile basics', type='warning'); return
                if current_step['value'] == 2:
                    if upload_mode['value'] == 'url':
                        if not is_valid_url(form_state['cvUrl']):
                            ui.notify('Please provide a valid CV URL (http/https)', type='warning'); return
                        if not is_valid_url(form_state['profilePictureUrl']):
                            ui.notify('Please provide a valid Profile Picture URL (http/https)', type='warning'); return
                    else:
                        if not files_state['cv']:
                            ui.notify('Please upload your CV file', type='warning'); return
                if current_step['value'] < 3:
                    current_step['value'] += 1
                    render_step_content.refresh()
                    actions_bar.refresh()
                else:
                    import asyncio as _asyncio
                    _asyncio.create_task(handle_submit_profile())

            with ui.row().classes('gap-2'):
                ui.button('Back', on_click=go_prev).props('outline').classes('px-6')
                if current_step['value'] < 3:
                    ui.button('Next', on_click=go_next).classes('px-6')
                else:
                    ui.button('Complete Setup →', icon='check_circle', on_click=handle_submit_profile).classes('px-8 py-3 text-lg').style('background: linear-gradient(135deg, #0055B8 0%, #003d82 100%); color: white; font-weight: 600; border-radius: 12px;')

    with ui.column().classes('onboarding-container items-center'):
        with ui.column().classes('w-full max-w-5xl items-center text-center mb-6'):
            ui.label('Complete Your Profile').classes('text-4xl font-bold text-gray-800 mb-2')
            ui.label('A quick 3-step setup to get you ready for opportunities').classes('text-lg text-gray-600')

        with ui.row().classes('w-full max-w-5xl gap-6'):
            with ui.column().classes('w-64 gap-2'):
                with ui.card().classes('onboarding-card'):
                    for idx, title, desc in steps_meta:
                        active = (idx == current_step['value'])
                        with ui.row().classes(f"items-start gap-3 p-3 rounded-lg cursor-pointer {'bg-blue-50' if active else ''}") as _:
                            ui.icon('check_circle' if active else 'radio_button_unchecked').classes('text-blue-600')
                            with ui.column().classes('gap-0'):
                                ui.label(title).classes('font-semibold text-gray-800')
                                ui.label(desc).classes('text-xs text-gray-500')
                            _.on('click', lambda e, i=idx: (current_step.update({'value': i}), render_step_content.refresh(), actions_bar.refresh()))

            with ui.column().classes('flex-1'):
                render_step_content()

        actions_bar()
