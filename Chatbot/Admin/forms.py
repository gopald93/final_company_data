from django import forms
from .models import *
from django.utils.safestring import mark_safe
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

class Google_Dialog_Flow_IntegrationForm(forms.ModelForm):
    class Meta:
        model = Google_Dialog_Flow_Integration
        fields = ('dialogflow_knowledge_base_id',
                  'default_bot_language_in_dialogflow',
                  'service_account_private_key_file')
        
class welcome_messagesform(forms.ModelForm):
    class Meta:
        model = welcome_messages
        fields = ('collect_email_id_from_anonymous_users','show_welcome_message_to_users',
            'default_language','default_welcome_message')  

        widgets = {'collect_email_id_from_anonymous_users': forms.RadioSelect(),
                    'show_welcome_message_to_users': forms.RadioSelect()} 


class Company_ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Company_Configuration 
        fields = ('company_name','company_urls','company_domain_name',)
       

class Chat_ConfigurationsForm(forms.ModelForm):
   class Meta:
        model = Chat_Configurations
        fields = (
               'cht_hty_rml_opt',
               'cht_hty_rml_dys',
               'cht_hty_rml_hrs',
               'cht_hty_rml_mnts',
               'bt_rpls_dly_prd',
               'no_of_thrd_alwd',
               'cht_wdgt_dply_inditr')
        widgets = {'cht_hty_rml_opt': forms.RadioSelect(),
                    'no_of_thrd_alwd': forms.RadioSelect(),
                   'cht_wdgt_dply_inditr':forms.RadioSelect()}

        labels  = {
               'cht_hty_rml_dys':'Chat history removal days',
               'cht_hty_rml_hrs':'Chat history removal hours',
               'cht_hty_rml_mnts':'Chat history removal minutes',
               'bt_rpls_dly_prd':'Bot replies delay period',
               'no_of_thrd_alwd':'Number of thread allowed',
               'cht_wdgt_dply_inditr':'Chat widget display indicator'
           }

class Custom_Choice_Field_For_Default_Icon_For_Bots(forms.ModelChoiceField):
   def label_from_instance(self, obj):
       return mark_safe('''<img src='http://127.0.0.1:8000{}'style="width: 8%;"/>'''.format(obj.image_path.url))

class Chat_Widget_Customization_Form(forms.ModelForm):  
  default_icon_for_bots = Custom_Choice_Field_For_Default_Icon_For_Bots(widget=forms.RadioSelect,queryset=Image_Gallery.objects.all(),required=False)
  class Meta:
    model = Chat_Widget_Customization
    fields = ['clr_cht_bt','upld_cstm_icon','wdgt_pos_on_the_scrn','ntn_snd_fr_bt','mfn_shwg_indct']
    widgets = {'wdgt_pos_on_the_scrn': forms.RadioSelect(),
                'mfn_shwg_indct':forms.RadioSelect()}
    labels  = {
            'clr_cht_bt':'Color chat bot',
            'upld_cstm_icon':'Custom icon for bots',
            'wdgt_pos_on_the_scrn':'Widget position on the screen',
            'ntn_snd_fr_bt':'Notification sound for bot',
            'mfn_shwg_indct':'show the modefin branding indicator'}            



def validation_of_exiting_user(field):
    user_data=list(User.objects.values_list('username','email'))
    for user in user_data:
        if field in user:
            return True
    return False    
    
USER_STATUS= (('Super Admin', 'Super Admin'), ('Teammates', 'Teammates'))
class CustomUserCreationForm(forms.Form):
    first_name=forms.CharField(label='Enter first name',min_length=4, max_length=150,required=True)
    last_name=forms.CharField(label='Enter last name', min_length=4, max_length=150,required=True)
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150,required=True)
    email = forms.EmailField(label='Enter email',required=True)
    password= forms.CharField(label='Enter password', widget=forms.PasswordInput,required=True)
    user_status= forms.CharField(label='Role of the user', widget=forms.RadioSelect(choices=USER_STATUS))
    bot=forms.ModelChoiceField(queryset=Bot_Details.objects.all(),required=True)
    def clean_username(self):
        username = self.cleaned_data['username']
        if validation_of_exiting_user(username)==True:
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if validation_of_exiting_user(email)==True:
            raise  ValidationError("Email already exists")
        return email
 
class User_Edit_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']             
Custom_User_Edit_Formset = inlineformset_factory(User,Custom_User_Model,fields=('bot_id','user_status'), can_delete=False, extra=1)            