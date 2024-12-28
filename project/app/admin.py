from django.contrib import admin
from . models import *




class YoutubeChannelAdmin(admin.ModelAdmin):
    # List display fields to show in the admin panel
    list_display = ('channel_name', 'user', 'statue', 'channel_url', 'channel_id', 'description')
    
    # Filter options for better browsing
    list_filter = ('statue', 'user')
    
    # Search functionality
    search_fields = ('channel_name', 'channel_id', 'description', 'user__username')  # Allows searching through channel_name, channel_id, and user
    
    # Fields for the form in the admin panel
    fieldsets = (
        (None, {
            'fields': ('user', 'channel_name', 'channel_url', 'channel_id', 'description', 'statue')
        }),
    )
    
    # Read-only fields if you don't want them to be editable in the admin interface (optional)
    readonly_fields = ('channel_id',)

# Registering the admin class for the YoutubeChannel model
admin.site.register(YoutubeChannel, YoutubeChannelAdmin)




class CustomerModelAdmin(admin.ModelAdmin):
    # List display fields to show in the admin panel
    list_display = ('firstname', 'lastname', 'email', 'phone', 'city', 'gender', 'terms_accepted', 'dob')
    
    # Filter options for better browsing
    list_filter = ('gender', 'terms_accepted', 'city', 'dob')
    
    # Search functionality
    search_fields = ('firstname', 'lastname', 'email', 'phone', 'city')
    
    # Fields for the form in the admin panel
    fieldsets = (
        (None, {
            'fields': ('firstname', 'lastname', 'email', 'gender', 'dob', 'age', 'phone', 'city', 'address', 'address2')
        }),
        ('Additional Info', {
            'fields': ('area_code', 'postal_code', 'signature', 'terms_accepted'),
            'classes': ('collapse',),  # To collapse the section in admin for a cleaner look
        }),
    )
    
    # Customizing formfield for some fields (e.g., age should not be manually entered if dob exists)
    def save_model(self, request, obj, form, change):
        if not obj.age and obj.dob:
            obj.age = self.calculate_age(obj.dob)
        super().save_model(request, obj, form, change)

    # Helper function to calculate age based on date of birth
    def calculate_age(self, dob):
        from datetime import date
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    # To make the gender field display more user-friendly in the admin panel
    def gender_display(self, obj):
        return dict(obj.GENDER_CHOICES).get(obj.gender, '-')
    
    gender_display.short_description = 'Gender'

# Registering the admin class for the Customer_model
admin.site.register(Customer_model, CustomerModelAdmin)



from django.contrib import admin
from .models import Withdraw, AddMoney

from django.contrib import admin
from .models import Withdraw, AddMoney

@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'status', 'created_at')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('user__username',)

    actions = ['approve_withdrawals']

    @admin.action(description="Approve selected withdrawals")
    def approve_withdrawals(self, request, queryset):
        for withdrawal in queryset.filter(status='Pending'):
            try:
                withdrawal.approve_withdrawal()
                self.message_user(request, f"Withdrawal for {withdrawal.user.username} approved successfully.")
            except ValueError as e:
                self.message_user(request, f"Error approving withdrawal for {withdrawal.user.username}: {str(e)}", level='error')



@admin.register(AddMoney)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['user' , 'earning' , 'payment']
    list_filter = ('earning', 'payment')
    # editable fields
    list_editable = ('earning',)
    

class SiteSettingsAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('logo', 'banner')
    
    # Fields to be displayed in the admin form
    fieldsets = (
        (None, {
            'fields': ('logo', 'banner')
        }),
    )
    
    # Optional: Add read-only fields if necessary
    readonly_fields = ('logo', 'banner')

# Register the model with the custom admin interface
admin.site.register(SiteSettings, SiteSettingsAdmin)



from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = "My Professional Admin"
    site_title = "Admin Portal"
    index_title = "Welcome to the Admin Dashboard"

admin_site = MyAdminSite()

