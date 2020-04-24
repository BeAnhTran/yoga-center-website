from django.urls import include, path
from django.conf.urls import url

from .views import (
    dashboard_view, courses_view, rooms_view,
    lessons_view, classes_view, cards_view,
    card_types_view, trainees_view, trainers_view, staffs_view,
    admins_view, roll_calls_view, blog_view, make_up_lessons_view, shop_view, promotions_view, taught_view, gallery_view, events_view, faq_view)

from .views.requests import extend_card_requests_view, refund_requests_view

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
    url(r'^(?P<lesson_id>[0-9]+)/roll-calls-trainer/$', taught_view.rollCallForTrainer,
        name='lessons-roll-calls-for-trainer'),
]

# ROOMS
rooms_urlpatterns = [
    path('', rooms_view.RoomListView.as_view(), name='rooms-list'),
    path('<int:pk>/', rooms_view.RoomDetailView.as_view(), name='rooms-detail'),
    path('<int:pk>/lessons/',
         rooms_view.get_lessons, name='rooms-get-lessons'),
]

# CARDS
cards_urlpatterns = [
    path('', cards_view.CardListView.as_view(), name='cards-list'),
]

# CARD TYPES
card_types_urlpatterns = [
    path('', card_types_view.CardTypeListView.as_view(),
         name='card-types-list'),
    path('for-course/', card_types_view.get_card_types_for_course.as_view(),
         name='json-card-type-list-for-course'),
]

# TRAINEES
trainees_urlpatterns = [
    path('', trainees_view.TraineeListView.as_view(), name='trainees-list')
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

    # bills
    path('bills/', shop_view.BillListView.as_view(),
         name='shop-bills-list'),
]

# Extend Card Request
extend_card_requests_urlpatterns = [
    path('', extend_card_requests_view.ExtendCardRequestListView.as_view(),
         name='extend-card-requests-list'),
    path('<int:pk>/', extend_card_requests_view.ExtendCardRequestDetailView.as_view(),
         name='extend-card-requests-detail'),
    path('<int:pk>/update-state/', extend_card_requests_view.updateStateOfExtendCardRequest,
         name='extend-card-requests-update-state'),
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
    path('<int:pk>/edit/', promotions_view.PromotionEditView.as_view(),
         name='promotions-edit'),
    path('<int:pk>/codes/', promotions_view.PromotionCodeListView.as_view(),
         name='promotions-codes-list'),
    path('<int:pk>/codes/new/', promotions_view.createPromotionCode,
         name='promotions-codes-create'),
]

# GALLERY
gallery_urlpatterns = [
    path('', gallery_view.GalleryListView.as_view(),
         name='gallery-list'),
    path('new/', gallery_view.GalleryNewView.as_view(), name='gallery-new'),
    path('<int:pk>/', gallery_view.GalleryEditView.as_view(),
         name='gallery-edit'),
    path('<int:pk>/delete/', gallery_view.GalleryDeleteView.as_view(),
         name='gallery-delete'),
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
    path('extend-card-requests/', include(extend_card_requests_urlpatterns)),
    path('refund-requests/', include(refund_requests_urlpatterns)),
    path('promotions/', include(promotions_urlpatterns)),
    path('gallery/', include(gallery_urlpatterns)),
    path('events/', include(events_urlpatterns)),
    path('faq/', include(faq_urlpatterns)),
]
