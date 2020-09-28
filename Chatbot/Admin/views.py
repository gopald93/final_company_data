from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf.global_settings import LANGUAGES
from django.shortcuts import render
from .forms import *
from multiselectfield import MultiSelectField
from Admin.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from Chatbot.decorators import admin_only,allowed_user

def user_login(request):
    if request.user.is_authenticated:
        user_status = request.user.custom_user_model.user_status
        if user_status=='Super Admin':
            return redirect('custom_user_list')
        else:  
            return redirect('dashboard')    
    else:       
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                user_status = request.user.custom_user_model.user_status
                if user_status=='Super Admin':
                    return redirect('custom_user_list')
                else:  
                    return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')
        return render(request, 'Admin/login.html', context)

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url="/login/")
@admin_only
def bots(request):
    context={}
    context["message"]=" bots is about the to develop"
    return render(request, "Admin/bots.html",context)  

@login_required(login_url="/login/")
@admin_only
def bot_integrations(request):
    context={}
    context["message"]=" bot_integrations is about the to develop"
    return render(request, "Admin/bot_integrations.html",context)  

@login_required(login_url="/login/")
@admin_only
def teammates(request):
    context={}
    context["message"]=" teammates is about the to develop"
    return render(request, "Admin/teammates.html",context)

@login_required(login_url="/login/")
@admin_only
def agents_activities(request):
    context={}
    context["message"]="Agents Activities is about the to develop"
    return render(request, "Admin/agents_activities.html",context)    

@login_required(login_url="/login/")
@admin_only
def customer_rating(request):
    context={}
    context["message"]="Customer Rating is about the to develop"
    return render(request, "Admin/customer_rating.html",context) 

@login_required(login_url="/login/")
@admin_only
def setting(request):
    context={}
    context["message"]=" settings  is about the to develop"
    return render(request, "Admin/settings.html",context)    

@login_required(login_url="/login/")
@admin_only
def welcome_message(request):
    company_configuration_obj = get_object_or_404(Company_Configuration,pk=2)
    if request.method == "POST":
        form = welcome_messagesform(request.POST)
        if form.is_valid():
            welcome_messages_obj = form.save(commit=False)
            welcome_messages_obj.cid = company_configuration_obj
            welcome_messages_obj.save()
            return redirect('teammates')
    else:
        form = welcome_messagesform()
    return render(request, "Admin/welcome_message.html", {'form': form})
@login_required(login_url="/login/")
@admin_only
def company_details(request):
    user_obj = get_object_or_404(User,pk=1)
    if request.method == "POST":
        form = Company_ConfigurationForm(request.POST)
        if form.is_valid():
            company_configuration_obj = form.save(commit=False)
            company_configuration_obj.user = user_obj
            company_configuration_obj.save()
            return redirect('teammates')
    else:
        form = Company_ConfigurationForm()
    return render(request, "Admin/company_details.html", {'form': form})
@login_required(login_url="/login/")
@admin_only
def google_dialog_flow_integration(request):
    bot_details_obj = get_object_or_404(Bot_Details,pk=1)
    if request.method == "POST":
        form = Google_Dialog_Flow_IntegrationForm(request.POST,request.FILES)
        if form.is_valid():
            service_account_private_key_file=form.cleaned_data['service_account_private_key_file']
            google_dialog_flow_integration_obj = form.save(commit=False)
            google_dialog_flow_integration_obj.bot_id = bot_details_obj
            google_dialog_flow_integration_obj.save()
            return redirect('teammates')
    else:
        form = Google_Dialog_Flow_IntegrationForm()
    return render(request, 'Admin/google_dialog_flow_integration.html', {'form': form})
@login_required(login_url="/login/")
@admin_only
def configuration(request):
    bot_details_obj = get_object_or_404(Bot_Details,pk=1)
    if request.method == "POST":
        form = Chat_ConfigurationsForm(request.POST)
        if form.is_valid():
            chat_configurations = form.save(commit=False)
            chat_configurations.bot_id= bot_details_obj
            chat_configurations.save()
            return redirect('teammates')
    else:
        form = Chat_ConfigurationsForm()
    return render(request, 'Admin/configuration.html', {'form': form})
@login_required(login_url="/login/")
@admin_only
def customisation(request):
    bot_details_obj = get_object_or_404(Bot_Details,pk=1)
    if request.method == 'POST':
        form = Chat_Widget_Customization_Form(request.POST, request.FILES)
        if form.is_valid():
            default_icon_for_bots = form.cleaned_data['default_icon_for_bots']
            company_chat_widget_customization_obj = form.save(commit=False)
            company_chat_widget_customization_obj.bot_id = bot_details_obj
            company_chat_widget_customization_obj.dflt_icn_fr_bts = default_icon_for_bots
            company_chat_widget_customization_obj.save()
            return redirect('teammates')
    else:
        form = Chat_Widget_Customization_Form()
    return render(request, 'Admin/customisation.html', {'form' : form})
############Teammates operation##################

@login_required(login_url="/login/")
@admin_only
def custom_user_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Teammates'
    return render(request, 'Admin/custom_user_list.html', context) 

@login_required(login_url="/login/")
@admin_only
def custom_user_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            encripted_password=make_password(form.cleaned_data.get('password'))
            user_obj,user_created_indicator = User.objects.update_or_create(username=form.cleaned_data.get('username'),defaults={'first_name':form.cleaned_data.get('first_name'),'last_name':form.cleaned_data.get('last_name'),'email':form.cleaned_data.get('email'),'password':encripted_password})
            custom_user_model_obj,custom_user_created_indicator=Custom_User_Model.objects.update_or_create(user=user_obj,defaults={'bot_id':form.cleaned_data.get('bot'),'user_status':form.cleaned_data.get('user_status')})  
            return redirect('custom_user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Admin/custom_user_add.html', {'form': form})

@login_required(login_url="/login/")
@admin_only
def custom_user_edit(request,id=None):
    context={}
    context["Activites"]="Update Teammates"
    user_obj = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_edit_form_obj = User_Edit_Form(request.POST, instance=user_obj)
        if user_edit_form_obj.is_valid():
            user_edit_obj = user_edit_form_obj.save()
            custom_user_edit_formset_obj = Custom_User_Edit_Formset(request.POST,instance=user_edit_obj)
            if custom_user_edit_formset_obj.is_valid():
                custom_user_edit_formset_obj.save()
                return redirect('custom_user_list')
    else:
        context["form"]=User_Edit_Form(instance=user_obj)
        context["formset"]=Custom_User_Edit_Formset(instance=user_obj)   
        return render(request,'Admin/custom_user_edit.html',context)

@login_required(login_url="/login/")
@admin_only
def custom_user_delete(request,id=None):
    user = get_object_or_404(User, id=id)
    custom_user = get_object_or_404(Custom_User_Model, user=user.id)
    if request.method == 'POST':
        custom_user.delete()
        user.delete()
        return HttpResponseRedirect(reverse('custom_user_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'Admin/custom_user_delete.html', context)        
