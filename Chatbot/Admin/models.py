from django.db import models
from django.conf.global_settings import LANGUAGES
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from colorful.fields import RGBColorField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Statement(models.Model):
    text = models.TextField(null=True, blank=True)
    
    def __str__(self):
       return self.text

class Message(models.Model):
    statement = models.OneToOneField(Statement, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)
    intent = models.CharField(max_length=100, blank=True)
    reply_status= models.BooleanField(default=False,null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    owner_response=models.TextField(null=True, blank=True)
    class Meta:
        ordering = ['created_date']
    def __str__(self):
        return self.response

class Company_Configuration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cid = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100,blank=True)
    company_urls=models.URLField(max_length = 200,blank=True)
    company_domain_name=models.CharField(max_length=300,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.company_name

LANGUAGE_CHOICES = (("English","English"),
              ("Mandarin Chinese", "Mandarin Chinese"),
              ("Hindi", "Hindi"),
              ("Spanish", "Spanish"),
              ("Arabic", "Arabic"),
              ("Bangla", "Bangla"),
              ("Russian", "Russian"),
              ("Portuguese", "Portuguese"),
              ("Indonesian", "Indonesian"),
              ("Urdu", "Urdu"),)
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
class welcome_messages(models.Model):
    cid = models.ForeignKey(Company_Configuration, on_delete=models.CASCADE)
    collect_email_id_from_anonymous_users = models.BooleanField(choices=BOOL_CHOICES,null=True, blank=True,default=False)
    show_welcome_message_to_users=models.BooleanField(choices=BOOL_CHOICES,null=True, blank=True,default=False)
    default_language=MultiSelectField(choices=LANGUAGE_CHOICES)
    default_welcome_message = models.TextField(blank=True)
     
class Bot_Details(models.Model):
    bot_id= models.AutoField(primary_key=True)
    cid = models.ForeignKey(Company_Configuration,on_delete=models.CASCADE)
    icon_type= models.CharField(max_length=100,blank=True)
    position= models.BooleanField(default=False)
    iconIndex=models.IntegerField(blank=True,null=True)
    popup=models.BooleanField(default=False)
    notificationTone= models.CharField(max_length=100,blank=True)
    primaryColor= models.CharField(max_length=100,blank=True)
    secondaryColor=models.CharField(max_length=100,blank=True)
    showPoweredBy=models.BooleanField(default=False)
    collectFeedback=models.BooleanField(default=False)
    botMessageDelayInterval=models.IntegerField(blank=True,null=True)
    def __str__(self):
      return str(self.bot_id)
    
class Google_Dialog_Flow_Integration(models.Model):
    bot_id=models.ForeignKey(Bot_Details,on_delete=models.CASCADE)
    dialogflow_knowledge_base_id = models.CharField(max_length=255)
    default_bot_language_in_dialogflow=models.CharField(max_length=100, choices=LANGUAGES)
    service_account_private_key_file=models.FileField(upload_to='documents/',blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.dialogflow_knowledge_base_id

Chat_Session_History_Remove_Option=(('First_Option',"Remove chat widget history after a set period of time"),
             ('Second_Option',"Remove chat session history on page refresh"))

class Chat_Configurations(models.Model):
    ccid= models.AutoField(primary_key=True)
    # Chat_Configurations_id
    bot_id=models.ForeignKey(Bot_Details,on_delete=models.CASCADE)
    # chat_session_history_remove_option
    cht_hty_rml_opt = models.CharField(max_length=100, choices=Chat_Session_History_Remove_Option,default='First_Option')
    #chat_history_removal_days
    cht_hty_rml_dys=models.IntegerField(blank=True,null=True,help_text="30 days")
    # chat_history_removal_hours
    cht_hty_rml_hrs=models.IntegerField(blank=True,null=True,help_text="10 hours")
    # chat_history_removal_minutes
    cht_hty_rml_mnts=models.IntegerField(blank=True,null=True,help_text="30 minutes")
    #bot_replies_delay_period
    bt_rpls_dly_prd=models.IntegerField(blank=True,null=True,help_text="0 second")
    #no_of_thread_allowed
    no_of_thrd_alwd=models.BooleanField(choices=BOOL_CHOICES,default=True)
    #chat_widget_display_indicator
    cht_wdgt_dply_inditr=models.BooleanField(choices=BOOL_CHOICES,default=True)
    def __str__(self):
      return str(self.ccid)

WIDGET_POSITION_ON_THE_SCREEN=(('Left', 'Left'), 
                              ('Right', 'Right')
                              )
NOTIFICATION_SOUND_FOR_BOT=(('First', 'First'),
                            ('Second', 'Second'),
                            ('Third', 'Third'),
                            ('Fourth', 'Fourth'),
                            ('Fifth', 'Fifth')
                            )

class Image_Gallery(models.Model):
  image_name = models.CharField(primary_key=True,max_length=200)
  image_path= models.ImageField(upload_to='images/',unique=True)
  def __str__(self):
    return self.image_name

class Chat_Widget_Customization(models.Model):
  #Chat_Widget_Customization id
  cwc_id=models.AutoField(primary_key=True)
  #bot id
  bot_id=models.ForeignKey(Bot_Details,on_delete=models.CASCADE)
  #color_chat_bot
  clr_cht_bt = RGBColorField()
  # default_icon_for_bots
  dflt_icn_fr_bts=models.ForeignKey(Image_Gallery,on_delete=models.CASCADE,null=True, blank=True)
  #custom_icon_for_bots
  upld_cstm_icon= models.ImageField(upload_to='images/',blank=True,null=True)
  # widget_position_on_the_screen
  wdgt_pos_on_the_scrn = models.CharField(max_length=100, choices=WIDGET_POSITION_ON_THE_SCREEN,default='Left')
  # notification_sound_for_bot
  ntn_snd_fr_bt = models.CharField(max_length=100, choices=NOTIFICATION_SOUND_FOR_BOT,default='First')
  #show the modefin branding indicator
  mfn_shwg_indct=models.BooleanField(choices=BOOL_CHOICES,default=True)

  def __str__(self):
   return str(self.cwc_id)


USER_STATUS= (('Super Admin', 'Super Admin'), ('Teammates', 'Teammates'))
class Custom_User_Model(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bot_id= models.ForeignKey(Bot_Details,on_delete=models.CASCADE,null=True, blank=True)
    user_status= models.CharField(max_length=100, choices=USER_STATUS,default='Teammates')  
    module= models.CharField(max_length=20, null=True, blank=True)
    sub_module=models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return "{0}".format(self.user.username)

@receiver(post_save, sender=User)
def custom_user_is_created(sender,instance,created,**kwargs):
    if created:
      custom_user_model_obj,custom_user_created_indicator=Custom_User_Model.objects.update_or_create(user=instance,defaults={'user_status':'Super Admin'})        