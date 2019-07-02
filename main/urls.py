from django.urls import path,include
from . import views

app_name="main"

urlpatterns = [
    path('', views.home, name="home"),
    path('category/<category>', views.category, name="category"),
    path('login/', views.login, name="login"),
    path('login_signin/', views.login_signin, name="login_signin"),
    path('logouts/', views.logouts, name="logouts"),
    path('signup/', views.signup, name="signup"),
    path("like/", views.like, name="like"),
    path("detail/<pid>/like/", views.like, name="like"),
    path("detail/<pid>/comment/", views.comment, name="comment"),
    path("detail/<pid>/", views.detail, name="detail"),
    path("admin_page/", views.admin_page, name="admin_page"),
    path("upload_image/", views.upload_image, name="upload_image"),
    path('add_category/', views.add_category,name="add_category"),
    path('admin_page/update_category/', views.update_category, name="update_category"),
    path('detail/<picid>/count_download/', views.count_download, name="count_download"),
]