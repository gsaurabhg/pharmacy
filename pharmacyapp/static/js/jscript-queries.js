if(typeof jQuery!=='undefined'){
    console.log('jQuery Loaded');
}
else{
    console.log('not loaded yet');
}

function sortTable(columnIndex) {
	// Toggle sorting direction
	if (columnIndex == 0) {
		return;
	}
	if (dir === 'asc') {
		dir = 'desc';
	} else {
		dir = 'asc';
	}

	// Update sort icon
	var icon = document.querySelectorAll('.sort-icon');
	icon.forEach(function(element) {
		element.innerHTML = ''; // Clear previous icons
	});
    icon[columnIndex].innerHTML = dir === 'asc' ? '&#9650;' : '&#9660;';

	var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
	table = document.getElementById("stock-table");
	switching = true;
	// Set the sorting direction to ascending:
	//dir = "asc";
	/* Make a loop that will continue until
	no switching has been done: */
	while (switching) {
		// Start by saying: no switching is done:
		switching = false;
		rows = table.rows;
		/* Loop through all table rows (except the
		first, which contains table headers): */
		for (i = 1; i < (rows.length - 1); i++) {
			// Start by saying there should be no switching:
			shouldSwitch = false;
			/* Get the two elements you want to compare,
			one from current row and one from the next: */
			x = rows[i].getElementsByTagName("td")[columnIndex];
			y = rows[i + 1].getElementsByTagName("td")[columnIndex];
			//var xValue = x.innerHTML.trim().toLowerCase();
            //var yValue = y.innerHTML.trim().toLowerCase();
			/* Check if the two rows should switch place,
			based on the direction, asc or desc: */
			if (dir == "asc") {
				if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
					// If so, mark as a switch and break the loop:
					shouldSwitch = true;
					break;
				}
			} else if (dir == "desc") {
				if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
					// If so, mark as a switch and break the loop:
					shouldSwitch = true;
					break;
				}
			}
		}
		if (shouldSwitch) {
			/* If a switch has been marked, make the switch
			and mark that a switch has been done: */
			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
			switching = true;
			// Each time a switch is done, increase this count by 1:
			switchcount++;
		} else {
			/* If no switching has been done AND the direction is "asc",
			set the direction to "desc" and run the while loop again. */
			if (switchcount == 0 && dir == "asc") {
				dir = "desc";
				switching = true;
			}
		}
	}
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
  var totalPrice1 = computeTableColumnTotal("cartMeds",5);
  var totalPrice = Math.round(totalPrice1*100)/100;
  var totalDiscountedPriceUnrounded = computeTableColumnTotal("cartMeds",7);
  var totalDiscountedPrice = Math.round(totalDiscountedPriceUnrounded*100)/100;
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

(5,6)
function finishTable_2ClmnSum(colNo1,colNo2)
{
  var totalPrice1 = computeTableColumnTotal("cartMeds",colNo1);
  var totalPrice = Math.round(totalPrice1*100)/100;
  var totalDiscountedPriceUnrounded = computeTableColumnTotal("cartMeds",colNo2);
  var totalDiscountedPrice = Math.round(totalDiscountedPriceUnrounded*100)/100;
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


function finishTable_v1(colNo)
{
  var totalPrice = computeTableColumnTotal("daysales",colNo);
  var totalPriceRounded = Math.round(totalPrice*100)/100;
  try
  {
    window.document.getElementById("TPP").innerHTML = totalPriceRounded;
  }
  catch (ex)
  {
     window.alert("Exception in function finishTable()\n" + ex);
  }
  return;
}

function get_batch_no(request_data)
{
	request_data=request_data.trim().replace(/\s/g, '-_____-');
	var url = "/medicineName/" + request_data + "/get_batch_no";
	var medicineName = request_data;
	$.getJSON(url, function(medName){
	var options = '<option></option>';
	for (var i = 0; i < medName.length; i++) {
	options += '<option value="' + medName[i].fields['batchNo'] + '">' + medName[i].fields['batchNo'] + '</option>';
	}
	$("select#batchNo").html(options);
	$("select#batchNo").attr('disabled', false);
	});
}


function printReturnInvoice(divName) {
     var printContents = document.getElementById(divName).innerHTML;
     var originalContents = document.body.innerHTML;

     document.body.innerHTML = printContents;

     window.print();

     document.body.innerHTML = originalContents;
}

function confirmDelete(medicineName) {
    var result = confirm("Are you sure you want to delete the medicine '" + medicineName + "'?");
    return result;
}

console.log('End of Java script loading')