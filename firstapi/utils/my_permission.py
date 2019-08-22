from rest_framework.permissions import BasePermission

class SVIPPermission(BasePermission):
    message = "must be VIP"
    def has_permission(self, request, view):
        try:
            if request.user.user_type != 3:
                return False
            return True
        except Exception as e:
            print("permission error>>>>>>>",e)
            return False

class GeneralPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True