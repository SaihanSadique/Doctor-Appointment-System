fetch('/get_appointments_list')
    .then(response => response.json())
    .then(data => {
    const dateTimeArray = data.map(element => element.DateTime);
    console.log(dateTimeArray); // Array containing only DateTime strings
    const appointmentsData = document.querySelector('.appointmentsData');
    for (let i = 0; i < dateTimeArray.length; i++) {
        var tableRow = document.createElement('tr');
        var newRow = document.createElement('tr');
        var newCell = document.createElement('td');
        newCell.textContent = dateTimeArray[i];
        newRow.appendChild(newCell);
        // Append the row to the table
        appointmentsData.appendChild(newRow);

    }
    
})
.catch(error => console.error('Error:', error));