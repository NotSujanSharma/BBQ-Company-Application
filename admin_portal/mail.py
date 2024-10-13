import requests

def send_mail(subject, message, recipient_list):
    print(f"Sending email to {recipient_list} with subject: {subject} and message: {message}")
    total_sent = 0
    cloudflare_url = 'https://lively-sun-8327.admin-60e.workers.dev/'  # Replace with your actual worker URL
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sujansharmathegreat'  # Replace with your actual secret key
    }
    for recipient in recipient_list:
        
        payload = {
            'to': recipient,
            'subject': subject,
            'message': message
        }

        response = requests.post(cloudflare_url, json=payload, headers=headers)
        print(response.json())
        if response.status_code == 200:
            total_sent += 1    
    if total_sent > 0:
        return True
    return False