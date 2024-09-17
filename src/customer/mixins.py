from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages 


class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None  # Define the required group(s)

    def test_func(self):
        # Ensure the user is authenticated
        if not self.request.user.is_authenticated:
            return False

        # If no group is required, allow access
        if not self.group_required:
            return True

        # If one group is required
        if isinstance(self.group_required, str):
            return self.request.user.groups.filter(name=self.group_required).exists()

        # If multiple groups are required, allow if the user is in any of them
        if isinstance(self.group_required, list):
            return self.request.user.groups.filter(name__in=self.group_required).exists()

        return False

    def handle_no_permission(self):
        return redirect("subs:plans")
    
    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.add_message(request, messages.INFO, "You Need to update your plan.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
