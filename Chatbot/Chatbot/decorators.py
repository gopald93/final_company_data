from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

def allowed_user(allowed_roles=[]):
	def decorator(func):
		def wrap(request, *args, **kwargs):
			
			if request.user_status in allowed_roles:
				return func(request, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrap	
	return decorator	
				
def admin_only(view_func):
	def wrap(request, *args, **kwargs):
		if request.user_status == "Super Admin":
			return view_func(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse('dashboard'))
	return wrap