#!/usr/bin/env python3

import requests
import json
import urllib3

# Disable SSL warnings when using verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Session cookies
SESSION_COOKIES = {
    'adAuthCookie': '3E4B8442C4C2B56A55611D00DB26D793B8B72FC1FC5D433E8C1EB8DB8923CCF9FAF264C8E59D72BAD342196F9E3C24AF277BB92504B17312AF5CF5E3E3983700C6688964BA9FD75864A6797CB6B074459C815AB3BD601F98D8A0517445BF8E509920987EB4CE13A80F04EBEF2A26DF5211E9FADA',
    'ui-tabs-1': '0',
    '_ga': 'GA1.1.209123277.1752075474',
    '_ga_6JKEKWMK4R': 'GS2.1.s1752333686$o7$g1$t1752334715$j60$l0$h0',
    'ASP.NET_SessionId': 'duvywnxg0ptglmba41bz2lun',
    'AWSALB': 'p5b2IUeOMx7IqHcoA4H208ubymsk1iEg+P5YxmsXlVyaRtfvdgY/2N/Gnl8J4NOe5lC0B0FMF7jyZxgK2cYJtKHlMS7A5egCJf1Mcttn9CDGudv1ZFmnIX6wbakR',
    'AWSALBCORS': 'p5b2IUeOMx7IqHcoA4H208ubymsk1iEg+P5YxmsXlVyaRtfvdgY/2N/Gnl8J4NOe5lC0B0FMF7jyZxgK2cYJtKHlMS7A5egCJf1Mcttn9CDGudv1ZFmnIX6wbakR'
}

# Common headers
COMMON_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://drill.gghc.com/rcp.html',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}


def get_payment_requests(emp_id=154, period_id=202506):
    """
    Fetch payment requests for a given employee and period.
    
    Args:
        emp_id (int): Employee ID
        period_id (int): Period ID
    
    Returns:
        dict: JSON response from the API
    """
    url = f'https://drill.gghc.com/extras/api/rcp/get-payment-requests.aspx'
    params = {
        'emp_id': emp_id,
        'period_id': period_id
    }
    
    try:
        response = requests.get(
            url,
            params=params,
            headers=COMMON_HEADERS,
            cookies=SESSION_COOKIES,
            verify=False
        )
        response.raise_for_status()
        
        # Save to file
        with open('payment_requests.json', 'w') as f:
            f.write(response.text)
        
        print(f"Payment requests saved to payment_requests.json")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching payment requests: {e}")
        return None


def update_payment_request(emp_id=154, request_id=85360, split=0.1, producer_approved=True, producer_rejected=False):
    """
    Update a payment request with approval/rejection status.
    
    Args:
        emp_id (int): Employee ID
        request_id (int): Payment request ID
        split (float): Split percentage
        producer_approved (bool): Producer approval status
        producer_rejected (bool): Producer rejection status
    
    Returns:
        dict: JSON response from the API
    """
    url = f'https://drill.gghc.com/extras/api/rcp/update-payment-request.aspx'
    params = {
        'emp_id': emp_id,
        'id': request_id,
        'split': split,
        'producerApproved_fl': str(producer_approved).lower(),
        'producerRejected_fl': str(producer_rejected).lower()
    }
    
    # Additional headers for POST request
    post_headers = COMMON_HEADERS.copy()
    post_headers.update({
        'content-length': '0',
        'origin': 'https://drill.gghc.com'
    })
    
    try:
        response = requests.post(
            url,
            params=params,
            headers=post_headers,
            cookies=SESSION_COOKIES,
            verify=False
        )
        response.raise_for_status()
        
        # Save to file
        with open('approval_json.json', 'w') as f:
            f.write(response.text)
        
        print(f"Payment request update saved to approval_json.json")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error updating payment request: {e}")
        return None


def get_payments_ytd(emp_id=154, period_id=202506):
    """
    Fetch year-to-date payments for a given employee and period.
    
    Args:
        emp_id (int): Employee ID
        period_id (int): Period ID
    
    Returns:
        dict: JSON response from the API
    """
    url = f'https://drill.gghc.com/extras/api/rcp/get-payments-ytd.aspx'
    params = {
        'emp_id': emp_id,
        'period_id': period_id
    }
    
    try:
        response = requests.get(
            url,
            params=params,
            headers=COMMON_HEADERS,
            cookies=SESSION_COOKIES,
            verify=False
        )
        response.raise_for_status()
        
        # Save to file
        with open('payments_ytd.json', 'w') as f:
            f.write(response.text)
        
        print(f"YTD payments saved to payments_ytd.json")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching YTD payments: {e}")
        return None


def main():
    """
    Main function to execute all API calls in sequence.
    """
    print("Starting RCP API calls...")
    
    # 1. Get payment requests
    print("\n1. Fetching payment requests...")
    payment_requests = get_payment_requests()
    
    # 2. Update payment request
    print("\n2. Updating payment request...")
    update_result = update_payment_request()
    
    # 3. Get YTD payments
    print("\n3. Fetching YTD payments...")
    ytd_payments = get_payments_ytd()
    
    print("\nAll API calls completed!")


if __name__ == "__main__":
    main()
