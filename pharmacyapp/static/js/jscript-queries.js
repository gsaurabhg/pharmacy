if(typeof jQuery!=='undefined'){
    console.log('jQuery Loaded');
}
else{
    console.log('not loaded yet');
}

function sortTable(columnIndex, tableId) {
    // Get the table element
    var table = document.getElementById(tableId);
    var tbody = table.querySelector('tbody');
    var rows = Array.from(tbody.rows); // Convert HTMLCollection to array for sorting
    var switching = true;
    var dir;


    // Update sort icon for the specific table and column
    var headerRow = table.querySelector('thead tr');
    var headerCells = headerRow.querySelectorAll('th');
    headerCells.forEach(function(cell, index) {
        if (index === columnIndex) {
            var icon = cell.querySelector('.sort-icon');
            if (icon) {
                if (icon.innerHTML === '▲') {
                    dir = 'desc'; // If currently in ascending order, toggle to descending
                    icon.innerHTML = '&#9660;'; // Change icon to descending
                } else {
                    dir = 'asc'; // If currently in descending order, toggle to ascending
                    icon.innerHTML = '&#9650;'; // Change icon to ascending
                }

            }
        } else {
            // Clear sort icons from other header cells
            var icon = cell.querySelector('.sort-icon');
            if (icon) {
                icon.innerHTML = '';
            }
        }
    });


    // Perform radix sort on rows based on the column values
	rows.sort(function(rowA, rowB) {
		var xValue = rowA.cells[columnIndex].textContent.trim().toLowerCase();
		var yValue = rowB.cells[columnIndex].textContent.trim().toLowerCase();

		// Convert to numbers if possible
		var xNum = parseFloat(xValue);
		var yNum = parseFloat(yValue);

		if (!isNaN(xNum) && !isNaN(yNum)) {
			// If both values are numeric, compare as numbers
			return (dir === 'asc') ? xNum - yNum : yNum - xNum;
		} else {
			// Otherwise, compare as strings
			return (dir === 'asc') ? xValue.localeCompare(yValue) : yValue.localeCompare(xValue);
		}
	});

// Rearrange rows in the table based on sorted order
	rows.forEach(function(row) {
		tbody.appendChild(row);
	});
	rows.sort(function(rowA, rowB) {
		var xValue = rowA.cells[columnIndex].textContent.trim().toLowerCase();
		var yValue = rowB.cells[columnIndex].textContent.trim().toLowerCase();

		// Convert to numbers if possible
		var xNum = parseFloat(xValue);
		var yNum = parseFloat(yValue);

		if (!isNaN(xNum) && !isNaN(yNum)) {
			// If both values are numeric, compare as numbers
			return (dir === 'asc') ? xNum - yNum : yNum - xNum;
		} else {
			// Otherwise, compare as strings
			return (dir === 'asc') ? xValue.localeCompare(yValue) : yValue.localeCompare(xValue);
		}
	});

	// Rearrange rows in the table based on sorted order
	rows.forEach(function(row) {
		tbody.appendChild(row);
	});
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


$(document).ready(function() {
	// Remember and set the active tab
	var activeTab = "{{ active_tab }}";
	$('.nav-tabs a[href="#' + activeTab + '"]').tab('show');

	// Function to confirm delete
	function confirmDelete(medName, url) {
		var result = confirm("Are you sure you want to delete the medicine '" + medicineName + "'?");
		return result;
	}
});

console.log('End of Java script loading')