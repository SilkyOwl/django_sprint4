from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            # TODO: set correct redirect on user creation (now it's about page, seems to be wrong)
            success_url=reverse_lazy('pages:about'),
        ),
        name='registration',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
