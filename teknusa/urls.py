from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from accounts import views
from django.contrib import admin

from django.contrib.sitemaps.views import sitemap
from teknusa.sitemap import StaticViewSitemap, ArticleSiteMap, CategorySiteMap, TagSiteMap, UserSiteMap
from teknusa.feeds import AgrositeFeed
from django.views.generic import TemplateView
from ckeditor_uploader import urls as ckeditor_urls
from ckeditor_uploader import views as ckeditor_uploader_views


sitemaps = {
    'blog': ArticleSiteMap,
    'Category': CategorySiteMap,
    'Tag': TagSiteMap,
    'User': UserSiteMap,
    'static': StaticViewSitemap
}

handler404 = 'blog.views.page_not_found_view'
handler500 = 'blog.views.server_error_view'
handler403 = 'blog.views.permission_denied_view'  # perbaiki typo: handle403 -> handler403

urlpatterns = [
    path('admin/', admin.site.urls),   # <--- tambahkan ini

    path('mdeditor/', include('mdeditor.urls')),
    path('cookies/', include('cookie_consent.urls')),
    # path('', include('notice.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('home.urls')),
    path('', include('apps.contactus.urls')),
    path('', include('about.urls')),
    # path('', include('apps.careers.urls')),
    path('', include('services.urls')),
    path('', include('portfolio.urls')),
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path("likes/", include(('likeunlike.urls', 'likeunlike'), namespace="likes")),
    path('summernote/', include('django_summernote.urls')),

    # sitemap pakai re_path karena regex
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    path('feed/', AgrositeFeed()),
    path('rss/', AgrositeFeed()),
    path('comment/', include('comment.urls')),
    path('', include('accounts.urls', namespace='account')),
    path('leads/', include('leads.urls', namespace='leads')),
    path('lean/', include('lean.urls')),
    path('ledger/', include('ledger.urls')),
    path('post_media/', include('post_media.urls')),
    path('search/', include('haystack.urls'), name='search'),
    path('ckeditor/', include(ckeditor_urls)),  # Ensure ckeditor URLs are included
    path('ckeditor/upload/', ckeditor_uploader_views.upload, name='ckeditor_upload'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
