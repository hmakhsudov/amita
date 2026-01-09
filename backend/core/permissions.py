from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminRole(BasePermission):
    message = "Недостаточно прав."

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, "profile", None)
        return bool(profile and profile.role == "admin")


class IsClientRole(BasePermission):
    message = "Недостаточно прав."

    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, "profile", None)
        return bool(profile and profile.role == "client")


class IsAdminRoleOrReadOnly(IsAdminRole):
    pass


class IsOwnerOrAdmin(BasePermission):
    message = "Недостаточно прав."

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, "profile", None)
        if profile and profile.role == "admin":
            return True
        return getattr(obj, "user_id", None) == user.id


class IsBookingOwnerOrMaster(BasePermission):
    message = "Недостаточно прав."

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(obj, "user_id", None) == user.id:
            return True
        if getattr(obj, "master_id", None) == user.id:
            return True
        if user.is_superuser:
            return True
        return False


class IsServiceMasterOrAdmin(BasePermission):
    message = "Недостаточно прав."

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, "profile", None)
        return bool(profile and profile.role == "admin")

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if obj.masters.filter(id=user.id).exists():
            return True
        masters_ids = request.data.get("masters_ids") if hasattr(request, "data") else None
        if masters_ids:
            if isinstance(masters_ids, str):
                masters_set = {masters_ids}
            else:
                masters_set = {str(value) for value in masters_ids}
            if str(user.id) in masters_set:
                return True
        return False
