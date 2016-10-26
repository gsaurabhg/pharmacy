from django import forms
from .models import Post
from .models import Bill
from .models import PatientDetail, returnBill

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['pharmacy_user','freeArticles','netPurchasePrice','noOfTablets','pricePerTablet','noOfTabletsSold','noOfTabletsInStores','expiryDate']
        widgets = {
                'quantity' : forms.TextInput(    attrs   =  {'placeholder':'Enter the number of strips'}),
                'mrp' : forms.TextInput(    attrs   =  {'placeholder':'Maximum Retail Price per strip'}),
        		'expiryDate' : forms.TextInput(    attrs   =  {'placeholder':'YYYY-MM-DD'})
        }
        

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('patientID','medicineName','noOfTabletsOrdered')

class CombinedForm(forms.ModelForm):
    Patient_Name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    Patient_Id= forms.CharField(max_length=128, help_text="To be passed from the form")
    Patient_PhoneNo= forms.CharField(max_length=128, help_text="Please enter the category name.")
    Medicine_Name = forms.ChoiceField(label="Medicine Name",initial='',widget=forms.Select(),required=True)
    class Meta:
        model = Bill
        fields = ('patientID','medicineName','noOfTabletsOrdered')



class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientDetail
        fields = ('patientID','patientName', 'patientPhoneNo')


Discount= ((0,0),(5,5),(10,10))
class availableMedsForm(forms.Form):
    def __init__(self, medicineNameChoices,*args, **kwargs):
        super(availableMedsForm, self).__init__(*args, **kwargs)
        self.fields['medicineName'].choices = medicineNameChoices
    medicineName = forms.ChoiceField(label='Medicine Name',choices=(), required=True)
    orderQuantity = forms.DecimalField(label='Enter the quantity', required=False)
    batchNo = forms.CharField(label='Batch Number:',max_length=128,required=True)
    discount = forms.ChoiceField(label='Discount:',choices=Discount, required=True)
    
    

class reportForm(forms.Form):
    startDate = forms.CharField(max_length=128, help_text="Please pick a date.")
    endDate = forms.CharField(max_length=128, help_text="Please pick a date.")

class medsAdjustForm(forms.ModelForm):
    class Meta:
        model = Bill
        exclude = ['returnSales','returnSalesBillDate']
        widgets = {
                'returnSalesNoOfTablets' : forms.TextInput(    attrs   =  {'placeholder':'Enter the number of tablets to be returned'}),
        }
        
