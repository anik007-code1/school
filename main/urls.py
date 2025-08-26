from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('notices/', views.notices, name='notices'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('teachers/', views.teachers, name='teachers'),
    path('other-employee/', views.other_employee, name='other_employee'),
    path('committee/', views.committee, name='committee'),
    path('headmaster/', views.headmaster, name='headmaster'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/image/<int:image_id>/', views.gallery_image_detail, name='gallery_detail'),
    path('contact/', views.contact, name='contact'),
    path('students/', views.students, name='students'),
    path('exam-results/', views.exam_results, name='exam_results'),
    path('exam-result/<int:result_id>/', views.exam_result_detail, name='exam_result_detail'),

    # Custom Admin URLs
    # path('custom-admin/', views.custom_admin, name='custom_admin'),
    
    # # Notice Management
    # path('custom-admin/notices/', views.notice_list, name='notice_list'),
    # path('custom-admin/notices/add/', views.notice_add, name='notice_add'),
    # path('custom-admin/notices/<int:notice_id>/edit/', views.notice_edit, name='notice_edit'),
    # path('custom-admin/notices/<int:notice_id>/delete/', views.notice_delete, name='notice_delete'),
    
    # # Teacher Management
    # path('custom-admin/teachers/', views.teacher_list, name='teacher_list'),
    # path('custom-admin/teachers/add/', views.teacher_add, name='teacher_add'),
    # path('custom-admin/teachers/<int:teacher_id>/edit/', views.teacher_edit, name='teacher_edit'),
    # path('custom-admin/teachers/<int:teacher_id>/delete/', views.teacher_delete, name='teacher_delete'),
    
    # # Other Employee Management
    # path('custom-admin/other-employees/', views.other_employee_list, name='other_employee_list'),
    # path('custom-admin/other-employees/add/', views.other_employee_add, name='other_employee_add'),
    # path('custom-admin/other-employees/<int:employee_id>/edit/', views.other_employee_edit, name='other_employee_edit'),
    # path('custom-admin/other-employees/<int:employee_id>/delete/', views.other_employee_delete, name='other_employee_delete'),
    
    # # Committee Member Management
    # path('custom-admin/committee-members/', views.committee_member_list, name='committee_member_list'),
    # path('custom-admin/committee-members/add/', views.committee_member_add, name='committee_member_add'),
    # path('custom-admin/committee-members/<int:member_id>/edit/', views.committee_member_edit, name='committee_member_edit'),
    # path('custom-admin/committee-members/<int:member_id>/delete/', views.committee_member_delete, name='committee_member_delete'),
    
    # # Headmaster Management
    # path('custom-admin/headmasters/', views.headmaster_list, name='headmaster_list'),
    # path('custom-admin/headmasters/add/', views.headmaster_add, name='headmaster_add'),
    # path('custom-admin/headmasters/<int:headmaster_id>/edit/', views.headmaster_edit, name='headmaster_edit'),
    # path('custom-admin/headmasters/<int:headmaster_id>/delete/', views.headmaster_delete, name='headmaster_delete'),
    
    # # Exam Result Management
    # path('custom-admin/exam-results/', views.exam_result_list, name='exam_result_list'),
    # path('custom-admin/exam-results/add/', views.exam_result_add, name='exam_result_add'),
    # path('custom-admin/exam-results/<int:result_id>/edit/', views.exam_result_edit, name='exam_result_edit'),
    # path('custom-admin/exam-results/<int:result_id>/delete/', views.exam_result_delete, name='exam_result_delete'),
    
    # # Homepage Slider Management
    # path('custom-admin/sliders/', views.slider_list, name='slider_list'),
    # path('custom-admin/sliders/add/', views.slider_add, name='slider_add'),
    # path('custom-admin/sliders/<int:slider_id>/edit/', views.slider_edit, name='slider_edit'),
    # path('custom-admin/sliders/<int:slider_id>/delete/', views.slider_delete, name='slider_delete'),
    
    # # Gallery Category Management
    # path('custom-admin/gallery-categories/', views.gallery_category_list, name='gallery_category_list'),
    # path('custom-admin/gallery-categories/add/', views.gallery_category_add, name='gallery_category_add'),
    # path('custom-admin/gallery-categories/<int:category_id>/edit/', views.gallery_category_edit, name='gallery_category_edit'),
    # path('custom-admin/gallery-categories/<int:category_id>/delete/', views.gallery_category_delete, name='gallery_category_delete'),
    
    # # Gallery Image Management
    # path('custom-admin/gallery-images/', views.gallery_image_list, name='gallery_image_list'),
    # path('custom-admin/gallery-images/add/', views.gallery_image_add, name='gallery_image_add'),
    # path('custom-admin/gallery-images/<int:image_id>/edit/', views.gallery_image_edit, name='gallery_image_edit'),
    # path('custom-admin/gallery-images/<int:image_id>/delete/', views.gallery_image_delete, name='gallery_image_delete'),
    
    # # School Info Management
    # path('custom-admin/school-info/', views.school_info_list, name='school_info_list'),
    # path('custom-admin/school-info/add/', views.school_info_add, name='school_info_add'),
    # path('custom-admin/school-info/<int:info_id>/edit/', views.school_info_edit, name='school_info_edit'),
    # path('custom-admin/school-info/<int:info_id>/delete/', views.school_info_delete, name='school_info_delete'),
    
    # # Contact Info Management
    # path('custom-admin/contact-info/', views.contact_info_list, name='contact_info_list'),
    # path('custom-admin/contact-info/add/', views.contact_info_add, name='contact_info_add'),
    # path('custom-admin/contact-info/<int:info_id>/edit/', views.contact_info_edit, name='contact_info_edit'),
    # path('custom-admin/contact-info/<int:info_id>/delete/', views.contact_info_delete, name='contact_info_delete'),
    
    # # Exam Type Management
    # path('custom-admin/exam-types/', views.exam_type_list, name='exam_type_list'),
    # path('custom-admin/exam-types/add/', views.exam_type_add, name='exam_type_add'),
    # path('custom-admin/exam-types/<int:type_id>/edit/', views.exam_type_edit, name='exam_type_edit'),
    # path('custom-admin/exam-types/<int:type_id>/delete/', views.exam_type_delete, name='exam_type_delete'),
    
    # # Student Class Management
    # path('custom-admin/student-classes/', views.student_class_list, name='student_class_list'),
    # path('custom-admin/student-classes/add/', views.student_class_add, name='student_class_add'),
    # path('custom-admin/student-classes/<int:class_id>/edit/', views.student_class_edit, name='student_class_edit'),
    # path('custom-admin/student-classes/<int:class_id>/delete/', views.student_class_delete, name='student_class_delete'),
    
    # # Classwise Student Count Management
    # path('custom-admin/student-counts/', views.student_count_list, name='student_count_list'),
    # path('custom-admin/student-counts/add/', views.student_count_add, name='student_count_add'),
    # path('custom-admin/student-counts/<int:count_id>/edit/', views.student_count_edit, name='student_count_edit'),
    # path('custom-admin/student-counts/<int:count_id>/delete/', views.student_count_delete, name='student_count_delete'),
    
    # Language Switcher
    path('switch-language/<str:language_code>/', views.switch_language, name='switch_language'),
]
