# C:\PORTFOLIO\Web_Developer\AmazingBlogApp\BlogAppEnv\blognews\api\urls.py
from django.urls import path
from .views import ArticleListCreateView, ArticleDetailView, CategoryListCreateView, CommentListCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('v1/articles/', ArticleListCreateView.as_view(), name='article-list'),
    path('v1/articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('v1/categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('v1/articles/<int:article_id>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]