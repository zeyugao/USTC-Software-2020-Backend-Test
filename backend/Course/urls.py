from django.urls import path
from Course import views
app_name = 'Course'

urlpatterns = [
    path('listAllCourse',views.ListAllCourse,name = 'listAllCourse'),
    path('chooseCourse',views.ChooseCourse,name = 'chooseCourse'),
    path('quitCourse',views.QuitCourse,name = 'quitCourse'),
    path('listGradeCourse',views.ListGradeCourse,name = 'listGradeCourse'),
    path('listChosenCourse',views.ListChosenCourse,name = 'listChosenCourse'),
    path('listPreparatoryCourse',views.ListPreparatoryCourse,name = 'listPreparatoryCourse'),
]