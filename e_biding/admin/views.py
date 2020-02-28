from django.contrib import messages
from django.shortcuts import render,redirect
from admin.models import AdminData, Complains
from admin.sms_service import sendSMS
from user.models import UserRegister
data = None


def contact_page(request):
    return redirect('/#Contact')


def about(request):
    return redirect('/#about')


def admin_login(request):
    if request.method == 'POST':
        aemail = request.POST.get("aemail")
        apassword = request.POST.get("apassword")
        try:
            global data
            data = AdminData.objects.get(email=aemail, password=apassword)
            request.session["aemail"] = aemail
            return render(request, "admin/welcome.html", {'data':data, 'msg':'Welcome '})
        except:
            messages.error(request, "You enter a wrong email or password.")
            return render(request, "admin/login.html")
    else:
        try:
            if request.session["aemail"]:
                aemail = request.session["aemail"]
                data = AdminData.objects.get(email=aemail)
                return render(request, "admin/welcome.html", {'data': data})
            else:
                return render(request, 'admin/login.html')
        except:
            return render(request, 'admin/login.html')


def admin_logout(request):
    del request.session["aemail"]
    global data
    data = None
    return render(request, "admin/index.html")


def welcome(request):
    if request.session["aemail"]:
        aemail = request.session["aemail"]
        data = AdminData.objects.get(email=aemail)
        return render(request, "admin/welcome.html", {'data': data})
    else:
        return redirect('admin_login')


def pending_req(request):
    if request.session["aemail"]:
        aemail = request.session["aemail"]
        data = AdminData.objects.get(email=aemail)
        qs = UserRegister.objects.filter(status="pending")
        if qs:
            return render(request, 'admin/pad_table.html', {"preq":qs, "data":data})
        else:
            return render(request, 'admin/pad_table.html', {"msg":"No pending request !", "data":data})
    else:
        return redirect('admin_login')


def approved_req(request):
    if request.session["aemail"]:
        aemail = request.session["aemail"]
        data = AdminData.objects.get(email=aemail)
        qs = UserRegister.objects.filter(status="approved")
        if qs:
            return render(request, 'admin/pad_table.html', {"areq":qs, "data":data})
        else:
            return render(request, 'admin/pad_table.html', {"msg":"No approved request !", "data":data})
    else:
        return redirect('admin_login')


def declined_req(request):
    if request.session["aemail"]:
        aemail = request.session["aemail"]
        data = AdminData.objects.get(email=aemail)
        qs = UserRegister.objects.filter(status="declined")
        if qs:
            return render(request, 'admin/pad_table.html', {"dreq":qs, "data":data})
        else:
            return render(request, 'admin/pad_table.html', {"msg":"No declined request !", "data":data})
    else:
        return redirect('admin_login')


def approve(request, pk):
    if request.session["aemail"]:
        qs = UserRegister.objects.filter(id=pk)
        name = ""
        cno = ""
        u = ""
        p = ""
        for x in qs:
            name = x.name
            cno = x.phone
            u = x.username
            p = x.password
        qs.update(status="approved")
        mess = "Hello Mr/miss "+name+". Your registration is approved by E-Bidding. Your Username = "+u+" and password = "+p+", don't share with any one."
        x = sendSMS(str(cno), mess)
        print(x)
        return redirect('approved_req')
    else:
        return redirect('admin_login')


def decline(request, pk, name):
    if request.session["aemail"]:
        aemail = request.session["aemail"]
        data = AdminData.objects.get(email=aemail)
        return render(request, "admin/decline_confirm.html", {"data":data, "id":pk, "name":name})
    else:
        return redirect('admin_login')


def decline_confirm(request, pk):
    if request.session["aemail"]:
        UserRegister.objects.filter(id=pk).update(status="declined")
        return redirect('declined_req')
    else:
        return redirect('admin_login')


def changepass(request):
    if request.session["aemail"]:
        aemail = request.session["aemail"]
        data = AdminData.objects.get(email=aemail)
        if request.method == 'POST':
            old = request.POST["old"]
            new1 = request.POST["new1"]
            new2 = request.POST["new2"]
            try:
                AdminData.objects.get(password=old)
                if new1 == new2:
                    AdminData.objects.filter(id=data.id).update(password=new1)
                    return render(request, "admin/welcome.html", {"data":data, "msg":"Password changed successfully."})
                else:
                    return render(request, "admin/change_pass.html",
                                  {"data":data, "msg2":"New password and Confirm password must be same !"})
            except:
                return render(request, "admin/change_pass.html",
                              {"data": data, "msg1": "Old password not matched try again !"})
        else:
            return render(request, "admin/change_pass.html",{"data":data})
    else:
        return redirect('admin_login')


def complain(request):
    if request.session["aemail"]:
        aemail = request.session["aemail"]
        data = AdminData.objects.get(email=aemail)
        if request.method == 'POST':
            name = request.POST["name"]
            email = request.POST["email"]
            subject = request.POST["subject"]
            message = request.POST["message"]
            Complains(name=name, email=email, subject=subject, description=message).save()
            messages.success(request, "Send successfully.")
            return redirect('contact')
        else:
            qs = Complains.objects.all()
            if qs:
                return render(request, "admin/complains.html", {"data": data,"complains": qs})
            return render(request, "admin/complains.html", {"data": data, "msg":"No complains !"})
    else:
        return redirect('admin_login')


def del_complain(request, pk):
    if request.session["aemail"]:
        Complains.objects.get(id=pk).delete()
        messages.success(request, "Successfully deleted.")
        return redirect('complain')
    else:
        return redirect('admin_login')
