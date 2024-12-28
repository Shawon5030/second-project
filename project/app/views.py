from django.shortcuts import render 
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import *
from .form import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.

from django.shortcuts import render

def home(request):
    settings = SiteSettings.objects.first()
    money = None
    if request.user.is_authenticated:
        try:
            money = AddMoney.objects.get(user=request.user)
        except AddMoney.DoesNotExist:
            money = None
    
    return render(request, 'home.html', {'settings':settings,'money': money})

    





@login_required
def Cform(request):
    if request.method == 'POST':
             Channel_Name = request.POST["ChannelName"]
             Channel_Url = request.POST["ChannelUrl"]
             Channel_Id = request.POST["ChannelId"]
             Channel_Description = request.POST["message"]
             print(Channel_Name)
          
             f = YoutubeChannel(
                   channel_name=Channel_Name,
                   channel_url=Channel_Url,
                   channel_id=Channel_Id,
                   description=Channel_Description,
                   statue = "Pending",
                   user = request.user
               )
             f.save()
             messages.success(request,'Congratulations Submit done.')
             
             # Replace 'success_url' with the actual URL or name of the success page
           
    
      
    return render(request, 'form.html')

    
@login_required
def formsee(request):
    form = YoutubeChannel.objects.filter(user=request.user)
    return render(request,'yourForm.html',{'form':form})


class CustomerRegistrationView(View):
  def get(self,request):
     form = CustomerRegistrationForm()
     return render(request, 'customerregistration.html', {'form':form})
  
  def post(self,request):
     form = CustomerRegistrationForm(request.POST)
     if form.is_valid():
        messages.success(request,'Congratulations registration done.')
        form.save()
     return render(request, 'customerregistration.html', {'form':form})


def user_form_view(request):
    if request.method == "POST":
        # Extract form data from POST request
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        post_code = request.POST.get('post')
        city = request.POST.get('city')
        image = request.FILES['upload']  # Correct way to get the uploaded image
        agree_terms = request.POST.get('supportCheckbox') == 'on'

        # Basic validation
        if not image:
            messages.error(request, "image not found")
            return render(request, 'profile.html')

        try:
            # Save to the database
            form_entry = Customer_model(
                user=request.user,
                firstname=first_name,
                lastname=last_name,
                age=age,
                dob=dob,
                email=email,
                address=address,
                phone=phone,
                postal_code=post_code,
                city=city,
                terms_accepted=agree_terms,
                signature=image,
            )
            form_entry.save()

            messages.success(request, "Form submitted successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred while saving the data: {e}")
            return render(request, 'profile.html')

    return render(request, 'profile.html')




@login_required 
def show_customer_data(request):
    customer_data = Customer_model.objects.filter(user=request.user).first()
    return render(request, 'show_customer_data.html', {'customer': customer_data})






@login_required
def withdraw_request(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            add_money = AddMoney.objects.get(user=request.user)
            
            if add_money.can_withdraw(withdrawal.amount):
                withdrawal.save()
                messages.success(request, "Your withdrawal request has been submitted.")
            else:
                messages.error(request, "Insufficient balance for withdrawal.")
              # Replace with the appropriate URL
    else:
        form = WithdrawForm()
    return render(request, 'withdraw.html', {'form': form})





@login_required
def withdrawal_history(request):
    # Get the current user's withdrawal history
    withdrawals = Withdraw.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == "POST":
        # Optionally, handle actions like downloading the invoice here
        withdrawal_id = request.POST.get('withdrawal_id')
        withdrawal = get_object_or_404(Withdraw, id=withdrawal_id)

        if withdrawal.status == 'Approved':
            # Generate the invoice for the approved withdrawal
            invoice_html = render_to_string('invoice_template.html', {'withdrawal': withdrawal})
            response = HttpResponse(invoice_html, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="invoice_{withdrawal.id}.pdf"'
            return response

    context = {
        'withdrawals': withdrawals
    }
    return render(request, 'withdrawal_history.html', context)


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Withdraw

def generate_invoice(request, withdrawal_id):
    # Retrieve the withdrawal object
    withdrawal = get_object_or_404(Withdraw, id=withdrawal_id)

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{withdrawal.id}.pdf"'

    # Create the PDF content
    c = canvas.Canvas(response, pagesize=letter)
    c.setFont("Helvetica", 10)

    # Header Section: Add a title and company logo (optional)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, f"Invoice #{withdrawal.id}")
    
    c.setFont("Helvetica", 10)
    c.drawString(100, 735, f"User: {withdrawal.user.username}")
    c.drawString(100, 720, f"Amount: ${withdrawal.amount:.2f}")
    c.drawString(100, 705, f"Payment Method: {withdrawal.get_method_display()}")
    c.drawString(100, 690, f"Status: {withdrawal.get_status_display()}")
    c.drawString(100, 675, f"Date: {withdrawal.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Draw a line below the header
    c.setStrokeColor(colors.grey)
    c.setLineWidth(0.5)
    c.line(50, 665, 550, 665)

    # Itemized Breakdown (if needed): Add a more detailed description of the withdrawal
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 630, "Transaction Details")
    
    c.setFont("Helvetica", 10)
    c.drawString(100, 615, f"Amount Withdrawn: ${withdrawal.amount:.2f}")
    c.drawString(100, 600, f"Payment Method: {withdrawal.get_method_display()}")
    c.drawString(100, 585, f"Account Number: {withdrawal.Account_number if withdrawal.Account_number else 'N/A'}")
    
    # Draw a line below the transaction details
    c.line(50, 575, 550, 575)

    # Footer: Include additional information or contact details
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 550, "Thank you for using our platform!")
    c.drawString(100, 535, "For any queries, please contact support@example.com.")
    
    # Add a border around the invoice (optional)
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(50, 50, 500, 750, stroke=1, fill=0)  # Add rectangle border

    c.showPage()
    c.save()

    return response
