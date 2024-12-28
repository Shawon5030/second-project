from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NameForm(models.Model):
    name = models.CharField(max_length=100)
    
    
    def __str__(self):
        return str(self.name)
    
# this model is not use here
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    division = models.CharField( max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=50)
    villorroad = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    Mobile_number = models.IntegerField()
    image = models.ImageField( default='image.png',null=True , blank=True)
    
    
    
    def __str__(self):
        return str(self.name)
    
    


ch = (
    ('Pending','Pending'),
    ('approved','approved'),
    
)
#user for youtube channel informmationm
class YoutubeChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
    statue = models.CharField(max_length=255 ,default='Pending', choices=ch)
    channel_url = models.URLField()
    channel_id = models.CharField(max_length=255 , unique=True)
    description = models.TextField()

    def __str__(self):
        return self.channel_name




    
from django.conf import settings
class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logos/' , null=True , blank=True)
    banner = models.ImageField(upload_to='banner/' , null=True,blank=True)
    
   

    def __str__(self):
        return "Site Settings"

class EmailSettings(models.Model):
    host_user = models.EmailField()
    host_password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        settings.EMAIL_HOST_USER = self.host_user
        settings.EMAIL_HOST_PASSWORD = self.host_password
        super().save(*args, **kwargs)

    


class Customer_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True )
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    age = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=10, blank=True, null=True,choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')])
    email = models.EmailField()
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    area_code = models.CharField(max_length=10,blank=True, null=True)
    phone = models.CharField(max_length=15)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    terms_accepted = models.BooleanField(default=False ,  null=True, blank=True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
    
class AddMoney(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    earning = models.IntegerField(default=0)
    payment = models.IntegerField(default=0)

    def can_withdraw(self, amount):
        return self.earning >= amount

    def process_withdrawal(self, amount):
        """Process the withdrawal by deducting from earnings and adding to payments."""
        if not self.can_withdraw(amount):
            raise ValueError("Insufficient balance to process the withdrawal.")
        
        # Debugging
        print(f"Before: Earnings = {self.earning}, Payments = {self.payment}")
        
        self.earning -= amount
        self.payment += amount
        self.save()
        
        # Debugging
        print(f"After: Earnings = {self.earning}, Payments = {self.payment}")


    def __str__(self):
        return f"{self.user.username} - Earnings: {self.earning}, Payments: {self.payment}"


class Withdraw(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Bank', 'Bank Transfer'),
        ('Paypal', 'Paypal'),
        ('Bkash', 'Bkash'),
        ('Nagad', 'Nagad'),
        ('Crypto', 'Cryptocurrency'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    Account_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def approve_withdrawal(self):
        """Approve the withdrawal and update user earnings and payments."""
        if self.status != 'Pending':
            raise ValueError("Only pending withdrawals can be approved.")

        try:
            add_money = AddMoney.objects.get(user=self.user)
            if add_money.can_withdraw(self.amount):
                add_money.process_withdrawal(self.amount)
                self.status = 'Approved'
                self.save()
                print(f"Withdrawal approved: {self.user.username}, Amount: {self.amount}")
            else:
                raise ValueError(f"Insufficient balance for {self.user.username}: {add_money.earning}")
        except Exception as e:
            print(f"Error in approving withdrawal: {str(e)}")
            raise


    def __str__(self):
            return f"{self.user.username} - {self.amount} ({self.method}) - {self.status}"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Withdraw)
def handle_withdrawal_approval(sender, instance, **kwargs):
    if instance.status == 'Approved':
        try:
            add_money = AddMoney.objects.get(user=instance.user)
            add_money.process_withdrawal(instance.amount)
        except ValueError as e:
            print(f"Error in signal: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


