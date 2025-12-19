from django.urls import path
from . import views

urlpatterns = [
    # Reviews
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:pk>/helpful/', views.ReviewHelpfulView.as_view(), name='review-helpful'),
    path('reviews/<int:review_id>/images/', views.ReviewImagesView.as_view(), name='review-images'),
    
    # Provider reviews
    path('providers/<int:provider_id>/reviews/', views.ProviderReviewsView.as_view(), name='provider-reviews'),
    path('providers/top-rated/', views.TopRatedProvidersView.as_view(), name='top-rated-providers'),
    
    # Reports
    path('reports/', views.ProviderReportCreateView.as_view(), name='report-create'),
    path('reports/list/', views.ProviderReportListView.as_view(), name='report-list'),
    path('reports/<int:pk>/', views.ProviderReportDetailView.as_view(), name='report-detail'),
]