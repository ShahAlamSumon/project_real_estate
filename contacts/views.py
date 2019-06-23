from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check user has made query already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have already made an inquiry for this')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing_id=listing_id,listing=listing,name=name,email=email,
                          phone=phone,message=message,user_id=user_id)
        contact.save()
        # Send mail
        # send_mail(
        #     'Proper listing inquiry',
        #     'There has been inquiry for '+ listing +'.Sign in for more.',
        #     'sacsesumon@gmail.com',
        #     [realtor_email, 'sacsesumon@gmail.com'],
        #     fail_silently=False
        # )
        messages.success(request,'Your query has been submitted,a realtor will contact you soon')
        return redirect('/listings/'+listing_id)