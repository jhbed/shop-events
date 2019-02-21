from django.urls import path
from . import views as shopify_con_views


urlpatterns = [
    path('', view=shopify_con_views.test_view, name='events-home')
]
