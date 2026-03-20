from django.urls import path
from clinics.views import ClinicViewSet, ClinicRecommendationViewSet

urlpatterns = [
    # Clinic endpoints
    path('clinics/', ClinicViewSet.as_view({'get': 'all_clinics'}), name='clinic-list'),
    path('clinics/<uuid:clinic_id>/', ClinicViewSet.as_view({'get': 'clinic_detail'}), name='clinic-detail'),
    path('clinics/cities/', ClinicViewSet.as_view({'get': 'cities'}), name='clinic-cities'),
    path('clinics/specializations/', ClinicViewSet.as_view({'get': 'specializations'}), name='clinic-specializations'),
    
    # Recommendation endpoints
    path('recommendations/nearest/', ClinicRecommendationViewSet.as_view({'get': 'nearest_clinics'}), name='recommendation-nearest'),
    path('recommendations/create/', ClinicRecommendationViewSet.as_view({'post': 'create_recommendation'}), name='recommendation-create'),
    path('recommendations/user/', ClinicRecommendationViewSet.as_view({'get': 'user_recommendations'}), name='recommendation-user'),
    path('recommendations/<uuid:rec_id>/mark-contacted/', ClinicRecommendationViewSet.as_view({'put': 'mark_contacted'}), name='recommendation-contacted'),
    path('recommendations/<uuid:rec_id>/mark-viewed/', ClinicRecommendationViewSet.as_view({'put': 'mark_viewed'}), name='recommendation-viewed'),
]
