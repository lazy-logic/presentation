"""
Global state management for Dompell Africa
"""

from nicegui import ui, app

class AppState:
    """Global application state"""
    def __init__(self):
        self.current_user = None
        self.user_role = None  # 'trainee', 'employer', 'institution', 'admin'
        self.current_page = 'home'
        self.notifications = []
    
    def login(self, email: str, role: str):
        """Login user"""
        self.current_user = email
        self.user_role = role
    
    def logout(self):
        """Logout user"""
        self.current_user = None
        self.user_role = None
        ui.navigate.to('/')
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None

class Events:
    """A simple event handling class."""
    def __init__(self):
        self.callbacks = {}

    def on(self, event_type):
        """Decorator to register a callback for an event."""
        def decorator(callback):
            if event_type not in self.callbacks:
                self.callbacks[event_type] = []
            self.callbacks[event_type].append(callback)
            return callback
        return decorator

    def trigger(self, event_type, *args, **kwargs):
        if event_type in self.callbacks:
            for callback in self.callbacks[event_type]:
                callback(*args, **kwargs)

# Global state instance
app_state = AppState()

# Create a global instance of the event handler
auth_events = Events()

@auth_events.on('login')
def handle_login(user_data: dict, token: str, refresh_token: str = None):
    """Handle user login state."""
    app.storage.user.update({
        'is_authenticated': True,
        'user_data': user_data,
        'token': token,
        'refresh_token': refresh_token,
    })
    # Set the token in the API service for subsequent requests
    from .services.api_service import api_service
    api_service.set_auth_token(token)
    if refresh_token:
        api_service.set_refresh_token(refresh_token)
    print(f"User {user_data.get('email')} logged in.")

@auth_events.on('logout')
def handle_logout():
    """Handle user logout state."""
    # Clear the token from the API service
    from .services.api_service import api_service
    api_service.clear_auth_token()
    api_service.refresh_token = None
    
    # Clear user session
    app.storage.user.clear()
    app.storage.user['is_authenticated'] = False
    
    print("User logged out.")
    ui.navigate.to('/login')