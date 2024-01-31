from django.contrib import admin

# Register your models here.
"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# integrates with django translation system (for future proofing purposes)
from django.utils.translation import gettext_lazy as _

from core import models 

class UserAdmin(BaseUserAdmin):
	"""
		Define the admin pages for users.
	"""
	ordering = ["id"]
	list_display = ["email", "name"]
	fieldsets = (
		# the "None" represents the title of the section, and the fields are the editable fields
		(None, {"fields": ("email", "password")}),
		(
			# title : permissions, and editable fields : is_active, is_staff, is_superuser
			_("Permissions"),
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
				)
			}
		),
		(_("Important dates"), {"fields": ("last_login",)}),
	)
	readonly_fields = ["last_login"]
	add_fieldsets = (
		(None, {
			"classes" : ("wide", ),		
			"fields" : (
				"email",
				"password1",
				"password2",
				"name",
				"is_active",
				"is_staff",
				"is_superuser"
			)
		}),
	)

# the second param will use our custom admin class as opposed to the default model manager
admin.site.register(models.User, UserAdmin)

