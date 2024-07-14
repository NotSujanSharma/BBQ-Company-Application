console.log('main.js loaded');
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function formatTime(timeString) {
    const options = { hour: 'numeric', minute: 'numeric', hour12: true };
    return new Date(`1970-01-01T${timeString}`).toLocaleTimeString(undefined, options);
}

function getStatusColor(status) {
    const colorMap = {
        0: 'text-yellow-400',
        1: 'text-green-400',
        2: 'text-red-400',
        3: 'text-blue-400'
    };
    return colorMap[status] || 'text-gray-400';
}
function getStatusString(status) {
    const statusMap = {
        0: 'Pending',
        1: 'Confirmed',
        2: 'Cancelled',
        3: 'Completed'
    };
    return statusMap[status] || 'Unknown';
}

function formatJSONField(jsonField) {
    return Object.entries(jsonField)
        .map(([key, value]) => `<p class="mb-1">${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}</p>`)
        .join('');
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
}
    

function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    messageDiv.classList.add('fixed', 'top-4', 'right-4', 'p-4', 'rounded', 'text-white', 'opacity-0', 'transition-opacity', 'duration-300');

    if (type === 'success') {
        messageDiv.classList.add('bg-green-600');
    } else {
        messageDiv.classList.add('bg-red-600');
    }

    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.classList.add('opacity-100');
    }, 10);

    setTimeout(() => {
        messageDiv.classList.remove('opacity-100');
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 3000);
}

function openPopup(popupTitle) {
    const popup = document.getElementById('popupWindow');
    const popupContent = popup.querySelector('div');
    document.getElementById('popupTitle').textContent = popupTitle;

    popup.classList.remove('hidden');
    popup.classList.add('flex');

    setTimeout(() => {
        popupContent.classList.remove('scale-95', 'opacity-0');
        popupContent.classList.add('scale-100', 'opacity-100');
    }, 10);
}

function closePopup() {
    const popup = document.getElementById('popupWindow');
    const popupContent = popup.querySelector('div');

    popupContent.classList.remove('scale-100', 'opacity-100');
    popupContent.classList.add('scale-95', 'opacity-0');

    setTimeout(() => {
        popup.classList.remove('flex');
        popup.classList.add('hidden');
    }, 300);
}

function fetchBookingDetails(bookingId, generatePDF = false) {
    const url = `/admin-portal/booking-details/${bookingId}/`;

    fetch(url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (generatePDF) {
                    generateBookingPDF(data.booking);
                } else {
                    displayBookingDetails(data.booking);
                }
            } else {
                showMessage('Failed to fetch booking details', 'error');
            }
        })
        .catch(error => {
            console.error('Error fetching booking details:', error);
            showMessage('Error fetching booking details. Please try again.', 'error');
        });
}

function generateBookingPDF(booking) {
    if (typeof window.jspdf === 'undefined') {
        console.error('jsPDF library not loaded');
        showMessage('Error generating PDF. Please try again later.', 'error');
        return;
    }

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    doc.setFontSize(18);
    doc.text('Event Details', 105, 15, null, null, 'center');

    doc.setFontSize(12);
    doc.text(`Event Type: ${booking.event_type}`, 20, 30);
    doc.text(`Date: ${formatDate(booking.date)} - ${formatTime(booking.time)}`, 20, 40);
    doc.text(`Number of Guests: ${booking.guests}`, 20, 50);
    doc.text(`Location: ${booking.location}`, 20, 60);
    doc.text(`Status: ${getStatusString(booking.status)}`, 20, 70);

    doc.text('Client Information', 120, 30);
    doc.text(`Name: ${booking.user.first_name} ${booking.user.last_name}`, 120, 40);
    doc.text(`Email: ${booking.user.email}`, 120, 50);
    doc.text(`Contact: ${booking.user.contact_number}`, 120, 60);

    doc.text('Menu', 20, 80);
    let yPos = 90;
    ['Main Dishes', 'Side Dishes', 'Desserts'].forEach(category => {
        doc.text(`${category}:`, 20, yPos);
        yPos += 10;
        Object.entries(booking[category.toLowerCase().replace(' ', '_')]).forEach(([item, quantity]) => {
            doc.text(`- ${item}: ${quantity}`, 30, yPos);
            yPos += 10;
        });
        yPos += 5;
    });

    doc.text(`Drinks: ${booking.drinks}`, 20, yPos);

    doc.save(`${booking.event_type}_${booking.user.first_name}.pdf`);
}