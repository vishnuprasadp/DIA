from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello, name='index'),
    path('deptlist',views.deptList,name='Organization'),
    path('deptdetail',views.deptDetail,name='Organization1'),
    path('article/<int:articleId>/', views.viewArticle, name = 'article'),
    path('articles/<int:year>/<int:month>/', views.viewArticles, name = 'articles'),
]