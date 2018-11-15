from django.urls import path, include
from academy.views import IndexView, TutorialView, VideoView, BrowseTutorialView, DashboardView, DashboardAdminCourses, AddCourse, EditCourse, DashboardAdminRank, DashboardAdminRankEdit, SubscriptionView, CheckoutView, PaystackVerifyView, AdminSubscriptionsView
from academy.models import Subscription
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings

app_name = 'academy'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('how-it-works/', TemplateView.as_view(template_name="pages/how-it-works.html"), name="how_it_works"),
    path('tutorial/<int:id>', TutorialView.as_view(), name="view_tuts"),
    path('browse/', BrowseTutorialView.as_view(), name="browse_tuts"),
    path('tutorial/<int:id>/video/<int:video>/', VideoView.as_view(), name="view_video"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('dashboard/user/subscription', TemplateView.as_view(template_name='user/subscription.html'), name="dashboard_subscription"),
    path('subscribe/', SubscriptionView.as_view(), name="subscribe"),
    path('subscribe/checkout', CheckoutView.as_view(), name="checkout"),
    path('paystack/callback', PaystackVerifyView.as_view(), name="paystack_callback"),
    path('dashboard/admin/courses', DashboardAdminCourses.as_view(), name="admin_courses"),
    path('dashboard/admin/courses/add', AddCourse.as_view(), name="add_course"),
    path('dashboard/admin/courses/<int:id>/edit', EditCourse.as_view(), name="edit_course"),
    path('dashboard/admin/ranks', DashboardAdminRank.as_view(), name="admin_ranks"),
    path('dashboard/admin/subscription', AdminSubscriptionsView.as_view(), name="admin_subscriptions"),
    path('dashboard/admin/ranks/<int:id>/edit', DashboardAdminRankEdit.as_view(), name="admin_ranks_edit"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
