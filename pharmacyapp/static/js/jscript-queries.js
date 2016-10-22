if(typeof jQuery!=='undefined'){
    console.log('jQuery Loaded');
}
else{
    console.log('not loaded yet');
}



function computeTableColumnTotal(tableId, colNumber)
{
  var result = 0;
  try
  {
    var tableBody = window.document.getElementById(tableId).getElementsByTagName("tbody").item(0);
    var i;
    var howManyRows = tableBody.rows.length;
    for (i=1; i<(howManyRows-1); i++) // skip first and last row (hence i=1, and howManyRows-1)
    {
       var thisTextNode = tableBody.rows[i].cells[colNumber].childNodes.item(0);
       var thisNumber = parseFloat(thisTextNode.data);
       if (!isNaN(thisNumber))
         result += thisNumber;
	 } // end for
  } // end try
  catch (ex)
  {
     window.alert("Exception in function computeTableColumnTotal()\n" + ex);
     result = 0;
  }
  finally
  {
     return result;
  }

}

function finishTable()
{
  var totalPrice = computeTableColumnTotal("cartMeds",5);
  var totalDiscountedPrice = computeTableColumnTotal("cartMeds",7);
  try
  {
    window.document.getElementById("TP").innerHTML = totalPrice;
    window.document.getElementById("TDP").innerHTML = totalDiscountedPrice;
  }
  catch (ex)
  {
     window.alert("Exception in function finishTable()\n" + ex);
  }
  return;
}

function finishTable_retMeds()
{
  var totalReturnAmount = computeTableColumnTotal("cartMeds",9);
  try
  {
    window.document.getElementById("TP").innerHTML = totalReturnAmount;
  }
  catch (ex)
  {
     window.alert("Exception in function finishTable()\n" + ex);
  }
  return;
}


function printDiv(divName) {
     var printContents = document.getElementById(divName).innerHTML;
     var originalContents = document.body.innerHTML;

     document.body.innerHTML = printContents;

     window.print();

     document.body.innerHTML = originalContents;
}


function finishTable_v1()
{
  var totalPrice = computeTableColumnTotal("daysales",4);
  try
  {
    window.document.getElementById("TPP").innerHTML = totalPrice;
  }
  catch (ex)
  {
     window.alert("Exception in function finishTable()\n" + ex);
  }
  return;
}

function get_batch_no(request_data)
{
	request_data=request_data.trim().replace(/ /g, '-_____-');
	var url = "/medicineName/" + request_data + "/get_batch_no";
	var medicineName = request_data;
	$.getJSON(url, function(medName){
	var options = '<option value="Z">Select a BatchNo</option>';
	for (var i = 0; i < medName.length; i++) {
	options += '<option value="' + medName[i].fields['batchNo'] + '">' + medName[i].fields['batchNo'] + '</option>';
	}
	$("select#batchNo").html(options);
	$("select#batchNo").attr('disabled', false);
	});
}


$(document).ready( function() {
    $( "#startDate" ).datepicker({
      changeMonth: true,//this option for allowing user to select month
      changeYear: true, //this option for allowing user to select from year range
      dateFormat : 'dd-mm-yy',
      showButtonPanel: true,
    });
  });

$(document).ready( function() {
    $( "#endDate" ).datepicker({
      changeMonth: true,//this option for allowing user to select month
      changeYear: true, //this option for allowing user to select from year range
      dateFormat : 'dd-mm-yy',
      showButtonPanel: true,
    });
  });


$(document).ready(function() {
   $('#expiryDate').datepicker({
     changeMonth: true,
     changeYear: true,
     dateFormat: 'mm-yy',

     onClose: function() {
        var iMonth = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
        var iYear = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
        $(this).datepicker('setDate', new Date(iYear, iMonth, 1));
     },

     beforeShow: function() {
       if ((selDate = $(this).val()).length > 0)
       {
          iYear = selDate.substring(selDate.length - 4, selDate.length);
          iMonth = jQuery.inArray(selDate.substring(0, selDate.length - 5), $(this).datepicker('option', 'monthNames'));
          $(this).datepicker('option', 'defaultDate', new Date(iYear, iMonth, 1));
           $(this).datepicker('setDate', new Date(iYear, iMonth, 1));
       }
    }
  });
});


function adjustQuantity(retMed,medPK,medOrdered,returnSalesNoOfTablets,returnSales,expiryDate)
{
	if (isNaN(retMed) || isNaN(medPK) || retMed =="" )
	{
		document.getElementById("returnQuantity").disabled = true;
		alert("Must Input Numbers");
		return;
	}
	if (retMed > medOrdered )
	{
		document.getElementById("returnQuantity").disabled = true;
		alert("Return invoice is more than purchases")
		return;
	}
	var dateToday = new Date();
	var m = dateToday.getMonth()+1;
	var y = dateToday.getFullYear();
	var ex = new Date(expiryDate);
	var me = ex.getMonth()+1;
	var ye = ex.getFullYear();

	if (dateToday > ex)
	{
		document.getElementById("returnQuantity").disabled = true;
		alert("Expired");
		return;
	}
	if ((returnSales == "Y" ) || (returnSalesNoOfTablets > 0 ))
	{
		document.getElementById("returnQuantity").disabled = true;
		alert("Already Returned")
		return;
	}
    if (window.confirm("Are you sure you want to return "+ retMed + " medicines") == true) {
		var url = "/bill" + "/details/" + retMed + "/" + medPK;
		$.getJSON(url, function(models){});
		window.location.reload();
		document.getElementById("returnQuantity").disabled = true;
	}else {
		window.alert("cancel");
	}

}



function printReturnInvoice(divName) {
     var printContents = document.getElementById(divName).innerHTML;
     var originalContents = document.body.innerHTML;

     document.body.innerHTML = printContents;

     window.print();

     document.body.innerHTML = originalContents;
}
