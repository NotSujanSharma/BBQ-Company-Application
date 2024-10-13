function fetchClientDetails(clientId) {
    // Replace this with your actual API endpoint
    const url = `/admin-portal/client-details/${clientId}/`;

    fetch(url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.success) {
                displayClientDetails(data.client);
            } else {
                showMessage('Failed to fetch client details', 'error');
            }
        })
        .catch(error => {
            console.error('Error fetching client details:', error);
            showMessage('Error fetching client details. Please try again.', 'error');
        });
}

function displayClientDetails(client) {
    const clientDetails = document.getElementById('clientDetails');
    clientDetails.innerHTML = `
        <div class="grid grid-cols-2 gap-4">
            <div class="col-span-2 sm:col-span-1">
                <p class="text-lg font-semibold mb-3">Personal Information</p>
                <p class="mb-2">Name: ${client.first_name} ${client.last_name}</p>
                <p class="mb-2">Email: <a href="/admin-portal/new-message/?email=${client.email}">${client.email}</a></p>
                <p class="mb-2">Phone: ${client.contact_number}</p>
                <p class="mb-2">Address: ${client.address}</p>
            </div>
            <div class="col-span-2 sm:col-span-1">
                <p class="text-lg font-semibold mb-3">Booking Information</p>
                <p class="mb-2">Total Bookings: ${client.booking_count}</p>
                <p class="mb-2">Last Booking: ${client.last_booking_date || 'N/A'}</p>
            </div>
            <div class="col-span-2">
                <p class="text-lg font-semibold mb-3">Additional Information</p>
                <p class="mb-2">Joined: ${formatDate(client.date_joined)}</p>
                <p class="mb-2">Preferred Event Type: ${client.preferred_event_type || 'Not specified'}</p>
            </div>
        </div>
    `;
    openPopup('Client Details');
}

function handleEventAction(action) {
    if (action === 'delete') {
        deleteClient(currentClientId);
    }
    else if (action === 'edit') {
        window.location.href = `/admin-portal/edit-client/${currentClientId}/`;
    }
    else {
        console.log(`Action: ${action}, Event ID: ${currentClientId}`);
        closePopup();
    }
}

function deleteClient(clientId) {
    const url = `/admin-portal/delete-client/${clientId}/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage('Client deleted successfully', 'success');
                closePopup();
                
            } else {
                showMessage('Failed to delete client', 'error');
            }
        })
        .catch(error => {
            console.error('Error deleting client:', error);
            showMessage('Error deleting client. Please try again.', 'error');

        
        })
        .finally(() => {
            setTimeout(() => {
                window.location.reload();
            }, 300);
        });
    
}