from django.shortcuts import render, redirect
from django.contrib import messages
from customer.models import Customer
from django.contrib.auth import get_user_model
from .bkash_utils import create_payment, create_token, exec_payment
from .models import CustomerPayment
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def check_customer(number):
    customer = Customer.objects.filter(phone_number=number).exists()
    if customer:
        return Customer.objects.filter(phone_number=number)


def customer_payment(request):
    if request.method == "POST":
        customer_bkash_number = request.POST.get("bnumber")
        customer = check_customer(customer_bkash_number)

        if customer is not None:
            admin_bkash_number = customer.get().admin.bkash_number
            pay_amount = customer.get().package.price
            try:
                get_token = create_token(
                    bk_secret=customer.get().admin.bkash_secret_key,
                    bk_username=customer.get().admin.bkash_username,
                    bk_app=customer.get().admin.bkash_app_key,
                    bk_password=customer.get().admin.bkash_password,
                )
                token = get_token["id_token"]
                payment = create_payment(
                    token=str(token),
                    amount=pay_amount,
                    payer_reference=str(customer_bkash_number),
                    minumber=str(admin_bkash_number),callback="http://127.0.0.1:8000/pay/customer"
                )
                if payment["agreementStatus"] == "Initiated":
                    return redirect(payment["bkashURL"])
            except Exception as e:
                messages.error(
                    request,
                    "There is a problem with the payment gateway. Please try again later",
                )
                return redirect("pay:bill")
        messages.success(request, "Your payment was successfull")
        return redirect("pay:bill")
    return render(request, "payment/customer.html")



@csrf_exempt
def customer_payment_execution(request):
    if request.method == "GET":
        status = request.GET['status']
        if status == 'cancel':
            messages.error(request,"Payment Canceled")
            return redirect("pay:bill")
        if status == 'failed':
            messages.error(request,"Payment Failed")
            return redirect("pay:bill")
        
    data = request.POST
    payment_id = data.get('paymentID')
    admin_phone_number = data.get('merchantInvoiceNumber')
    admin = User.objects.get(bkash_number=admin_phone_number)
    try:
        get_token = create_token(bk_secret=admin.bkash_secret_key,
                    bk_username=admin.bkash_username,
                    bk_app=admin.bkash_app_key,
                    bk_password=admin.bkash_password)
        token = get_token["id_token"]
        exe_payment = exec_payment(token,paymentId=payment_id)
        date_string=exe_payment["agreementExecuteTime"]
        date_string = date_string.replace(" GMT", "")
        customer_phone_number = exe_payment["customerMsisdn"]
        customer = Customer.objects.get(phone_number=customer_phone_number)
        admin = customer.get().admin
        if exe_payment.get('agreementStatus') == 'Completed' :
            save_payment = CustomerPayment.objects.create(customer=customer,admin=admin,payment_id=payment_id,trxID=exe_payment['trxID'],payment_exec_time=date_string,amount=exe_payment["amount"],payment_type="Bkash")
            messages.success(request,"Payment Successful")
            return redirect("pay:bill")
    except Exception as e:
        messages.error(request,"There is a problem with the payment gateway. Please try again later")
        return redirect("pay:bill")
        
