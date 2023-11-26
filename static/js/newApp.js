const appointmentTimeInput = document.getElementById('appointmentTime');

        appointmentTimeInput.addEventListener('input', function () {
            const selectedTime = appointmentTimeInput.value;
            if (selectedTime < '08:00' || selectedTime > '17:00') {
                appointmentTimeInput.setCustomValidity('Please select a time between 8:00 AM and 5:00 PM');
            }
            else {
                appointmentTimeInput.setCustomValidity('');
            }
        });

//date restriction script
const appointmentDateInput = document.getElementById('appointmentDate');
const today = new Date();
const yyyy = today.getFullYear();
let mm = today.getMonth() + 1; 
mm = (mm < 10 ? '0' : '') + mm;
const dd = today.getDate();
const currentDate = `${yyyy}-${mm}-${dd}`;

// Get the date until next month
const nextMonth = new Date();
nextMonth.setMonth(nextMonth.getMonth() + 1);
const nextMonthYYYY = nextMonth.getFullYear();
let nextMonthMM = nextMonth.getMonth() + 1;
nextMonthMM = (nextMonthMM < 10 ? '0' : '') + nextMonthMM;
const nextMonthDD = nextMonth.getDate();
const nextMonthDate = `${nextMonthYYYY}-${nextMonthMM}-${nextMonthDD}`;

// Set min and max attributes for the date input
appointmentDateInput.setAttribute('min', currentDate);
appointmentDateInput.setAttribute('max', nextMonthDate);