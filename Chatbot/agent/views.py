from django.http import HttpResponse
from django.shortcuts import render
from Admin.models import Statement,Message
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from Chatbot.decorators import admin_only,allowed_user

@login_required(login_url="/login/")
@allowed_user(allowed_roles=['Super Admin','Teammates'])
def conversations(request):
    context={}
    context["message"]="conversations is about the to develop"
    return render(request, "agent/conversations.html",context)    

@login_required(login_url="/login/")
@allowed_user(allowed_roles=['Super Admin','Teammates'])
def dashboard(request):
    total_obj=Message.objects.all()
    count=0
    total_count_list=[['CREATED_DATETIME','COUNT']]
    for field in total_obj:
        if field.reply_status==True:
            count=count+1
        if field.reply_status==False:
            count=count-1

        created_date=(field.created_date).strftime("(%Y,%m,%d,%H)")
        total_count=count
        total_count_list.append([created_date,total_count])
    total_count_list_json=json.dumps(total_count_list)

    total_messages=Message.objects.all().count()
    total_messages_json=json.dumps(total_messages)

    total_true_messages=Message.objects.filter(reply_status=True).count()
    total_true_messages_json=json.dumps(total_true_messages)

    total_failed_messages=Message.objects.filter(reply_status=False).count()
    total_failed_messages_json=json.dumps(total_failed_messages)

    if request.method=='POST':
        # ALL COUNT GRAPH
        from_date=request.POST.get('from_date')
        f_date=tuple(from_date.split()[0].split('/'))
        f_time=tuple(from_date.split()[1].split(':'))
        from_datetime_str=f_date+f_time
        from_date_converted=datetime(int(from_datetime_str[2]),int(from_datetime_str[0]),int(from_datetime_str[1]),int(from_datetime_str[3]),int(from_datetime_str[4]))


        to_date=request.POST.get('to_date')
        t_date=tuple(to_date.split()[0].split('/'))
        t_time=tuple(to_date.split()[1].split(':'))
        to_datetime_str=t_date+t_time
        to_date_converted=datetime(int(to_datetime_str[2]),int(to_datetime_str[0]),int(to_datetime_str[1]),int(to_datetime_str[3]),int(to_datetime_str[4]))

        #TOTAL COUNT GRAPH

        total_obj=Message.objects.filter(created_date__range=(from_date_converted,to_date_converted))

        count=0
        total_count_list=[['CREATED_DATETIME','TOTAL_COUNT']]
        for field in total_obj:
            if field.reply_status==True:
                count=count+1
            if field.reply_status==False:
                count=count-1

            created_date=(field.created_date).strftime("(%Y,%m,%d,%H)")
            total_count=count
            total_count_list.append([created_date,total_count])
            print(created_date)

        total_count_list_json=json.dumps(total_count_list)

        total_messages=total_obj.count()
        total_messages_json=json.dumps(total_messages)

        total_true_messages=total_obj.filter(reply_status=True).count()
        total_true_messages_json=json.dumps(total_true_messages)

        total_failed_messages=total_obj.filter(reply_status=False).count()
        total_failed_messages_json=json.dumps(total_failed_messages)

        return render(request,"agent/dashboard.html",{'total_count_list_json':total_count_list_json,'from_date':from_date,'to_date':to_date,'total_messages_json':total_messages_json,'total_true_messages_json':total_true_messages_json,'total_failed_messages_json':total_failed_messages_json})

    return render(request,"agent/dashboard.html",{'total_count_list_json':total_count_list_json,'from_date':"Select",'to_date':"Select",'total_messages_json':total_messages_json,'total_true_messages_json':total_true_messages_json,'total_failed_messages_json':total_failed_messages_json})

