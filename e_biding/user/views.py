import json

import requests
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from user.models import UserRegister
from admin.models import Products, MaxBidTable, BitTable, Order, CheckoutData
data = None


def registration_page(request):
    return redirect('/#registration')


def register(request):
    name = request.POST["name"]
    lname = request.POST["lname"]
    phone = request.POST["uphone"]
    try:
        UserRegister.objects.get(phone=phone)
        messages.error(request, "This phone no is already available !")
        return redirect('registration_page')
    except:
        email = request.POST["uemail"]
        try:
            UserRegister.objects.get(email=email)
            messages.error(request, "This email is already available !")
            return redirect('registration_page')
        except:
            username = request.POST["uname"]
            try:
                UserRegister.objects.get(username=username)
                messages.error(request, "This username is already available !")
                return redirect('registration_page')
            except:
                password1 = request.POST["upassword1"]
                password2 = request.POST["upassword2"]
                status = "pending"
                image = "user_profile/no_image.jpg"
                if password1 == password2:
                    UserRegister(name=name,lname=lname, phone=phone, email=email, username=username,
                                 status=status, password=password1, image=image).save()
                    return render(request, 'user/userlogin.html', {"msg": "Successfully registered."})
                else:
                    messages.error(request, "Password and confirm password must be same !")
                    return redirect('registration_page')


def user_login(request):
    if request.method == 'POST':
        uemail = request.POST.get("uemail")
        upassword = request.POST.get("upassword")
        try:
            data = UserRegister.objects.get(email=uemail, password=upassword)  # check email or password..
            try:
                UserRegister.objects.get(email=uemail, status="pending")  # check status pending..
                messages.error(request, "You'r still not approved by administration !")
                return render(request, "user/userlogin.html")
            except:
                try:
                    UserRegister.objects.get(email=uemail, status="declined")  # check status declined..
                    messages.error(request, "You'r Declined by administration !")
                    return render(request, "user/userlogin.html")
                except:
                    request.session["uemail"] = uemail     # successfully login..
                    return render(request, "user/user_welcome.html", {'data':data})
        except:
            messages.error(request, "You enter a wrong email or password !")
            return render(request, "user/userlogin.html")
    else:
        try:
            if request.session["uemail"]:
                uemail = request.session["uemail"]
                data = UserRegister.objects.get(email=uemail)
                return render(request, "user/user_welcome.html", {'data': data})
            else:
                return render(request, 'user/userlogin.html')
        except:
            return render(request, 'user/userlogin.html')


def user_logout(request):
    del request.session["uemail"]
    global data
    data = None
    return render(request, "admin/index.html")


def profile(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        return render(request, "user/user_welcome.html", {'data': data})
    return redirect('user_login')


def upload(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        if request.method == 'POST':
            image = request.FILES["a1"]
            id = data.id
            name = data.name
            lname = data.lname
            phone = data.phone
            email = data.email
            username = data.username
            password = data.password
            status = data.status
            doj = data.doj
            UserRegister(id=id, name=name,lname=lname, email=email, phone=phone, status=status, username=username,password=password,doj=doj,image=image).save()
            return redirect("profile")
        else:
            return render(request, "user/upload.html", {"data":data})
    else:
        return redirect('user_login')


def user_changepass(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        if request.method == 'POST':
            old = request.POST["old"]
            new1 = request.POST["new1"]
            new2 = request.POST["new2"]
            try:
                UserRegister.objects.get(id=data.id,password=old)
                if new1 == new2:
                    UserRegister.objects.filter(id=data.id).update(password=new1)
                    del request.session["uemail"]
                    data = None
                    return render(request, "user/userlogin.html", {"data":data, "msg":"Password changed successfully."})
                else:
                    return render(request, "user/user_change_pass.html",
                                  {"data":data, "msg2":"New password and Confirm password must be same !"})
            except:
                return render(request, "user/user_change_pass.html",
                              {"data": data, "msg1": "Old password not matched try again !"})
        else:
            return render(request, "user/user_change_pass.html",{"data":data})
    else:
        return redirect('user_login')


def seller(request):
    if request.session["uemail"]:
        return render(request, "user/seller.html")
    return redirect('user_login')


def add_product(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        if request.method == 'POST':
            pname = request.POST["pname"]
            ptitle = request.POST["ptitle"]
            pprice = request.POST["pprice"]
            pdesc = request.POST["pdesc"]
            image1 = request.FILES["image1"]
            image2 = request.FILES["image2"]
            image3 = request.FILES["image3"]
            Products(p_name=pname, title=ptitle, bid_price=pprice, disc=pdesc,
                     image1=image1, image2=image2, image3=image3, user_id=data.id, p_status="not_bid").save()
            messages.success(request, "Product added successfully.")
            return redirect('my_product')

        else:
            return render(request, "user/add_product.html")
    else:
        return redirect('user_login')


def my_product(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        qs = Products.objects.filter(user_id=data.id)
        if qs:
            return render(request, "user/my_product.html", {"mpro":qs , "data":data})
        else:
            messages.error(request, "No Product's.")
            return render(request, "user/my_product.html", {"data": data})
    else:
        return redirect('user_login')


def bid_product(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        qs = Products.objects.filter(user_id=data.id, p_status="bid")
        if qs:
            return render(request, "user/bid_products.html", {"bpro": qs, "data": data})
        else:
            messages.error(request, "No Bidding Product's.")
            return render(request, "user/bid_products.html", {"data": data})
    else:
        return redirect('user_login')


def not_bid_product(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        qs = Products.objects.filter(user_id=data.id, p_status="not_bid")
        if qs:
            return render(request, "user/not_bid_products.html", {"nbpro": qs, "data": data})
        else:
            messages.error(request, "No Product's.")
            return render(request, "user/not_bid_products.html", {"data": data})
    else:
        return redirect('user_login')


def sold_product(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        qs = Products.objects.filter(user_id=data.id, p_status="sold")
        if qs:
            return render(request, "user/sold_products.html", {"spro": qs, "data": data})
        else:
            messages.error(request, "No sold Product's.")
            return render(request, "user/sold_products.html", {"data": data})
    else:
        return redirect('user_login')


def bidding(request, pk):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        Products.objects.filter(p_id=pk).update(p_status="bid")
        pro = Products.objects.get(p_id=pk)
        MaxBidTable(product_id=pk, user_id=data.id, max_amount=pro.bid_price).save()
        return redirect('bid_product')
    else:
        return redirect('user_login')


def buyer(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        qs = MaxBidTable.objects.filter(~Q(user_id=data.id))
        if qs:
            return render(request, 'user/buyer.html', {"all":qs, "data":data})
        else:
            messages.error(request, "Not available bidding!")
            return render(request, 'user/buyer.html', {"data":data})
    else:
        return redirect('user_login')


def bidding_process(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        pid = request.POST["pid"]
        bprice = request.POST["bprice"]
        pro = MaxBidTable.objects.get(product_id=pid)
        if float(bprice) < pro.max_amount:
            messages.error(request, "Price must be greater than fixed price !")
            return redirect('buyer')
        else:
            BitTable(product_id=pid,user_id=data.id,amount=bprice).save()
            MaxBidTable.objects.filter(product_id=pid).update(max_amount=bprice)
            return redirect('buyer')
    else:
        return redirect('user_login')


def bidding_details(request, pk):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        b_detail = BitTable.objects.filter(product_id=pk)
        pro = Products.objects.get(p_id=pk)
        if b_detail:
            return render(request, "user/bidding_detail.html", {"data":data, "b_detail":b_detail, "pro":pro})
        else:
            return render(request, "user/bidding_detail.html", {"data": data, "pro": pro, "msg":"Bidding not done."})
    else:
        return redirect('user_login')


def update_pro(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        if request.method == 'POST':
            pid = request.POST["pid"]
            try:
                pro = Products.objects.get(p_id=int(pid), user_id=data.id)
                return render(request, "user/update_pro.html", {"data":data, "pro":pro})
            except:
                return render(request, "user/update_pro.html", {"data": data, "msg": "Product Id Number Not Matching."})
        else:
            return render(request, "user/update_pro.html", {"data": data})
    else:
        return redirect('user_login')


def update(request):
    if request.session["uemail"]:
        pid = request.POST["pid"]
        pname = request.POST["p_name"]
        ptitle = request.POST["title"]
        p_status = request.POST["p_status"]
        pprice = request.POST["p_price"]
        pdesc = request.POST["p_desc"]
        image1 = request.FILES["image1"]
        image2 = request.FILES["image2"]
        image3 = request.FILES["image3"]
        user_id = request.POST["user_id"]
        Products(p_id=pid, p_name=pname, title=ptitle, bid_price=pprice, disc=pdesc,
                 image1=image1, image2=image2, image3=image3, user_id=user_id, p_status=p_status).save()
        messages.success(request, "Product Updated successfully.")
        return redirect('my_product')
    else:
        return redirect('user_login')


def delete_pro(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        if request.method == 'POST':
            pid = request.POST["pid"]
            try:
                pro = Products.objects.get(p_id=int(pid),user_id=data.id)
                return render(request, "user/delete_pro.html", {"data":data, "pro":pro})
            except:
                return render(request, "user/delete_pro.html", {"data": data, "msg": "Product Id Number Not Matching."})
        else:
            return render(request, "user/delete_pro.html", {"data": data})
    else:
        return redirect('user_login')


def delete(request, pk):
    if request.session["uemail"]:
        Products.objects.get(p_id=pk).delete()
        return redirect('my_product')
    else:
        return redirect('user_login')


def my_cart(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        qs = Order.objects.filter(user_id=data.id)
        if qs:
            return render(request, "user/mycart.html", {"data": data, "order":qs})
        else:
            return render(request, "user/mycart.html", {"data": data, "msg": "Not available order."})
    else:
        return redirect('user_login')


def stop_bid(request, pk):
    if request.session["uemail"]:
        max = MaxBidTable.objects.get(product_id=pk)
        user = BitTable.objects.get(product_id=pk,amount=max.max_amount)
        Order(product_id=user.product_id,user_id=user.user_id,o_status="not_purchase",final_price=max.max_amount).save()
        Products.objects.filter(p_id=pk).update(p_status="sold")
        MaxBidTable.objects.get(product_id=pk).delete()
        return redirect('sold_product')
    else:
        return redirect('user_login')


def checkout_page(request, pk):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)
        qs = Order.objects.get(user_id=data.id, o_id=pk)
        return render(request, "user/checkout-page.html",{"data":data, "order":qs})
    else:
        return redirect('user_login')


def checkout(request):
    if request.session["uemail"]:
        uemail = request.session["uemail"]
        data = UserRegister.objects.get(email=uemail)

        o_id = request.POST["o_id"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        add = request.POST["add"]
        add2 = request.POST["add2"]
        country = request.POST["country"]
        state = request.POST["state"]
        zip = request.POST["zip"]
        balance = request.POST["balance"]
        card_name = request.POST["card_name"]
        card_number = request.POST["card_number"]
        card_exp = request.POST["card_exp"]
        card_cvv = request.POST["card_cvv"]
        balance = str(balance).split('.')

        d1 = {"card_no": int(card_number),
              "cvv": int(card_cvv),
              "exp_date": card_exp,
              "balance": int(balance[0])
              }
        json_data = json.dumps(d1)

        try:
            res = requests.post("http://192.168.0.171:5000/transaction/", data=json_data)
            if res.status_code == 200:
                msg = res.json()
                CheckoutData(fname=fname, lname=lname, email=email, contact=phone,
                             add=add, add2=add2, country=country, state=state, pin=zip, status="not_delivered").save()
                Order.objects.filter(o_id=o_id).update(o_status="purchased")
                return render(request, "user/done.html", {"data": data, "msg":msg})
            else:
                msg = res.json()
                return render(request, "user/done.html", {"data": data, "msg": msg})
        except requests.exceptions.ConnectionError:
            return render(request, "user/servernotavailable.html")
    else:
        return redirect('user_login')