import requests
import time

# Endpoint
url = "http://127.0.0.1:8000/hackrx/run"

# Bearer token
headers = {
    "Authorization": "Bearer 0bb47e221b4a0fcd07e75742ec888026ed66cdf92f4caa4a3e7c3cd50237d896",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Request body
payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}

# Number of requests to send
num_requests = 5
timeout_seconds = 90

for i in range(num_requests):
    print(f"\n🚀 Sending request #{i+1}")
    start_time = time.time()
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout_seconds)
        total_duration = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        if response.ok:
            response_json = response.json()
            answers = response_json.get("answers", [])
            num_questions = len(answers)
            avg_duration = total_duration / num_questions if num_questions else 0

            print("✅ Success")
            print(f"⏱️ Total time: {total_duration:.2f} seconds")
            print(f"⏱️ Average time per question: {avg_duration:.2f} seconds")

            # Optional: Show Q&A
            for idx, ans in enumerate(answers):
                print(f"\nQ{idx+1}: {payload['questions'][idx]}")
                print(f"A{idx+1}: {ans}")
        else:
            print("❌ Error:")
            print(response.text)
    except requests.exceptions.Timeout:
        print("⏱️ Request failed: Timeout after 60 seconds")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")

    # Optional delay before next request
    # time.sleep(60)
