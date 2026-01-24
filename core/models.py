from django.contrib.auth.models import AbstractUser,Group, Permission, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Role Model
class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name

class AdminRole(models.Model):
    admin_role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.admin_role_name

# Custom Manager untuk Admin
class AdminManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        if 'admin_role' not in extra_fields:
            #jika tidak ada titipan role, set otomatis jadi Super Admin
            # Dapatkan atau buat role Super Admin
            admin_role, created = AdminRole.objects.get_or_create(
                admin_role_name='Super Administrator'
            )
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('admin_role', admin_role)  # Set role secara otomatis
        
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        
        return self.create_user(username, email, password, **extra_fields)

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

class Admin(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=255)
    admin_role = models.ForeignKey(
        AdminRole,
        on_delete=models.CASCADE,
        related_name='admins',
        verbose_name=_('admin role')
    )
    is_staff = models.BooleanField(_('staff status'), default=True)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = AdminManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name'] #menambahkan name sebagai required field

    class Meta:
        verbose_name = _('admin')
        verbose_name_plural = _('admins')

    def __str__(self):
        return self.username

# Custom Manager untuk User
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    mobile_phone = models.CharField(_('mobile phone'), max_length=15)
    name = models.CharField(_('full name'), max_length=255)
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name=_('role')
    )
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username


# Transaction Rules
class TransactionRule(models.Model):
    rules_name = models.CharField(max_length=100)

    def __str__(self):
        return self.rules_name

# User Transaction Rules
class UserTransactionRule(models.Model):
    id_transaction_rules = models.ForeignKey(TransactionRule, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

# Passanger Model
class Passenger(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    ID_type = models.CharField(max_length=50)
    ID_number = models.CharField(max_length=50)
    ID_expired_date = models.DateField()
    ID_issued_country = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=15)
    DOB = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])

# Booking Model
class Booking(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_number = models.CharField(max_length=20, unique=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    type_booking = models.CharField(max_length=50)

# Payment Model
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

# Supplier Model
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    supplier_email = models.EmailField()
    supplier_phone_number = models.CharField(max_length=15)
    supplier_address = models.TextField()
    supplier_services = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.supplier_name

# Flight Model
class Flight(models.Model):
    id_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    airline_name = models.CharField(max_length=100)
    flight_departure_time = models.DateTimeField()
    flight_arrival_time = models.DateTimeField()
    flight_price = models.DecimalField(max_digits=10, decimal_places=2)
    flight_departure_city = models.CharField(max_length=100)
    flight_arrival_city = models.CharField(max_length=100)

# Hotel Model
class Hotel(models.Model):
    id_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100)
    hotel_address = models.TextField()
    hotel_price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField()

# Profit Model
class Profit(models.Model):
    profit_name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)

# Supplier Profit Model
class SupplierProfit(models.Model):
    id_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    id_profit = models.ForeignKey(Profit, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
