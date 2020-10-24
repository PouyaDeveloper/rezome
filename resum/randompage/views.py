from django.shortcuts import render, redirect
from .forms import BookForm
from django.shortcuts import get_object_or_404
from .models import AddToDatabase
from zarinpal.models import Vocher
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/')
def upload(request):
    if request.method == 'POST':
        code= request.POST['secure']
        if Vocher.objects.filter(unique_id = code).exists():
            Vocher.objects.filter(unique_id = code).delete()
            form = BookForm(request.POST,request.FILES)
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.save()
                return redirect("form_detail", random_url=form_instance.random_url)
        else:
            statement='لطفا کد ووچر معتبر وارد کنید'
            form = BookForm()
            return render(request,'randompage/upload_cv.html',{
                'statement':statement, 'form': form
            })
        
    
    else:
        
        hit = request.session.get('hit')
        if not hit:
            request.session['hit'] = 1
            form = BookForm()
            return render(request,'randompage/upload_cv.html',{
                'form': form
                })
        else: 
            request.session['hit'] += 1
            print(request.session['hit'])
            return render(request,'portal/user.html')


def form_detail(request, random_url):
    
    context = {}
    form_detail = get_object_or_404(AddToDatabase, random_url=random_url)
    context["form_detail"] = form_detail
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        email=form_detail.email_name
        send_mail(
            'Viewed',
            f"congratulations! your page has been viewed by this ip address: {ip}",
            'pooya_cim@outlook.com',
            [f"{email}"],
            fail_silently=False
        )
    
    else:
        ip = request.META.get('REMOTE_ADDR')
        
        email=form_detail.email_name
        send_mail(
            'Viewed',
            f"congratulations! your page has been viewed by this ip address: {ip}",
            'pooya_cim@outlook.com',
            [f"{email}"],
            fail_silently=False
        )
        
    return render(request, 'randompage/form_detail.html',context)