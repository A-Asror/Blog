from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from blog import settings

schema_view = get_schema_view(
    openapi.Info(title="Blog API", default_version='v1', description="Blog API urls",
                 contact=openapi.Contact(email="blog@gmail.com"), license=openapi.License(name="Blog")),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/panel/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('', include('account.urls')),
    path('post/', include('myapp.urls')),
    path('admin/', include('admin.urls'))
    # path('blog/', include('myapp.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
