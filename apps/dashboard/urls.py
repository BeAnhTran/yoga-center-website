from django.urls import include, path
from django.conf.urls import url

from .views import (
    dashboard_view, courses_view, rooms_view,
    lessons_view, classes_view, cards_view,
    card_types_view, trainees_view, trainers_view, staffs_view,
    admins_view, roll_calls_view, blog_view, make_up_lessons_view, shop_view, promotions_view, taught_view, events_view, faq_view, questions_view, feedback_view, trainers_salary_view)

from .views.requests import refund_requests_view

app_name = 'dashboard'

# COURSE
courses_urlpatterns = [
    path('', courses_view.CourseListView.as_view(), name='courses-list'),
    path('new/', courses_view.CourseNewView.as_view(), name='courses-new'),
    url(r'^edit/(?P<slug>[\w-]+)/$',
        courses_view.CourseEditView.as_view(), name='courses-update'),
    path('<int:pk>/delete/',
         courses_view.CourseDeleteView.as_view(), name='courses-delete'),
]

# CLASSES
classes_urlpatterns = [
    path('', classes_view.ClassListView.as_view(), name='classes-list'),
    path('new/', classes_view.ClassNewView.as_view(), name='classes-new'),
    path('<int:pk>/', classes_view.ClassDetailView.as_view(),
         name='classes-detail'),
    path('<int:pk>/schedule/',
         classes_view.ClassScheduleView.as_view(), name='classes-schedule'),
    url(r'^edit/(?P<slug>[\w-]+)/$',
        classes_view.ClassEditView.as_view(), name='classes-update'),
    path('<int:pk>/delete/',
         classes_view.ClassDeleteView.as_view(), name='classes-delete'),
    path('<int:pk>/lessons/',
         classes_view.get_lessons, name='classes-get-lessons'),
    # create lesson for a class
    path('<int:pk>/lessons/new/',
         classes_view.create_lessons, name='classes-create-new-lesson'),
    path('<int:pk>/lessons/new/from-last-week/',
         classes_view.create_lessons_from_last_time, name='classes-create-new-lesson-from-last-time')
]

# LESSONS
lessons_urlpatterns = [
    path('', lessons_view.LessonListView.as_view(), name='lessons-list'),
    url(r'^(?P<pk>[0-9]+)$', lessons_view.LessonDetailApiView.as_view(),
        name='lessons-detail-json'),
    url(r'^(?P<pk>[0-9]+)/roll-calls/$', lessons_view.ListRollCallApiView.as_view(),
        name='lessons-roll-calls'),
    url(r'^(?P<pk>[0-9]+)/substitute-trainer/$', lessons_view.SubstituteTrainerApi.as_view(),
        name='lessons-substitute-trainer'),
    url(r'^(?P<pk>[0-9]+)/check-is-full-lesson/$', lessons_view.CheckFullLessonApi.as_view(),
        name='check-is-full-lesson'),
    url(r'^(?P<lesson_id>[0-9]+)/roll-calls-trainer/$', taught_view.rollCallForTrainer,
        name='lessons-roll-calls-for-trainer'),
]

# ROOMS
rooms_urlpatterns = [
    path('', rooms_view.RoomListView.as_view(), name='rooms-list'),
    path('new/', rooms_view.RoomNewView.as_view(), name='rooms-new'),
    path('<int:pk>/', rooms_view.RoomDetailView.as_view(), name='rooms-detail'),
    path('<int:pk>/edit/', rooms_view.RoomEditView.as_view(), name='rooms-edit'),
    path('<int:pk>/delete/', rooms_view.RoomDeleteView.as_view(), name='rooms-delete'),
    path('<int:pk>/lessons/',
         rooms_view.get_lessons, name='rooms-get-lessons'),
]

# CARDS
cards_urlpatterns = [
    path('', cards_view.CardListView.as_view(), name='cards-list'),
    path('new/', cards_view.CardNewIndexView.as_view(), name='cards-new-index'),
    path('<slug:slug>/new/', cards_view.CardNewView.as_view(),
         name='cards-new-for-class'),
    path('<slug:slug>/new-preview/', cards_view.CardNewPreviewView.as_view(),
         name='cards-new-for-class-preview'),
    path('new-result/<int:pk>/', cards_view.CardNewResultView.as_view(),
         name='cards-new-for-class-result'),
    path('unpaid-list/', cards_view.UnPaidCardListView.as_view(),
         name='unpaid-cards-list'),
    path('unpaid-list/<int:pk>/receive-payment/', cards_view.ReceiveCardPaymentView.as_view(),
         name='receive-card-payment'),
]

# CARD TYPES
card_types_urlpatterns = [
    path('', card_types_view.CardTypeListView.as_view(),
         name='card-types-list'),
    path('new/', card_types_view.CardTypeNewView.as_view(),
         name='card-types-new'),
    path('for-course/', card_types_view.get_card_types_for_course.as_view(),
         name='json-card-type-list-for-course'),
]

# TRAINEES
trainees_urlpatterns = [
    path('', trainees_view.TraineeListView.as_view(), name='trainees-list'),
    path('new/', trainees_view.TraineeNewView.as_view(), name='trainees-new'),
    path('training-class/', trainees_view.TrainingClassListView.as_view(),
         name='training-class-list'),
    path('training-class/<slug:slug>/', trainees_view.TraineeOfTrainingClassListView.as_view(),
         name='trainee-of-training-class-list'),
]

# TRAINERS
trainers_urlpatterns = [
    path('', trainers_view.TrainerListView.as_view(), name='trainers-list')
]

# STAFFS
staffs_urlpatterns = [
    path('', staffs_view.StaffListView.as_view(), name='staffs-list')
]

# STAFFS
admins_urlpatterns = [
    path('', admins_view.AdminListView.as_view(), name='admins-list')
]

# ROLL CALLS
roll_calls_urlpatterns = [
    path('<int:pk>/', roll_calls_view.RollCallDetail.as_view(),
         name='roll-calls-detail'),
    path('api/make-up-lessons/', roll_calls_view.RollCallListViewApi.as_view(),
         name='api-roll-calls-list-make-up-lesson'),
]

# BLOG
blog_urlpatterns = [
    # post category
    path('categories/', blog_view.PostCategoryListView.as_view(),
         name='blog-categories-list'),
    path('categories/new/', blog_view.PostCategoryNewView.as_view(),
         name='blog-categories-new'),
    path('categories/<slug:slug>/delete/',
         blog_view.PostCategoryDeleteView.as_view(), name='blog-categories-delete'),
    # post
    path('posts/', blog_view.PostListView.as_view(),
         name='blog-posts-list'),
    path('posts/new/', blog_view.PostNewView.as_view(),
         name='blog-posts-new'),
    path('posts/<slug:slug>/delete/',
         blog_view.PostDeleteView.as_view(), name='blog-posts-delete'),
]

# MAKE UP LESSON
make_up_lessons_urlpatterns = [
    path('', make_up_lessons_view.MakeUpLessonListApi.as_view(),
         name='make-up-lessons-list-api'),
    path('<int:pk>/roll_call/lessons/<int:lesson_id>/delete/',
         make_up_lessons_view.delete_make_up_lesson_roll_call, name='make-up-lessons-delete-in-lesson-roll-call'),
    path('<int:pk>/', make_up_lessons_view.MakeUpLessonDetailApiView.as_view(),
         name='make-up-lessons-detail-api'),
    path('<int:pk>/update/', make_up_lessons_view.UpdateMakeUpLessonStateApiView.as_view(),
         name='make-up-lessons-update-state-api'),
]

# SHOP
shop_urlpatterns = [
    # product category
    path('categories/', shop_view.ProductCategoryListView.as_view(),
         name='shop-categories-list'),
    path('categories/new/', shop_view.ProductCategoryNewView.as_view(),
         name='shop-categories-new'),
    path('categories/<slug:slug>/delete/',
         shop_view.ProductCategoryDeleteView.as_view(), name='shop-categories-delete'),

    # product
    path('products/', shop_view.ProductListView.as_view(),
         name='shop-products-list'),
    path('products/new/', shop_view.ProductNewView.as_view(),
         name='shop-products-new'),
    path('products-list-api/', shop_view.ProductListAPIView.as_view(),
         name='shop-products-list-api'),

    # bills
    path('bills/', shop_view.BillListView.as_view(),
         name='shop-bills-list'),
]

# Refund Request
refund_requests_urlpatterns = [
    path('', refund_requests_view.RefundRequestListView.as_view(),
         name='refund-requests-list'),
    path('<int:pk>/', refund_requests_view.RefundRequestDetailView.as_view(),
         name='refund-requests-detail'),
    path('<int:pk>/update-state/', refund_requests_view.updateStateOfRefundRequest,
         name='refund-requests-update-state'),
]

# PROMOTION
promotions_urlpatterns = [
    path('', promotions_view.PromotionListView.as_view(),
         name='promotions-list'),
    path('new/', promotions_view.PromotionNewView.as_view(),
         name='promotions-new'),
    path('<int:pk>/', promotions_view.PromotionDetailView.as_view(),
         name='promotions-detail'),
    path('<int:pk>/delete/', promotions_view.PromotionDeleteView.as_view(),
         name='promotions-delete'),
    path('<int:pk>/codes/', promotions_view.PromotionCodeListView.as_view(),
         name='promotions-codes-list'),
    path('<int:pk>/codes/new/', promotions_view.createPromotionCode,
         name='promotions-codes-create'),
]

# EVENTS
events_urlpatterns = [
    path('', events_view.EventListView.as_view(),
         name='events-list'),
    path('new/', events_view.EventNewView.as_view(),
         name='events-new'),
    path('<int:pk>/delete/', events_view.EventDeleteView.as_view(),
         name='events-delete'),
]

# FAQ
faq_urlpatterns = [
    path('', faq_view.FAQListView.as_view(),
         name='faq-list'),
    path('new/', faq_view.FAQNewView.as_view(),
         name='faq-new'),
    path('<int:pk>/edit/', faq_view.FAQEditView.as_view(),
         name='faq-edit'),
    path('<int:pk>/delete/', faq_view.FAQDeleteView.as_view(),
         name='faq-delete'),
]

# Question (of user)
questions_urlpatterns = [
    path('', questions_view.QuestionListView.as_view(),
         name='questions-list'),
]

# Feedback
feedback_urlpatterns = [
    path('', feedback_view.FeedbackListView.as_view(),
         name='feedback-list'),
]

# Salary
salary_urlpatterns = [
    path('trainers/', trainers_salary_view.IndexView.as_view(),
         name='salary-trainers-index'),
    path('trainers/<slug:slug>/', trainers_salary_view.DetailListYogaClassView.as_view(),
         name='salary-trainers-detail-list-class'),
    path('trainers/<slug:slug>/yoga-classes/<int:yoga_class_pk>/', trainers_salary_view.DetailYogaClassSalaryView.as_view(),
         name='salary-trainers-detail-class-detail'),
]

# DASHBOARD
urlpatterns = [
    path('', dashboard_view.index, name='index'),
    path('courses/', include(courses_urlpatterns)),
    path('classes/', include(classes_urlpatterns)),
    path('lessons/', include(lessons_urlpatterns)),
    path('rooms/', include(rooms_urlpatterns)),
    path('cards/', include(cards_urlpatterns)),
    path('card-types/', include(card_types_urlpatterns)),
    path('trainees/', include(trainees_urlpatterns)),
    path('trainers/', include(trainers_urlpatterns)),
    path('staffs/', include(staffs_urlpatterns)),
    path('admins/', include(admins_urlpatterns)),
    path('roll-calls/', include(roll_calls_urlpatterns)),
    path('blog/', include(blog_urlpatterns)),
    path('shop/', include(shop_urlpatterns)),
    path('make-up-lessons/', include(make_up_lessons_urlpatterns)),
    path('refund-requests/', include(refund_requests_urlpatterns)),
    path('promotions/', include(promotions_urlpatterns)),
    path('events/', include(events_urlpatterns)),
    path('faq/', include(faq_urlpatterns)),
    path('questions/', include(questions_urlpatterns)),
    path('feedback/', include(feedback_urlpatterns)),
    path('salary/', include(salary_urlpatterns)),
]
