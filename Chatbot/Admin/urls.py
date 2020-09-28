from django.urls import path
from Admin.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('bots/', bots, name='bots'),
    path('bots/bot_integrations',bot_integrations, name='bots/bot_integrations'),
    path('bots/bot_integrations/google_dialog_flow_integration',google_dialog_flow_integration, name='bots/bot_integrations/google_dialog_flow_integration'),
    path('company/company_details',company_details, name='company/company_details'),
    path('company/teammates',teammates, name='company/teammates'),
    path('teammates/', teammates, name='teammates'),
    path('agents_activities/', agents_activities, name='agents_activities'),
    path('customer_rating/', customer_rating, name='customer_rating'),
    path('setting/', setting, name='setting'),
    path('chat_widget/configuration/',configuration, name='chat_widget/configuration'),
    path('chat_widget/customisation/', customisation, name='chat_widget/customisation/'),
    path('chat_widget/welcome_message/', welcome_message, name='chat_widget/welcome_message/'),
    path('company/teammates/custom_user_list', custom_user_list, name='custom_user_list'),
    path('company/teammates/custom_user_add/', custom_user_add, name="custom_user_add"),
    path('company/teammates/<int:id>/custom_user_edit/', custom_user_edit, name="custom_user_edit"),
    path('company/teammates/<int:id>/custom_user_delete/', custom_user_delete, name="custom_user_delete"),
    ]