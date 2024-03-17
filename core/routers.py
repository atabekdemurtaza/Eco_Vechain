from rest_framework import routers

from core.user.viewsets import UserViewSet
from core.auth.viewsets import (
    RegisterViewSet,
    RefreshViewSet,
    LoginViewSet,
    LogoutViewSet
)
from core.post.viewsets import PostViewSet

router = routers.SimpleRouter()

# ##################################################################### #
# ################### AUTH                       ###################### #
# ##################################################################### #

router.register(r"auth/register", RegisterViewSet, basename="auth-register")
router.register(r"auth/login", LoginViewSet, basename="auth-login")
router.register(r"auth/refresh", RefreshViewSet, basename="auth-refresh")
router.register(r"auth/logout", LogoutViewSet, basename="auth-logout")

# ##################################################################### #
# ################### USER                       ###################### #
# ##################################################################### #

router.register(r"user", UserViewSet, basename="user")

# Post
router.register(r'post', PostViewSet, basename='post')
# posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')

urlpatterns = [
    *router.urls,
]
