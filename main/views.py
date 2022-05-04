from django.shortcuts import render
from django.views.generic import ListView
from .models import *
from django.shortcuts import render, redirect
from .models import Course, Video, Payment, UserCourse
from django.shortcuts import HttpResponse
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from time import time
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import *


import razorpay
client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))

class HomePageView(ListView):
    template_name = "home.html"
    queryset = Course.objects.filter(active=True)
    context_object_name = 'courses'


@login_required(login_url='/login')
def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    user = request.user
    action = request.GET.get('action')
    couponcode = request.GET.get('couponcode')
    coupon_code_message = None
    coupon = None
    order = None
    payment = None
    error = None
    try:
        user_course = UserCourse.objects.get(user=user, course=course)
        error = "You are Already Enrolled in this Course"
    except:
        pass
    amount = None
    if error is None:
        amount = int(
            (course.price - (course.price * course.discount * 0.01)) * 100)
   # if ammount is zero dont create paymenty , only save emrollment obbect
    if couponcode:
        try:
            coupon = CouponCode.objects.get(course=course, code=couponcode)
            amount = course.price - (course.price * coupon.discount * 0.01)
            amount = int(amount) * 100
        except Exception as e:
            coupon_code_message = "Invaild Coupon Code"
            messages.error(request, 'Coupon Code Invalid')
    
    if amount == 0:
        userCourse = UserCourse(user=user, course=course)
        userCourse.save()
        return redirect('my-courses')
        # enroll direct
    if action == 'create_payment':

        currency = "INR"
        notes = {
            "email": user.email,
            "name": f'{user.first_name} {user.last_name}'
        }
        reciept = f"codewithvirendra-{int(time())}"
        order = client.order.create(
            {'receipt': reciept,
             'notes': notes,
             'amount': amount,
             'currency': currency
             }
        )

        payment = Payment()
        payment.user = user
        payment.course = course
        payment.order_id = order.get('id')
        payment.save()


            
    
    context = {
        "course": course,
        "order": order,
        "payment": payment,
        "user": user,
        "error": error,
        "coupon": coupon,
        "coupon_code_message": coupon_code_message,
        
    }
    return render(request, template_name="check_out.html", context=context)


@login_required(login_url='/login')
@csrf_exempt
def verifyPayment(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            userCourse = UserCourse(user=payment.user, course=payment.course)
            userCourse.save()

            print("UserCourse",  userCourse.id)

            payment.user_course = userCourse
            payment.save()

            return redirect('my-courses')

        except:
            return HttpResponse("Invalid Payment Details")


@method_decorator(login_required(login_url='login'), name='dispatch')
class MyCoursesList(ListView):
    template_name = 'my_courses.html'
    context_object_name = 'user_courses'

    def get_queryset(self):
        return UserCourse.objects.filter(user=self.request.user)


def coursePage(request,id, slug):
    rvs = Review.objects.filter(course_id=id)
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")

    if serial_number is None:
        serial_number = 1

    video = Video.objects.get(serial_number=serial_number, course=course)

    if (video.is_preview is False):

        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            user = request.user
            try:
                user_course = UserCourse.objects.get(user=user, course=course)
            except:
                return redirect("check-out", slug=course.slug)

    context = {
        "course": course,
        "video": video,
        'videos': videos,
        'rvs':rvs
    }
    return render(request, template_name="course_page.html", context=context)



def submit_review(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        text = request.POST.get('text')
        rate = request.POST.get('rate')
        data = Review()
        data.text = text
        data.rate = rate
        data.course_id = id
        current_user = request.user
        data.user_id = current_user.id
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        messages.success(
            request, "Your review has been update. Thank you for your interest.")
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)
