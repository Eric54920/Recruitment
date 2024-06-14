from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("province/", views.ProvinceAPIView.as_view()),
    path("jobs/", views.JobsAPIView.as_view()),
    path("position/", views.PositionListAPIView.as_view()),

    path("position/add/", views.PsoitionViewset.as_view({'post': 'create'})),
    re_path("position/delete/(?P<pk>\d+)/$", views.PsoitionViewset.as_view({'delete': 'destroy'})),
    re_path("update/position/(?P<pk>\d+)/$", views.PositionRetrieveAPIView.as_view({'get': 'retrieve', 'post': 'partial_update'})),
    re_path("position/(?P<pk>\d+)/$", views.PositionAPIView.as_view({'get': 'retrieve'})),

    path("company/", views.CompanyListAPIView.as_view()),
    path("company/retrieve/", views.CompanyRetrieveAPIView.as_view({'post': 'create'})),
    re_path("company/retrieve/(?P<companyId>\d+)/$", views.CompanyRetrieveAPIView.as_view({'put': 'partial_update', 'get': 'retrieve'})),
    re_path("company/detail/(?P<companyId>\d+)/$", views.CompanyDetailAPIView.as_view({'get': 'retrieve'})),

    path("PosFilterRequire/", views.PosFilterRequire),
    path("ComFilterRequire/", views.ComFilterRequire),
    path("search/companyname/", views.search_company),
]