from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, PatientDetail, Bill, returnBill
from .forms import PostForm, PatientForm, BillForm, CombinedForm, availableMedsForm, reportForm, medsAdjustForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
#Below import is needed for making OR based query
from django.db.models import Q, F, Count
#Below import is needed for creating the pop ups
from django.contrib import messages
from pharmacyapp.bing_search import run_query
from decimal import *
from datetime import datetime, date, timedelta, time
from django.core import validators
import datetime, time, json
from django.core import serializers
from django.http import HttpResponse
#needed for the pass word creae viewitems
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import logging 
from pharmacyapp.utilities import *

logging.basicConfig(filename="log.log", level=logging.DEBUG)

def welcome(request):
    return render(request, 'pharmacyapp/popup.html')

def post_list(request):
    posts = Post.objects.all().filter(noOfTabletsInStores__gt=0,expiryDate__gt=timezone.now()).order_by('medicineName')
    return render(request, 'pharmacyapp/post_list.html', {'posts':posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pharmacyapp/post_detail.html', {'post': post})

@login_required    
def post_new(request):
    current_user = request.user.username
    currentDate = datetime.datetime.strptime(str(format(datetime.date.today(), '%d-%m-%Y')),"%d-%m-%Y") 
    if (current_user == "admin" or current_user == "saurabhg"):
        if (request.method == "POST" and request.POST.get('save')):
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                webFormFields = request.POST
                enteredDate = datetime.datetime.strptime(webFormFields['dateOfPurchaseForm'],'%d-%m-%Y')
                #enteredDate = datetime.datetime.strptime(str(format(post.dateOfPurchase, '%d-%m-%Y')),"%d-%m-%Y") 
                if ( enteredDate > currentDate):
                    messages.info(request,"Purchase Date " + webFormFields['dateOfPurchaseForm'] + " can not be greater than Todays date i.e., " + format(timezone.now(), '%d-%m-%Y'))
                    return render(request, 'pharmacyapp/post_edit.html', {'form': form})
                post.dateOfPurchase= enteredDate
                if post.pack == 0:
                    messages.info(request,"Number of Tablets/Bottles to be greater than 0")
                    return render(request, 'pharmacyapp/post_edit.html', {'form': form})
                try:
                    medicineRecord = Post.objects.all().filter(medicineName__exact=post.medicineName,batchNo__exact = post.batchNo).get()
                    logging.debug('entered into the section of adding medicines for same batch')
                    logging.debug("Number of strips already in stores: {}".format(medicineRecord.quantity) + " Number of tablets/strip: {}" \
                    .format(medicineRecord.pack) + " batch Number entered: {}".format(medicineRecord.batchNo) + " medicine Name: {}" \
                    .format(medicineRecord.medicineName) + "  freeArticles: {}".format(medicineRecord.freeArticles) +" pack size: {}" \
                    .format(medicineRecord.pack) + " no of Tablets in Stores: {}".format(medicineRecord.noOfTabletsInStores))
                    "this section is basically if a person is entering more medicines for the same batch no. via new entry"
                    messages.info(request,"Found existing record in the stocks. Updating it")
                    medicineRecord.quantity = post.quantity+medicineRecord.quantity
                    medicineRecord.freeArticles = int(post.freeArticles)+medicineRecord.freeArticles
                    medicineRecord.noOfTablets = (medicineRecord.quantity+medicineRecord.freeArticles)*medicineRecord.pack
                    medicineRecord.noOfTabletsInStores = medicineRecord.noOfTablets - medicineRecord.noOfTabletsSold
                    medicineRecord.netPurchasePrice = medicineRecord.quantity*medicineRecord.pricePerStrip*(1+Decimal(medicineRecord.vat+medicineRecord.sat+medicineRecord.addTax)/100)
                    medicineRecord.save()
                    logging.debug("Entry by Admin: Number of strips purchased: {}".format(post.quantity) + "Number of tablets/strip: {}".format(post.pack))
                    logging.debug('-----------------------------------------------------------')
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
                    enteredExpiryDate = post.expiryDate
                    if enteredExpiryDate < currentDate:
                        messages.info(request,"enter the proper expiry Date")
                        return render(request, 'pharmacyapp/post_edit.html', {'form': form})
                    post.pharmacy_user = request.user
                    post.noOfTablets = (int(post.quantity)+int(post.freeArticles))*int(post.pack)
                    post.pricePerTablet = post.mrp/post.pack
                    post.noOfTabletsInStores = int(post.noOfTablets) - int(post.noOfTabletsSold)
                    post.netPurchasePrice = Decimal(post.quantity)*post.pricePerStrip*Decimal((100+int(post.vat)+int(post.sat)+int(post.addTax))/100)
                    post.save()
                    logging.debug('entered into the section of adding new medicines')
                    logging.debug("Input entry by Admin: Number of strips in stores: {}".format(post.quantity) + " Number of tablets/strip: {}" \
                    .format(post.pack) + " batch Number entered: {}".format(post.batchNo) + " medicine Name: {}".format(post.medicineName) + \
                    "  freeArticles: {}".format(post.freeArticles) + " pack size: {}".format(post.pack) + \
                    " no of Tablets in Stores: {}".format(post.noOfTabletsInStores))
                    logging.debug('------------------------------------------------------------------------------------------------')
                    return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'pharmacyapp/post_edit.html', {'form': form})
    else:
        messages.info(request,"You have to LOG in as ADMIN to use this feature")
        #posts = Post.objects.filter(dateOfPurchase__lte=timezone.now()).order_by('medicineName')
        posts = Post.objects.all().filter(noOfTabletsInStores__gt=0).order_by('medicineName')
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
            try:
                medicineRecord = Post.objects.all().filter(medicineName__exact=post.medicineName,batchNo__exact = post.batchNo).get()
            except ObjectDoesNotExist:
                messages.info(request,"If you want to change the medicine/batch Number, pls go through New Inventory with different batch")
                logging.debug("SCUM BAG: Medicine entered in edit mode: {}".format(post.medicineName) + \
                        " Batch No : {}".format(post.batchNo) + " pk value: {}".format(post.pk))
                return render(request, 'pharmacyapp/post_edit.html', {'form': form})
            if (medicineRecord.pk != post.pk):
                "this section is basically if a person is editing medicines for the exiting batch no."
                messages.info(request,"Found existing record in the stocks. Updating it")
                medicineRecord.quantity = post.quantity+medicineRecord.quantity
                medicineRecord.freeArticles = int(post.freeArticles)+medicineRecord.freeArticles
                medicineRecord.noOfTablets = (medicineRecord.quantity+medicineRecord.freeArticles)*medicineRecord.pack
                medicineRecord.noOfTabletsInStores = medicineRecord.noOfTablets - medicineRecord.noOfTabletsSold
                medicineRecord.netPurchasePrice = medicineRecord.quantity*medicineRecord.pricePerStrip*(1+Decimal(medicineRecord.vat+medicineRecord.sat+medicineRecord.addTax)/100)
                medicineRecord.save()
                post.delete()
            else:
                messages.info(request,"updated the record")
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
            bill_No = webFormFields['billNo'].upper()
            billDet = Bill.objects.filter(billNo__exact=bill_No)
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
    availableMeds = Post.objects.filter(noOfTabletsInStores__gt = 0).values().order_by('medicineName')
    medicineNameChoices = []
    for med in availableMeds:
        medicineNameChoices.append((med['medicineName'], med['medicineName']),)
    form = availableMedsForm(medicineNameChoices)
    if (request.method == "POST" and request.POST.get('addMed')):
        webFormFields = request.POST
        if 'batchNo' not in webFormFields:
            messages.info(request,"Please fill batchNo")
            return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
        if (webFormFields['medicineName'] == '' or webFormFields['orderQuantity'] == '' or webFormFields['batchNo'] == ''):
            messages.info(request,"Please fill all the fields")
            return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
        if (int(webFormFields['orderQuantity']) <= 0):
            messages.info(request,"Please fill proper quantity of medicines ")
            return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
        if  Post.objects.all().filter(medicineName__exact = webFormFields['medicineName'], batchNo__exact = webFormFields['batchNo']):
            if len(Post.objects.all().filter(medicineName__exact = webFormFields['medicineName'], batchNo__exact = webFormFields['batchNo'])) > 1 :
                logging.debug('Found Multiple Records')
                logging.debug("Multiple Records: Name of Medicine: {}".format(webFormFields['medicineName']) + \
                " batch Number entered: {}".format(webFormFields['batchNo']))
                logging.debug('------------------------------------------------------------------------------------------------')
                messages.info(request,"Please Reach out to Admin as Fault has happen for Medicine: "+ webFormFields['medicineName'])
                return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
            else:
                medDetails = Post.objects.all().filter(medicineName__exact = webFormFields['medicineName'], \
                batchNo__exact = webFormFields['batchNo']).get()
            if format(medDetails.expiryDate,'%Y-%m-%d') < format(timezone.now(),'%Y-%m-%d'):
                messages.info(request,"Can Not Sale " + medDetails.medicineName + " medicine as its Expired on "+ format(medDetails.expiryDate,'%Y-%m-%d'))
                return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
            if Decimal(webFormFields['orderQuantity']) > medDetails.noOfTabletsInStores:
                messages.info(request,"Quantity of " +webFormFields['medicineName']+ " has to be less than " + str(medDetails.noOfTabletsInStores) + " instead of " + webFormFields['orderQuantity'])
                messages.info(request,"Reach Out to Admin for ordering more medicine in Pharmacy")
                return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
            try:
                billDetails = Bill.objects.all().filter(medicineName__exact = webFormFields['medicineName'],patientID__patientID__exact = \
                patientDetails.patientID, transactionCompleted__exact = 'N', batchNo__exact = webFormFields['batchNo']).get()
                if (billDetails.noOfTabletsOrdered+int(webFormFields['orderQuantity'])) > medDetails.noOfTabletsInStores:
                    messages.info(request,"Select a different Batch Number as combined " + webFormFields['medicineName'] + \
                    " medicine is greater than available in Stores")
                    return render(request, 'pharmacyapp/medicine_order.html', {'form': form})
                billDetails.noOfTabletsOrdered = billDetails.noOfTabletsOrdered+int(webFormFields['orderQuantity'])
                billDetails.totalPrice = billDetails.noOfTabletsOrdered * billDetails.pricePerTablet
                billDetails.discountedPrice = billDetails.totalPrice*(Decimal(1)-(Decimal(billDetails.discount)/Decimal(100)))
            except ObjectDoesNotExist:
                billDetails = Bill(patientID=PatientDetail.objects.get(patientID = patientDetails.patientID), \
                medicineName=webFormFields['medicineName'],noOfTabletsOrdered = int(webFormFields['orderQuantity']))
                billDetails.pricePerTablet = medDetails.pricePerTablet
                billDetails.totalPrice = Decimal(webFormFields['orderQuantity'])*medDetails.pricePerTablet
                billDetails.discount = int(webFormFields['discount'])
                billDetails.discountedPrice = (Decimal(1)-(Decimal(webFormFields['discount'])/Decimal(100)))*Decimal(webFormFields['orderQuantity'])*medDetails.pricePerTablet
                billDetails.transactionCompleted = 'N'
                billDetails.batchNo = medDetails.batchNo
                billDetails.expiryDate = medDetails.expiryDate
                if len(Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID,transactionCompleted__exact = 'N')) == 0:
                    Bill.objects.filter(transactionCompleted__exact= 'N').delete()
                    noOfBills = Bill.objects.values('billNo').annotate(cnt=Count('billNo'))
                    billDetails.billNo = 'SSDS-19-'+str(len(noOfBills))
                    billDetails.billDate = timezone.now()
                else:
                    if len(Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID,transactionCompleted__exact = 'N')) > 1 :
                        unSettledRecord = Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID, \
                        transactionCompleted__exact = 'N')
                        unSettledRecord = unSettledRecord[0]
                    else:
                        unSettledRecord = Bill.objects.all().filter(patientID__patientID__exact = patientDetails.patientID, \
                        transactionCompleted__exact = 'N').get()
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
        recordToBeUpdatedInPostModel = Post.objects.all().filter(medicineName__exact = billDetail.medicineName, \
        batchNo__exact = billDetail.batchNo).get()
        if ((recordToBeUpdatedInPostModel.noOfTablets-(recordToBeUpdatedInPostModel.noOfTabletsSold+billDetail.noOfTabletsOrdered)) < 0) or \
        (recordToBeUpdatedInPostModel.noOfTabletsInStores - billDetail.noOfTabletsOrdered < 0) :
                messages.info(request, "pls reduce the amount of medicine " + recordToBeUpdatedInPostModel.medicineName + " Available: " + \
                str(recordToBeUpdatedInPostModel.noOfTabletsInStores))
                return render(request, 'pharmacyapp/sideNavigation.html',{'billGeneration': billGeneration})
    for billDetail in billGeneration:
        recordToBeUpdatedInPostModel = Post.objects.all().filter(medicineName__exact = billDetail.medicineName, \
        batchNo__exact = billDetail.batchNo).get()
        recordToBeUpdatedInPostModel.noOfTabletsSold = recordToBeUpdatedInPostModel.noOfTabletsSold + billDetail.noOfTabletsOrdered
        recordToBeUpdatedInPostModel.noOfTabletsInStores =recordToBeUpdatedInPostModel.noOfTabletsInStores - billDetail.noOfTabletsOrdered
        
        recordToBeUpdatedInBillModel = Bill.objects.all().filter(medicineName__exact = billDetail.medicineName, \
        batchNo__exact = billDetail.batchNo, billNo__exact = billDetail.billNo).get()
        recordToBeUpdatedInBillModel.transactionCompleted = 'Y'
        
        recordToBeUpdatedInPostModel.save()
        recordToBeUpdatedInBillModel.save()
    #passing the bill no to generate the pdf
    generate_pdf(billGeneration[0].billNo)
    return render(request, 'pharmacyapp/medicine_checkout.html', {'billGeneration': billGeneration})

@login_required    
def medicine_last_checkout(request, pk):
    patientInfo = get_object_or_404(PatientDetail, pk=pk)
    #To fix the use case of first entry
    try:
        billGeneration = Bill.objects.all().filter(patientID__patientID__exact = patientInfo.patientID,transactionCompleted__exact = 'Y').latest('pk')
    except ObjectDoesNotExist :
        messages.info(request,"This is the first time Customer, so no previous Invoice found")
        return redirect('patient_details')
    billGeneration = Bill.objects.all().filter(billNo__exact = billGeneration.billNo,transactionCompleted__exact = 'Y')
    return render(request, 'pharmacyapp/medicine_checkout.html', {'billGeneration': billGeneration})
    
@login_required  
def medicine_remove(request, pk):
    billInfo = get_object_or_404(Bill,pk=pk)
    models = Bill.objects.filter(billNo__exact = billInfo.billNo, medicineName__exact=billInfo.medicineName, \
    batchNo__exact = billInfo.batchNo, patientID__patientID__exact = billInfo.patientID.patientID, transactionCompleted__exact= 'N').delete()
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
    current_meds = Post.objects.all().filter(medicineName=medName,noOfTabletsInStores__gt = 0)
    json_models = serializers.serialize("json", current_meds)
    return HttpResponse(json_models, content_type="application/javascript")


@login_required
def meds_edit(request, pk):
    billAdjust = Bill.objects.filter(pk__exact=pk).get()
    billDet = Bill.objects.filter(billNo__exact=billAdjust.billNo)
    if request.POST.get('returnMeds'):
        webFormFields = request.POST
        meds2Return = webFormFields['meds2Return']
        if meds2Return == "" :
            messages.info(request,"Enter valid number of tablets to be returned")
            return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
        if billAdjust.returnSales == "Y" :
            messages.info(request,"Medicine already returned. No more allowed")
            return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
        if int(meds2Return) > billAdjust.noOfTabletsOrdered:
            messages.info(request,"You are returning medicines more than you bought!! Pls check")
            return render(request, 'pharmacyapp/meds_return.html', {'billDet':billDet})
        if int(meds2Return) < 0:
            messages.info(request,"Whew..u r the culprit!! wake up")
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
        reports= Bill.objects.filter(returnSalesBillDate__range=[startdate, enddate],returnSales__exact = 'Y').order_by('medicineName')
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


@login_required
def meds_null(request):
    #exhaustedMedicines=Post.objects.all().annotate(delta=F('noOfTabletsInStores')+F('noOfTabletsToTrf')).filter(delta__lt=1).order_by('medicineName')
    #exhaustedMedicines.delete()
    #medsNull=Post.objects.all().filter(noOfTabletsSold__gt=0)
    #for medNull in medsNull:
    #    wholePack=medNull.noOfTabletsSold//medNull.pack
    #    medNull.quantity-=wholePack
    #    medNull.noOfTabletsSold-=(wholePack*medNull.pack)
    #    medNull.noOfTablets-=(wholePack*medNull.pack)
    #    medNull.save()
    #    logging.debug('updated '+ medNull.medicineName)
    #startdate = datetime.datetime.strptime('16-02-2018','%d-%m-%Y')
    #enddate = datetime.datetime.strptime('31-03-2018','%d-%m-%Y')
    #BillLastFinYear= Bill.objects.filter(returnSalesBillDate__range=[startdate, enddate])
    #BillLastFinYear.delete()
    posts = Post.objects.all().annotate(delta=F('noOfTabletsInStores')+F('noOfTabletsToTrf')).filter(delta__gt=0).order_by('medicineName')
    return render(request, 'pharmacyapp/post_list.html', {'posts':posts})
