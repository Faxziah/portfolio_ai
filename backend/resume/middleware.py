"""
Middleware for tracking website visits.
Session-based tracking to avoid duplicate entries for page reloads.
"""
from .models import Visit
from django.utils import timezone
import uuid


class VisitTrackingMiddleware:
    """Track page visits with session-based deduplication."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip admin, static files, API endpoints, and favicon
        if not request.path.startswith('/admin/') and \
           not request.path.startswith('/static/') and \
           not request.path.startswith('/_next/') and \
           not request.path.startswith('/api/') and \
           not request.path.endswith('/favicon.ico'):
            
            try:
                # Get or create session ID
                if not request.session.session_key:
                    request.session.create()
                
                session_id = request.session.session_key
                
                # Try to find existing visit for this session
                visit = Visit.objects.filter(session_id=session_id).first()
                
                if visit:
                    # Update last_visit time (auto_now will handle this)
                    visit.save(update_fields=['last_visit'])
                else:
                    # Create new visit record
                    Visit.objects.create(
                        session_id=session_id,
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                        referer=request.META.get('HTTP_REFERER', '')[:500] if request.META.get('HTTP_REFERER') else None,
                        page=request.path
                    )
            except Exception as e:
                # Don't break the request if tracking fails
                print(f"Visit tracking error: {e}")
        
        return self.get_response(request)
    
    @staticmethod
    def get_client_ip(request):
        """Get real IP address, considering proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Take first IP from comma-separated list
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')

