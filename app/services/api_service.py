"""
API Service for Dompell Africa
This module handles all interactions with the Dompell backend API.
Updated based on API documentation: https://dompell-server.onrender.com/api-docs
"""

import requests
from typing import Dict, Any, Optional, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.config import API_BASE_URL

class ApiService:
    """A service class for handling API requests to the Dompell API."""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.token = None  # Initialize token attribute
        self.refresh_token = None
        self._configure_session()

    def _configure_session(self):
        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset(["GET", "POST", "PATCH", "DELETE"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)
        # Prefer keep-alive; we will force close on retry if needed
        self.session.headers.update({'Connection': 'keep-alive'})

    def _make_request(self, method: str, endpoint: str, data: Optional[Any] = None, 
                     params: Optional[Dict] = None, headers: Optional[Dict] = None,
                     files: Optional[Dict] = None, timeout: float = 30.0) -> requests.Response:
        """Make a generic API request with error handling."""
        url = f"{self.base_url}{endpoint}"
        
        def _do_request(hdrs: Optional[Dict]):
            if method.upper() == 'GET':
                return self.session.get(url, params=params, headers=hdrs, timeout=timeout)
            elif method.upper() == 'POST':
                if files:
                    return self.session.post(url, data=data, files=files, headers=hdrs, timeout=timeout)
                else:
                    return self.session.post(url, json=data, headers=hdrs, timeout=timeout)
            elif method.upper() == 'PATCH':
                return self.session.patch(url, json=data, headers=hdrs, timeout=timeout)
            elif method.upper() == 'DELETE':
                return self.session.delete(url, headers=hdrs, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

        try:
            resp = _do_request(headers)
            # Auto-refresh if unauthorized/forbidden and we have a refresh token
            if resp is not None and resp.status_code in (401, 403) and self.refresh_token and endpoint != '/auth/refresh-token':
                try:
                    rt_resp = self.refresh_access_token(self.refresh_token)
                    if rt_resp.ok:
                        try:
                            payload = rt_resp.json() if rt_resp.content else {}
                        except Exception:
                            payload = {}
                        # Handle possible shapes
                        new_access = (
                            (payload.get('data') or {}).get('accessToken')
                            or payload.get('accessToken')
                            or ((payload.get('token') or {}).get('accessToken'))
                        )
                        if new_access:
                            self.set_auth_token(new_access)
                            # Retry original request once, without overriding Authorization header
                            retry_headers = dict(headers or {})
                            retry_headers.pop('Authorization', None)
                            return _do_request(retry_headers)
                except Exception as _:
                    pass
            return resp
        except requests.RequestException as e:
            # Fallback: reinitialize session and retry once with Connection: close
            print(f"[API_SERVICE] Request error: {e}. Retrying once with a fresh session and Connection: close")
            try:
                self.session.close()
            except Exception:
                pass
            self.session = requests.Session()
            self._configure_session()
            if self.token:
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
            retry_headers = dict(headers or {})
            retry_headers['Connection'] = 'close'
            try:
                return _do_request(retry_headers)
            except requests.RequestException as e2:
                print(f"[API_SERVICE] Retry failed: {e2}")
                raise

    # ===== AUTHENTICATION ENDPOINTS =====
    
    def register(self, user_data: Dict[str, Any]) -> requests.Response:
        """
        Register a new user.
        
        Args:
            user_data: RegisterDto containing user registration information
            
        Returns:
            API response
        """
        return self._make_request('POST', '/auth/register', data=user_data)

    def verify_account(self, token: str, code: str) -> requests.Response:
        """
        Verify a user account with verification code.
        
        CORRECT FORMAT (tested and verified):
        - Token is passed as QUERY PARAMETER (not path!)
        - Code is sent as JSON object in body
        
        Args:
            token: JWT registration token from signup
            code: 6-digit verification code
            
        Returns:
            API response
        """
        # CORRECT format: token as query param, code in body
        url = f"{self.base_url}/auth/verify-account?token={token}"
        
        response = self.session.post(
            url,
            json={'code': code},
            headers={'Content-Type': 'application/json'}
        )
        
        return response

    def login(self, email: str, password: str) -> requests.Response:
        """
        Authenticate a user and return login response.

        Args:
            email: The user's email
            password: The user's password

        Returns:
            API response containing authentication token
        """
        payload = {
            "email": email,
            "password": password,
        }
        return self._make_request('POST', '/auth/login', data=payload)

    def forgot_password(self, email: str) -> requests.Response:
        """
        Send password reset code to user email.
        
        Args:
            email: User's email address
            
        Returns:
            API response
        """
        return self._make_request('POST', '/auth/forgot-password', data={"email": email})

    def reset_password(self, reset_data: Dict[str, Any]) -> requests.Response:
        """
        Reset user password using verification code.
        
        Args:
            reset_data: ResetPasswordDto containing email, code, and new password
            
        Returns:
            API response
        """
        return self._make_request('POST', '/auth/reset-password', data=reset_data)

    def resend_code(self, email: str) -> requests.Response:
        """
        Resend verification code to user.
        
        Args:
            email: User's email address
            
        Returns:
            API response
        """
        return self._make_request('POST', '/auth/resend-code', data={"email": email})

    def resend_email(self, email: str) -> requests.Response:
        """
        Resend verification email to user.
        
        Args:
            email: User's email address
            
        Returns:
            API response
        """
        return self._make_request('POST', '/auth/resend-email', data={"email": email})

    def refresh_access_token(self, refresh_token: str) -> requests.Response:
        """
        Generate a new access token using refresh token.
        
        Args:
            refresh_token: The refresh token
            
        Returns:
            API response with new access token
        """
        return self._make_request('POST', '/auth/refresh-token', data=refresh_token)

    # ===== USER ENDPOINTS =====

    def get_all_users(self, headers: Optional[Dict] = None) -> requests.Response:
        """
        Get all users (admin/authorized access required).
        
        Args:
            headers: Authorization headers
            
        Returns:
            API response with users list
        """
        return self._make_request('GET', '/users/all', headers=headers)

    def get_user_profile(self, user_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """
        Get a specific user's profile.
        
        Args:
            user_id: The user's ID
            headers: Authorization headers
            
        Returns:
            API response with user profile
        """
        return self._make_request('GET', f'/users/{user_id}', headers=headers)

    def update_user(self, user_id: str, user_data: Dict[str, Any], 
                   headers: Optional[Dict] = None) -> requests.Response:
        """
        Update a user's information.
        
        Args:
            user_id: The user's ID
            user_data: UserUpdateDto with updated information
            headers: Authorization headers
            
        Returns:
            API response
        """
        return self._make_request('PATCH', f'/users/{user_id}', 
                                data=user_data, headers=headers)

    def delete_user(self, user_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """
        Delete a user.
        
        Args:
            user_id: The user's ID
            headers: Authorization headers
            
        Returns:
            API response
        """
        return self._make_request('DELETE', f'/users/{user_id}', headers=headers)

    # ===== FILE UPLOAD ENDPOINTS =====

    def upload_file(self, file_data: Dict, headers: Optional[Dict] = None) -> requests.Response:
        """
        Upload a file to AWS S3 bucket.
        
        Args:
            file_data: File data and metadata
            headers: Authorization headers
            
        Returns:
            API response with file URL
        """
        return self._make_request('POST', '/upload', files=file_data, headers=headers)

    # ===== TRAINEE PROFILE ENDPOINTS =====

    def create_trainee_profile(self, user_id: str, form: Dict[str, Any], files: Optional[Dict] = None,
                               headers: Optional[Dict] = None) -> requests.Response:
        url = f"/trainee/create/{user_id}"
        return self._make_request('POST', url, data=form, files=files, headers=headers)

    def list_trainees(self, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', '/trainee', headers=headers)

    def get_trainee_by_user(self, user_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/{user_id}", headers=headers)

    def delete_trainee(self, trainee_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('DELETE', f"/trainee/{trainee_id}", headers=headers)

    # ===== TRAINEE SKILLS ENDPOINTS =====

    def add_skill(self, trainee_profile_id: str, name: str, headers: Optional[Dict] = None) -> requests.Response:
        payload = {"name": name}
        return self._make_request('POST', f"/trainee/skill/{trainee_profile_id}", data=payload, headers=headers)

    def update_skill(self, skill_id: str, update_data: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('PATCH', f"/trainee/skill/{skill_id}", data=update_data, headers=headers)

    def delete_skill(self, skill_id: str, trainee_profile_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('DELETE', f"/trainee/skill/{skill_id}/{trainee_profile_id}", headers=headers)

    # ===== TRAINEE EDUCATION ENDPOINTS =====

    def list_education(self, trainee_profile_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/education/{trainee_profile_id}", headers=headers)

    def create_education(self, trainee_profile_id: str, dto: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('POST', f"/trainee/education/create/{trainee_profile_id}", data=dto, headers=headers)

    def get_education(self, education_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/education/{education_id}", headers=headers)

    def update_education(self, education_id: str, dto: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('PATCH', f"/trainee/education/{education_id}", data=dto, headers=headers)

    def delete_education(self, education_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('DELETE', f"/trainee/education/{education_id}", headers=headers)

    # ===== TRAINEE EXPERIENCE ENDPOINTS =====

    def list_experience(self, trainee_profile_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/experience/{trainee_profile_id}", headers=headers)

    def create_experience(self, trainee_profile_id: str, dto: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('POST', f"/trainee/experience/create/{trainee_profile_id}", data=dto, headers=headers)

    def get_experience(self, experience_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/experience/{experience_id}", headers=headers)

    def update_experience(self, experience_id: str, dto: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('PATCH', f"/trainee/experience/{experience_id}", data=dto, headers=headers)

    def delete_experience(self, experience_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('DELETE', f"/trainee/experience/{experience_id}", headers=headers)

    # ===== TRAINEE CERTIFICATION ENDPOINTS =====

    def list_certifications(self, trainee_profile_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/certification/{trainee_profile_id}", headers=headers)

    def create_certification(self, trainee_profile_id: str, dto: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('POST', f"/trainee/certification/create/{trainee_profile_id}", data=dto, headers=headers)

    def get_certification(self, certification_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/certification/{certification_id}", headers=headers)

    def update_certification(self, certification_id: str, dto: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('PATCH', f"/trainee/certification/{certification_id}", data=dto, headers=headers)

    def delete_certification(self, certification_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('DELETE', f"/trainee/certification/{certification_id}", headers=headers)

    # ===== TRAINEE PORTFOLIO ENDPOINTS =====

    def list_portfolio(self, trainee_profile_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/portfolio/{trainee_profile_id}", headers=headers)

    def create_portfolio(self, trainee_profile_id: str, dto: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('POST', f"/trainee/portfolio/create/{trainee_profile_id}", data=dto, headers=headers)

    def get_portfolio_item(self, portfolio_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('GET', f"/trainee/portfolio/{portfolio_id}", headers=headers)

    def update_portfolio_item(self, portfolio_id: str, dto: Dict[str, Any], headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('PATCH', f"/trainee/portfolio/{portfolio_id}", data=dto, headers=headers)

    def delete_portfolio_item(self, portfolio_id: str, headers: Optional[Dict] = None) -> requests.Response:
        return self._make_request('DELETE', f"/trainee/portfolio/{portfolio_id}", headers=headers)

    # ===== ORGANIZATION ENDPOINTS =====

    def create_organization(self, user_id: str, org_data: Dict[str, Any], 
                          headers: Optional[Dict] = None) -> requests.Response:
        """
        Create or update an organization profile.
        
        Args:
            user_id: The user's ID
            org_data: OrganizationProfileDto with organization details
            headers: Authorization headers
            
        Returns:
            API response
        """
        return self._make_request('POST', f'/organization/create/{user_id}', 
                                data=org_data, headers=headers)

    def create_organization_multipart(self, user_id: str, form: Dict[str, Any], files: Optional[Dict] = None,
                                      headers: Optional[Dict] = None) -> requests.Response:
        """
        Create or update an organization profile using multipart/form-data.
        Use when uploading a logo file in addition to fields.
        
        Args:
            user_id: The user's ID
            form: Dict of string fields (name, industry, description, website, location, etc.)
            files: Dict with file tuples, e.g., {'logo': (filename, content_bytes, content_type)}
            headers: Authorization headers
        """
        return self._make_request('POST', f'/organization/create/{user_id}', data=form, files=files, headers=headers)

    def get_all_organizations(self, headers: Optional[Dict] = None) -> requests.Response:
        """
        Get all organizations.
        
        Args:
            headers: Authorization headers
            
        Returns:
            API response with organizations list
        """
        return self._make_request('GET', '/organization', headers=headers)

    def get_organization(self, org_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """
        Get an organization profile.
        
        Args:
            org_id: The organization's ID
            headers: Authorization headers
            
        Returns:
            API response with organization details
        """
        return self._make_request('GET', f'/organization/{org_id}', headers=headers)

    def delete_organization(self, org_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """
        Delete an organization profile.
        
        Args:
            org_id: The organization's ID
            headers: Authorization headers
            
        Returns:
            API response
        """
        return self._make_request('DELETE', f'/organization/{org_id}', headers=headers)

    def get_organization_programs(self, org_id: str, 
                                headers: Optional[Dict] = None) -> requests.Response:
        """
        Get all programs for an organization.
        
        Args:
            org_id: The organization's ID
            headers: Authorization headers
            
        Returns:
            API response with programs list
        """
        return self._make_request('GET', f'/organization/programs/{org_id}', headers=headers)

    # ===== TRAINING PROGRAMS ENDPOINTS =====

    def create_training_program(self, user_id: str, program_data: Dict[str, Any], 
                              headers: Optional[Dict] = None) -> requests.Response:
        """
        Post a new or upcoming training program.
        
        Args:
            user_id: The user's ID (institution owner)
            program_data: CreateTrainingProgramDto with program details
            headers: Authorization headers
            
        Returns:
            API response
        """
        return self._make_request('POST', f'/programs/create/{user_id}', 
                                data=program_data, headers=headers)

    def get_new_programs(self, user_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """
        Get newly created or ongoing training programs for a user.
        
        Args:
            user_id: The user's ID
            headers: Authorization headers
            
        Returns:
            API response with new programs list
        """
        return self._make_request('GET', f'/programs/new/{user_id}', headers=headers)

    def get_upcoming_programs(self, user_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """
        Get upcoming training programs (future start date) for a user.
        
        IMPORTANT: API spec shows '/api/programs/upcoming{userId}' without slash before userId
        
        Args:
            user_id: The user's ID
            headers: Authorization headers
            
        Returns:
            API response with upcoming programs list
        """
        # Try the canonical path with slash first
        resp = self._make_request('GET', f'/programs/upcoming/{user_id}', headers=headers)
        try:
            if resp is not None and 200 <= resp.status_code < 400:
                return resp
        except Exception:
            pass
        # Fallback to the spec variant missing the slash
        return self._make_request('GET', f'/programs/upcoming{user_id}', headers=headers)

    # ===== EMPLOYER ENDPOINTS =====

    def create_employer_profile(self, user_id: str, form: Dict[str, Any], files: Optional[Dict] = None,
                                headers: Optional[Dict] = None) -> requests.Response:
        """
        Create or update an employer profile.
        
        Args:
            user_id: The user's ID
            form: Dict with fields (name, industry, description, website, location)
            files: Optional dict with logo file
            headers: Authorization headers
        """
        return self._make_request('POST', f"/employer/create/{user_id}", data=form, files=files, headers=headers)

    def get_employer(self, employer_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """Get an employer profile by ID."""
        return self._make_request('GET', f"/employer/{employer_id}", headers=headers)

    def get_employer_by_user(self, user_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """Get an employer profile by user ID."""
        return self._make_request('GET', f"/employer/{user_id}", headers=headers)

    def list_employers(self, headers: Optional[Dict] = None) -> requests.Response:
        """Get all employers."""
        return self._make_request('GET', '/employer', headers=headers)

    def delete_employer(self, employer_id: str, headers: Optional[Dict] = None) -> requests.Response:
        """Delete an employer profile."""
        return self._make_request('DELETE', f"/employer/{employer_id}", headers=headers)

    # ===== UTILITY METHODS =====

    def set_auth_token(self, token: str):
        """
        Set the authorization token for all subsequent requests.
        
        Args:
            token: The JWT token
        """
        self.token = token  # Store token
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        print(f"[API_SERVICE] Token set: {token[:20]}...")

    def set_refresh_token(self, refresh_token: str):
        self.refresh_token = refresh_token

    def clear_auth_token(self):
        """Remove the authorization token from session headers."""
        self.token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']

    def get_api_status(self) -> requests.Response:
        """
        Check API server status.
        
        Returns:
            API response with server status
        """
        return self._make_request('GET', '')

# Create a singleton instance of the API service
api_service = ApiService()