from django.urls import path
from . import views
from django.utils.text import slugify

urlpatterns = [
    path('', views.index, name='index'),
    path('doc', views.doc, name='doc'),
    path('cluster/<int:id_project>/', views.cluster, name='cluster'),
    path('cluster_bilan/<int:id_project>/', views.cluster_bilan, name='cluster_bilan'),
    path('doc/post', views.post_datas, name='post_datas'),
    path('single_doc/<slug:pk>', views.single_doc, name='single_doc'),
    path('post-image-cluster', views.post_image, name='post_image_cluster'),
    path('valider_line', views.valider_line, name='valider_line'),
]