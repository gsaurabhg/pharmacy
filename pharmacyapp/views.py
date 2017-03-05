from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, PatientDetail, Bill, returnBill
from .forms import PostForm, PatientForm, BillForm, CombinedForm, availableMedsForm, reportForm, medsAdjustForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
#Below import is needed for making OR based query
from django.db.models import Q
#Below import is needed for creating the pop ups
from django.contrib import messages
from pharmacyapp.bing_search import run_query
from decimal import *
from datetime import datetime, date, timedelta, time
from django.core import validators
import datetime, time, json
from django.core import serializers
from django.http import HttpResponse

def welcome(request):
    return render(request, 'pharmacyapp/popup.html')

def post_list(request):
    posts = Post.objects.filter(dateOfPurchase__lte=timezone.now()).order_by('expiryDate')
    return render(request, 'pharmacyapp/post_list.html', {'posts':posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pharmacyapp/post_detail.html', {'post': post})

@login_required    
def post_new(request):
    current_user = request.user.username
    currentDate = datetime.datetime.strptime(str(format(timezone.now(), '%d-%m-%Y')),"%d-%m-%Y") 
    if (current_user == "admin" or current_user == "saurabhg"):
        if (request.method == "POST" and request.POST.get('save')):
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                enteredDate = datetime.datetime.strptime(str(format(post.dateOfPurchase, '%d-%m-%Y')),"%d-%m-%Y") 
                if ( enteredDate > currentDate):
                    messages.info(request,"Purchase Date " + format(post.dateOfPurchase, '%d-%m-%Y') + " can not be greater than Todays date i.e., " + format(timezone.now(), '%d-%m-%Y'))
                    return render(request, 'pharmacyapp/post_edit.html', {'form': form})
                if post.pack == 0:
                    messages.info(request,"Number of Tablets/Bottles to be greater than 0")
                    return render(request, 'pharmacyapp/post_edit.html', {'form': form})
                try:
                    medicineRecord = Post.objects.all().filter(medicineName__exact=post.medicineName,batchNo__exact = post.batchNo).get()
                    medicineRecord.quantity = post.quantity+medicineRecord.quantity
                    medicineRecord.freeArticles = int(post.freeArticles)+medicineRecord.freeArticles
                    medicineRecord.noOfTablets = (medicineRecord.quantity+medicineRecord.freeArticles)*medicineRecord.pack
                    medicineRecord.noOfTabletsInStores = medicineRecord.noOfTablets - medicineRecord.noOfTabletsSold
                    medicineRecord.netPurchasePrice = medicineRecord.quantity*medicineRecord.pricePerStrip*(1+Decimal(medicineRecord.vat+medicineRecord.sat+medicineRecord.addTax)/100)
                    medicineRecord.save()
                    return redirect('post_list')
                except ObjectDoesNotExist:
                    currentDate = datetime.datetime.strptime(str(format(timezone.now(), '%d-%m-%Y')),"%d-%m-%Y") 
                    webFormFields = request.POST
                    try:
                            datetime.datetime.strptime(webFormFields['expiryDateForm'], '%d-%m-%Y')
                    except ValueError:
                            messages.info(request,"Expiry Date to be in DD-MM-YYY format")
                            return render(request, 'pharmacyapp/post_edit.html', {'form': form})
                    post.expiryDate = datetime.datetime.strptime(webFormFields['expiryDateForm'],'%d-%m-%Y')
                    enteredDate = post.expiryDate
                    if enteredDate < currentDate:
                        messages.info(request,"enter the proper expiry Date")
                        return render(request, 'pharmacyapp/post_edit.html', {'form': form})
                    post.pharmacy_user = request.user
                    post.noOfTablets = (int(post.quantity)+int(post.freeArticles))*int(post.pack)
                    post.pricePerTablet = post.mrp/post.pack
                    post.noOfTabletsInStores = int(post.noOfTablets) - int(post.noOfTabletsSold)
                    post.netPurchasePrice = Decimal(post.quantity)*post.pricePerStrip*Decimal((100+post.vat+post.sat+post.addTax)/100)
                    post.save()
                    return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'pharmacyapp/post_edit.html', {'form': form})
    else:
        messages.info(request,"You have to LOG in as ADMIN to use this feature")
        posts = Post.objects.filter(dateOfPurchase__lte=timezone.now()).order_by('expiryDate')
        return render(request, 'pharmacyapp/post_list.html', {'posts':posts})
        

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            if post.pack == 0:
                messages.info(request,"Number of Tablets/Bottles to be greater than 0")
                return render(request, 'pharmacyapp/post_edit.html', {'form': form})
            currentDate = datetime.datetime.strptime(str(format(timezone.now(), '%d-%m-%Y')),"%d-%m-%Y") 
            enteredDate = datetime.datetime.strptime(str(format(post.dateOfPurchase, '%d-%m-%Y')),"%d-%m-%Y") 
            if ( enteredDate > currentDate):
                messages.info(request,"Purchase Date " + format(post.dateOfPurchase, '%d-%m-%Y') + " can not be greater than Todays date i.e., " + format(timezone.now(), '%d-%m-%Y'))
                return render(request, 'pharmacyapp/post_edit.html', {'form': form})
            post.pharmacy_user = request.user
            post.noOfTablets = (post.quantity+post.freeArticles)*post.pack
            post.pricePerTablet = post.mrp/post.pack
            post.noOfTabletsInStores = post.noOfTablets - post.noOfTabletsSold
            post.netPurchasePrice = post.quantity*post.pricePerStrip*(1+Decimal(post.vat+post.sat+post.addTax)/100)
            webFormFields = request.POST
            try:
                datetime.datetime.strptime(webFormFields['expiryDateForm'], '%d-%m-%Y')
            except ValueError:
                messages.info(request,"Expiry Date to be in DD-MM-YYY format")
                return render(request, 'pharmacyapp/post_edit.html', {'form': form})
                
            post.expiryDate = datetime.datetime.strptime(webFormFields['expiryDateForm'],'%d-%m-%Y')
            enteredDate = post.expiryDate
            if enteredDate < currentDate:
                messages.info(request,"enter the proper expiry Date")
                return render(request, 'pharmacyapp/post_edit.html', {'form': form})
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'pharmacyapp/post_edit.html', {'form': form})
    

@login_required    
def patient_details(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        patientNameToSearch = request.POST.get('patientName')
        patientIDToSearch = request.POST.get('patientID')
        patientPhoneNoToSearch = request.POST.get('patientPhoneNo')
        
        if request.POST.get('search'):
            if patientNameToSearch != "":
                patientRecord= PatientDetail.objects.filter(patientName__contains=patientNameToSearch)
            elif patientIDToSearch != "":
                patientRecord= PatientDetail.objects.filter(patientID__exact=patientIDToSearch)
            elif patientPhoneNoToSearch !="":
                patientRecord= PatientDetail.objects.filter(patientPhoneNo__exact=patientPhoneNoToSearch)
            else:
                messages.info(request, "Enter one of the fields")
                return redirect('patient_details')
            return render(request, 'pharmacyapp/possibilites.html', {'patientRecord': patientRecord})  
            #####MAKE THE BILL FORM IN 2 FRAMES
        elif request.POST.get('newReg'):
            existingRecordFound = PatientDetail.objects.filter(patientName__contains=patientNameToSearch,patientPhoneNo__exact = patientPhoneNoToSearch)
            if existingRecordFound:
                messages.info(request, "Patient Details already exists! Click Search Button")
                return render(request, 'pharmacyapp/patient_details.html', {'form': form})
            patientDetail = form.save(commit=False)
            patientDetail.patientID = 'AMC00'+str(PatientDetail.objects.count())
            patientDetail.save()
            return redirect('bill_details', pk=patientDetail.pk)
            #####MAKE THE BILL FORM IN 2 FRAMES
        elif request.POST.get('billSearch'):
            webFormFields = request.POST
            billDet = Bill.objects.filter(billNo__exact=webFormFields['billNo'])
            if len(billDet) == 0:
                messages.info(request,"Please Check the Bill Number")
            else:
                return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
    else:
        form = PatientForm()
    return render(request, 'pharmacyapp/patient_details.html', {'form': form})

@login_required    
def bill_details(request, pk):
    record = get_object_or_404(PatientDetail, pk=pk)
    billGeneration = Bill.objects.all().filter(patientID__patientID__exact = record.patientID,transactionCompleted__exact = 'N')
    if len(billGeneration) == 0:
        messages.info(request, "Pls check !! Nothing in Cart")            
        return render(request, 'pharmacyapp/bill_details.html', {'record': record})
    else:
        return render(request, 'pharmacyapp/sideNavigation.html',{'billGeneration': billGeneration})

    

@login_required    
def medicine_order(request, pk):
    patientDetails = get_object_or_404(PatientDetail, pk=pk)
    availableMeds = Post.objects.filter(noOfTabletsInStores__gt = 0).values()
    medicineNameChoices = []
    for med in availableMeds:
        medicineNameChoices.append((med['medicineName'], med['medicineName']),)
    form = availableMedsForm(medicineNameChoices)
    if (request.method == "POST" and request.POST.get('addMed')):
        webFormFields = request.POST
        if (webFormFields['medicineName'] == '' or webFormFields['orderQuantity'] == '' or webFormFields['batchNo'] == ''):
            messages.info(request,"Please fill all the fields")
            return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
        if (int(webFormFields['orderQuantity']) <= 0):
            messages.info(request,"Please fill proper quantity of medicines ")
            return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
        if  Post.objects.all().filter(medicineName__exact = webFormFields['medicineName'], batchNo__exact = webFormFields['batchNo']):
            medDetails = Post.objects.all().filter(medicineName__exact = webFormFields['medicineName'], batchNo__exact = webFormFields['batchNo']).get()
            if format(medDetails.expiryDate,'%Y-%m-%d') < format(timezone.now(),'%Y-%m-%d'):
                messages.info(request,"Can Not Sale " + medDetails.medicineName + " medicine as its Expired on "+ format(medDetails.expiryDate,'%Y-%m-%d'))
                return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
            if Decimal(webFormFields['orderQuantity']) > medDetails.noOfTabletsInStores:
                messages.info(request,"Quantity of " +webFormFields['medicineName']+ " has to be less than " + str(medDetails.noOfTabletsInStores) + " instead of " + webFormFields['orderQuantity'])
                return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
            try:
                billDetails = Bill.objects.all().filter(medicineName__exact = webFormFields['medicineName'], patientID__patientID__exact = patientDetails.patientID, transactionCompleted__exact = 'N').get()
                if (billDetails.noOfTabletsOrdered+int(webFormFields['orderQuantity'])) > medDetails.noOfTabletsInStores:
                    messages.info(request,"Select a differnt Batch Number as combined " + webFormFields['medicineName'] + " medicine is greater than available in Stores")
                    return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
                billDetails.noOfTabletsOrdered = billDetails.noOfTabletsOrdered+int(webFormFields['orderQuantity'])
                billDetails.totalPrice = billDetails.noOfTabletsOrdered * billDetails.pricePerTablet
                billDetails.discountedPrice = billDetails.totalPrice*(Decimal(1)-(Decimal(billDetails.discount)/Decimal(100)))
            except ObjectDoesNotExist:
                billDetails = Bill(patientID=PatientDetail.objects.get(patientID = patientDetails.patientID),medicineName=webFormFields['medicineName'],noOfTabletsOrdered = int(webFormFields['orderQuantity']))
                billDetails.pricePerTablet = medDetails.pricePerTablet
                billDetails.totalPrice = Decimal(webFormFields['orderQuantity'])*medDetails.pricePerTablet
                billDetails.discount = int(webFormFields['discount'])
                billDetails.discountedPrice = (Decimal(1)-(Decimal(webFormFields['discount'])/Decimal(100)))*Decimal(webFormFields['orderQuantity'])*medDetails.pricePerTablet
                billDetails.transactionCompleted = 'N'
                billDetails.batchNo = medDetails.batchNo
                billDetails.expiryDate = medDetails.expiryDate
                if len(Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID,transactionCompleted__exact = 'N')) == 0:
                    billDetails.billNo = 'US00'+str(Bill.objects.count())
                    billDetails.billDate = timezone.now()
                else:
                    if len(Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID,transactionCompleted__exact = 'N')) > 1 :
                        unSettledRecord = Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID,transactionCompleted__exact = 'N')
                        unSettledRecord = unSettledRecord[0]
                    else:
                        unSettledRecord = Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID,transactionCompleted__exact = 'N').get()
                    billDetails.billNo = unSettledRecord.billNo
                    billDetails.billDate = unSettledRecord.billDate
            billDetails.save()
            messages.info(request,"Added medicine in Cart")
        else:
            messages.error(request,"!!!!!!!!!!Please check the Batch Number!!!!!!!!!!!!!!")
            return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
    elif (request.method == "POST" and request.POST.get('order')):
        billGeneration = Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID,transactionCompleted__exact = 'N')
        if billGeneration :
            return render(request, 'pharmacyapp/sideNavigation.html',{'billGeneration': billGeneration})
        else:
            messages.info(request, "Nothing in Cart")            
            return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
    return render(request, 'pharmacyapp/medicine_order.html', {'form': form})

@login_required    
def medicine_checkout(request, pk):
    patientInfo = get_object_or_404(PatientDetail, pk=pk)
    billGeneration = Bill.objects.all().filter(patientID__patientID__exact = patientInfo.patientID,transactionCompleted__exact = 'N')
    for billDetail in billGeneration:
        recordToBeUpdatedInPostModel = Post.objects.all().filter(medicineName__exact = billDetail.medicineName, batchNo__exact = billDetail.batchNo).get()
        recordToBeUpdatedInPostModel.noOfTabletsSold = recordToBeUpdatedInPostModel.noOfTabletsSold + billDetail.noOfTabletsOrdered
        recordToBeUpdatedInPostModel.noOfTabletsInStores =recordToBeUpdatedInPostModel.noOfTablets - recordToBeUpdatedInPostModel.noOfTabletsSold
        
        recordToBeUpdatedInBillModel = Bill.objects.all().filter(medicineName__exact = billDetail.medicineName, batchNo__exact = billDetail.batchNo, billNo__exact = billDetail.billNo).get()
        recordToBeUpdatedInBillModel.transactionCompleted = 'Y'
        
        recordToBeUpdatedInPostModel.save()
        recordToBeUpdatedInBillModel.save()
    return render(request, 'pharmacyapp/medicine_checkout.html', {'billGeneration': billGeneration})

@login_required    
def medicine_last_checkout(request, pk):
    patientInfo = get_object_or_404(PatientDetail, pk=pk)
    billGeneration = Bill.objects.all().filter(patientID__patientID__exact = patientInfo.patientID,transactionCompleted__exact = 'Y').latest('pk')
    billGeneration = Bill.objects.all().filter(billNo__exact = billGeneration.billNo,transactionCompleted__exact = 'Y')
    return render(request, 'pharmacyapp/medicine_checkout.html', {'billGeneration': billGeneration})
    
@login_required  
def medicine_remove(request, pk):
    billInfo = get_object_or_404(Bill,pk=pk)
    models = Bill.objects.filter(billNo__exact = billInfo.billNo, medicineName__exact=billInfo.medicineName, batchNo__exact = billInfo.batchNo, patientID__patientID__exact = billInfo.patientID.patientID, transactionCompleted__exact= 'N').delete()
    billGeneration = Bill.objects.all().filter(patientID__patientID__exact = billInfo.patientID.patientID,transactionCompleted__exact = 'N')
    if billGeneration :
        return render(request, 'pharmacyapp/sideNavigation.html',{'billGeneration': billGeneration})
    else:
        patientDetail = PatientDetail.objects.all().filter(patientID__exact = billInfo.patientID.patientID).get()
        return redirect('bill_details', pk=patientDetail.pk)
    

def report_sales(request):
    form = reportForm(request.POST)
    if (request.method == "POST" and request.POST.get('Today')):
        startdate = date.today()
        enddate = startdate+timedelta(days=0)
        reports= Bill.objects.filter(billDate__range=[startdate, enddate],transactionCompleted__exact = 'Y').order_by('billNo')
        return render(request, 'pharmacyapp/report_sales.html', {'reports': reports})
    elif(request.method == "POST" and request.POST.get('Yesterday')):
        startdate = date.today()-timedelta(days=1)
        enddate = startdate+timedelta(days=0)
        reports= Bill.objects.filter(billDate__range=[startdate, enddate],transactionCompleted__exact = 'Y').order_by('billNo')
        return render(request, 'pharmacyapp/report_sales.html', {'reports': reports})
    elif(request.method == "POST" and request.POST.get('custom')):
        webFormFields = request.POST
        if 'startDate' in request.POST:
            if webFormFields['startDate'] and webFormFields['endDate']:
                startdate = datetime.datetime.strptime(webFormFields['startDate'],'%d-%m-%Y')
                enddate = datetime.datetime.strptime(webFormFields['endDate'],'%d-%m-%Y')
                if enddate < startdate:
                    messages.info(request,"End date can not be earlier than start date")
                    return render(request, 'pharmacyapp/report_sales.html', {'form': form})
                reports= Bill.objects.filter(billDate__range=[startdate, enddate],transactionCompleted__exact = 'Y').order_by('billNo')
                return render(request, 'pharmacyapp/report_sales.html', {'reports': reports})
            else:
                messages.info(request,"Enter the dates")
                return render(request, 'pharmacyapp/report_sales.html', {'form': form})
        else:
            return render(request, 'pharmacyapp/report_sales.html', {'form': form})
    return render(request, 'pharmacyapp/report_sales.html', {'form': form})
    
def get_batch_no(request, medName):
    medName=medName.replace("-_____-"," ")
    current_meds = Post.objects.all().filter(medicineName=medName)
    json_models = serializers.serialize("json", current_meds)
    return HttpResponse(json_models, content_type="application/javascript")


@login_required
def meds_edit(request, pk):
    billAdjust = Bill.objects.filter(pk__exact=pk).get()
    billDet = Bill.objects.filter(billNo__exact=billAdjust.billNo)
    if request.POST.get('returnMeds'):
        webFormFields = request.POST
        meds2Return = webFormFields['meds2Return']
        if billAdjust.returnSales == "Y" :
            messages.info(request,"Medicine already returned. No more allowed")
            return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
        if int(meds2Return) > billAdjust.noOfTabletsOrdered:
            messages.info(request,"You are returning medicines more than you bought!! Pls check")
            return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
        if format(billAdjust.expiryDate,'%Y-%m-%d') < format(timezone.now(),'%Y-%m-%d'):
            messages.info(request,"You are returning medicines after its expired!! Pls check")
            return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
        billAdjust.returnSalesNoOfTablets  = int(meds2Return)
        billAdjust.returnSalesBillDate = timezone.now()
        billAdjust.returnDiscountedPrice = Decimal(meds2Return)*billAdjust.pricePerTablet*Decimal(1-billAdjust.discount/100)
        billAdjust.returnSales = 'Y'
        billAdjust.save()
        medsAdjust = Post.objects.all().filter(medicineName__exact = billAdjust.medicineName,batchNo__exact = billAdjust.batchNo).get()
        medsAdjust.noOfTabletsSold = medsAdjust.noOfTabletsSold - int(meds2Return)
        medsAdjust.noOfTabletsInStores = medsAdjust.noOfTabletsInStores + int(meds2Return)
        medsAdjust.save()
        billDet = Bill.objects.filter(billNo__exact=billAdjust.billNo)
        return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
    elif request.POST.get('back'):
        return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
    return render(request, 'pharmacyapp/meds_edit.html', {'billAdjust': billAdjust})

   
def report_returns(request):
    form = reportForm(request.POST)
    if (request.method == "POST" and request.POST.get('Today')):
        startdate = date.today()
        enddate = startdate+timedelta(days=0)
        reports= Bill.objects.filter(billDate__range=[startdate, enddate],returnSales__exact = 'Y').order_by('medicineName')
        return render(request, 'pharmacyapp/report_returns.html', {'reports': reports})
    elif(request.method == "POST" and request.POST.get('Yesterday')):
        startdate = date.today()-timedelta(days=1)
        enddate = startdate+timedelta(days=0)
        reports= Bill.objects.filter(returnSalesBillDate__range=[startdate, enddate],returnSales__exact = 'Y')
        return render(request, 'pharmacyapp/report_returns.html', {'reports': reports})
    elif(request.method == "POST" and request.POST.get('custom')):
        webFormFields = request.POST
        if 'startDate' in request.POST:
            if webFormFields['startDate'] and webFormFields['endDate']:
                startdate = datetime.datetime.strptime(webFormFields['startDate'],'%d-%m-%Y')
                enddate = datetime.datetime.strptime(webFormFields['endDate'],'%d-%m-%Y')
                if enddate < startdate:
                    messages.info(request,"End date can not be earlier than start date")
                    return render(request, 'pharmacyapp/report_returns.html', {'form': form})
                reports= Bill.objects.filter(returnSalesBillDate__range=[startdate, enddate],returnSales__exact = 'Y')
                return render(request, 'pharmacyapp/report_returns.html', {'reports': reports})
            else:
                messages.info(request,"Enter the dates")
                return render(request, 'pharmacyapp/report_returns.html', {'form': form})
        else:
            return render(request, 'pharmacyapp/report_returns.html', {'form': form})
    return render(request, 'pharmacyapp/report_returns.html', {'form': form})
