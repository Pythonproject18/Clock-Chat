from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from .constants.default_values import Role


def auth_required(view_func=None, *, login_url='/api/verify-otp-login/'):
    """
    Decorator to enforce authentication.
    Redirects unauthenticated users to the login page.
    """

    def _auth_decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):  # ✅ `request` should be the first parameter
            if not request.user.is_authenticated:
                return redirect(login_url)  # Redirect if user is not logged in
            return view_func(request, *args, **kwargs)  # ✅ Pass request properly
        
        return _wrapped_view

    def _class_decorator(view_class):
        """Apply the decorator to class-based views"""
        view_class.dispatch = method_decorator(_auth_decorator)(view_class.dispatch)
        return view_class

    if view_func:
        if isinstance(view_func, type):  # ✅ Check if it's a class
            return _class_decorator(view_func)
        return _auth_decorator(view_func)

    return _class_decorator


def role_required(*allowed_roles, page_type='default'):
    """
    Decorator for enforcing role-based access control.

    - *allowed_roles: List of allowed role values.
    - page_type: 'admin' (admin pages) or 'enduser' (normal user pages).
    
    Behavior:
    - If user is not logged in → Redirect to sign-in page.
    - If user role is invalid → Redirect to signup page.
    - Admins cannot access end-user pages.
    - End-users cannot access admin pages.
    """
    def _role_decorator(func):
        @wraps(func)
        def _wrapped(request, *args, **kwargs):
            # ✅ Ensure user is authenticated first
            if not request.user.is_authenticated:
                return redirect('/api/verify-otp-login/')  # Redirect to sign-in

            # ✅ Safely get user role (Avoids AttributeError)
            user_role = getattr(request.user, 'roles', None)

            # ✅ If no valid role, force user to sign up
            if user_role is None:
                return redirect('/api/signup/')  # Redirect to sign-up

            # ✅ Check role-based access
            if user_role in allowed_roles:
                return func(request, *args, **kwargs)

            # ✅ Prevent cross-access (Admins cannot access user pages & vice versa)
            if page_type == 'admin' and user_role == Role.END_USER.value:
                logout(request)
                return HttpResponseForbidden("Access denied: End users cannot access admin pages.")

            elif page_type == 'enduser' and user_role in (Role.ADMIN.value):
                logout(request)
                return HttpResponseForbidden("Access denied: Admins cannot access end-user pages.")

            # ❌ Fallback case: Redirect to signup
            return redirect('/api/signup/')

        return _wrapped

    def decorator(view):
        if isinstance(view, type):  # If class-based view
            view.dispatch = method_decorator(_role_decorator)(view.dispatch)
            return view
        return _role_decorator(view)

    return decorator
