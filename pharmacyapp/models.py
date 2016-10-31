from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import *

Tax= ((0,0),(4,4),(5,5),(12,12))

class Post(models.Model):
    pharmacy_user = models.ForeignKey('auth.User')
    medicineName = models.CharField("Medicine Name",max_length=48,blank=False)
    batchNo = models.CharField("Enter the Batch Number",max_length=50, blank=False)
    expiryDate = models.DateField("Expiry Date")
    pack = models.PositiveSmallIntegerField("No. of Tablets per Strip/Bottles",default ='1')
    freeArticles = models.PositiveSmallIntegerField("Free Strips",default ='0')
    quantity = models.PositiveSmallIntegerField("Enter the number of strips Purchased")
    pricePerStrip = models.DecimalField(max_digits=8, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    netPurchasePrice = models.DecimalField(max_digits=8, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    mrp = models.DecimalField(max_digits=8, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    dateOfPurchase = models.DateField("Date Of Purchase",default=timezone.now)
    vat1 = models.PositiveSmallIntegerField("Vat (%)",choices=Tax,default ='4')
    vat2 = models.PositiveSmallIntegerField("Additional Vat (%)",choices=Tax,default ='0')
    addTax = models.PositiveSmallIntegerField("Additional Taxes (%)",default ='0')
    noOfTablets = models.PositiveSmallIntegerField(default ='0')
    pricePerTablet = models.DecimalField(max_digits=8, decimal_places=2,default ='0.01',validators=[MinValueValidator(Decimal('0.01'))])
    noOfTabletsSold = models.PositiveSmallIntegerField(default ='0')
    noOfTabletsInStores = models.PositiveSmallIntegerField(default ='0')
    
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.medicineName


class PatientDetail(models.Model):
    patientID = models.CharField("Patient ID",max_length=50, blank=True)
    patientName = models.CharField("Name",max_length=50, blank=True)
    patientPhoneNo = models.PositiveSmallIntegerField("Phone Number", blank=True, default = '0')

    def publish(self):
        self.save()
        
    def __str__(self):
        return self.patientID

Discount= ((0,0),(5,5),(10,10))
class Bill(models.Model):
    patientID = models.ForeignKey(PatientDetail)
    medicineName = models.CharField(max_length=50, blank=True, default='NA')
    billNo = models.CharField(max_length=50)
    billDate = models.DateField("Date Of Purchase",default=timezone.now)
    noOfTabletsOrdered = models.PositiveSmallIntegerField(default ='0')
    pricePerTablet = models.DecimalField(max_digits=8, decimal_places=2,default ='0',validators=[MinValueValidator(Decimal('0.01'))])
    totalPrice = models.DecimalField(max_digits=12, decimal_places=2,default ='0',validators=[MinValueValidator(Decimal('0.01'))])
    discount = models.PositiveSmallIntegerField("Discount (%)",choices=Discount,default ='0')
    discountedPrice = models.DecimalField(max_digits=12, decimal_places=2,default ='0',validators=[MinValueValidator(Decimal('0.01'))])
    transactionCompleted = models.CharField(max_length=1,default='N')
    batchNo = models.CharField(max_length=50, default='NA')
    expiryDate = models.DateField("Expiry Date")
    returnSales = models.CharField(max_length=2, default='N')
    returnSalesNoOfTablets = models.PositiveSmallIntegerField(default ='0')
    returnSalesBillDate = models.DateField("Date Of Return",default=timezone.now)
    returnDiscountedPrice=models.DecimalField(max_digits=12, decimal_places=2,default ='0',validators=[MinValueValidator(Decimal('0.01'))])
    

    def __str__(self):
        return self.billNo

class returnBill(models.Model):
    originalBillNo = models.ForeignKey(Bill)
    originalPricePerTablet = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    originalDiscount = models.PositiveSmallIntegerField("Discount (%)")
    returnSalesBillNo = models.CharField(max_length=50)
    returnSalesMedicineName = models.CharField(max_length=50, blank=True, default='NA')
    returnSalesBatchNo = models.CharField(max_length=50, default='NA')
    returnSalesBillDate = models.DateField("Date Of Return",default=timezone.now)
    returnSalesNoOfTablets = models.PositiveSmallIntegerField(default ='0')
    returnSalesDiscountedPricePerTablet = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    totalReturnAmount = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    def __str__(self):
        return self.returnSalesBillNo
    
    