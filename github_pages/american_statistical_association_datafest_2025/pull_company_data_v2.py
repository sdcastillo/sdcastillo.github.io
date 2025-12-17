import requests

def get_business_info(company_name: str, state: str) -> dict:
    """
    Fetches the industry class and company size for a given company in a particular state
    by querying the CompanyEnrich.com API.

    Parameters
    ----------
    company_name : str
        Name of the company
    state : str
        U.S. state where the company is located (might or might not be used by the API)

    Returns
    -------
    dict
        A dictionary with keys:
          - 'industry_class': str
          - 'company_size': str
    """

    # WARNING: Hardcoding an API key is not recommended in production.
    # Use environment variables or a secrets manager for security.
    api_key = "REDACTED"  # Example key from prior snippet

    url = "https://api.companyenrich.com/companies/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # Adjust the payload to match the API's expected format
    payload = {
        "name": company_name,
        "state": state
    }

    # Debugging: Print the payload to inspect what is being sent to the API
    #print("Payload:", payload)

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error if 4XX/5XX status

        # Debugging: Print the raw API response to inspect its structure
        print("Full API Response:", response.text)

        # Parse the response to extract the first company from the 'items' list
        data = response.json()
        items = data.get("items", [])

        if not items:
            print("No companies found in the response.")
            return {
                "industry_class": "Unknown",
                "company_size": "Unknown"
            }

        # Filter the items list to find the company that matches the provided name
        matching_company = next((item for item in items if item.get("name", "").lower() == company_name.lower()), None)

        if not matching_company:
            print(f"No matching company found for name: {company_name}")
            return {
                "industry_class": "Unknown",
                "company_size": "Unknown"
            }

        # Extract details from the matching company
        industry_class = matching_company.get("industry", "Unknown")
        company_size = matching_company.get("financial", {}).get("total_funding", "Unknown")

        return {
            "industry_class": industry_class,
            "company_size": company_size
        }

    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print("Bad Request: Check the payload and API requirements.")
            print("Payload:", payload)
        print(f"Error occurred while calling the CompanyEnrich API: {e}")
        return {
            "industry_class": "Unknown",
            "company_size": "Unknown"
        }

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while calling the CompanyEnrich API: {e}")
        return {
            "industry_class": "Unknown",
            "company_size": "Unknown"
        }


if __name__ == "__main__":
    # Example usage (the result depends on live data from the API)
    info = get_business_info("Energy Insurance Mutual", "FL")/
    # e.g. might return:
    # {
    #   "industry_class": "Insurance",
    #   "company_size": "200-500 employees"
    # }

info = get_business_info("Airbnb", "WA")
print(info)0.
