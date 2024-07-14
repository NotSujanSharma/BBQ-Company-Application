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