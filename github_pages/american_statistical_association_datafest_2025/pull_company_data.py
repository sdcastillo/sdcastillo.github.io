import os
import requests

def get_business_info(company_name: str, state: str) -> dict:
    """
    Fetches the industry class and company size for a given company in a particular state
    by querying the CompanyEnrich.com API. This example assumes you can identify the
    company by 'name' (and possibly 'state'), but typically domain-based lookups are
    more reliable.

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

    Notes
    -----
    - Actual request/response structure depends on CompanyEnrich.com's live API.
    - Typically, domain-based lookups are preferred (they cost 1 credit per domain).
    - If you must rely on `name`, ensure the API supports name-based enrichment.
    - Store your API key securely (e.g., as an environment variable).
    """

    # Example: store your API key in an environment variable named "COMPANY_ENRICH_API_KEY"
    # or replace below with your actual key (not recommended for production).
    api_key = os.getenv("COMPANY_ENRICH_API_KEY", "REDACTED")

    # According to companyenrich.com summary:
    #   "You need to provide at least one of the following properties:
    #    Domain, Name, LinkedinUrl, TwitterUrl, FacebookUrl, InstagramUrl"
    #
    # For demonstration, we'll pass 'name' plus 'state'. The actual endpoint and
    # accepted parameters may differ. Check the official docs for correct usage.

    url = "https://api.companyenrich.com/companies/search"  # Hypothetical endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": "Energy Insurance Mutual",
        # Optional: If the API supports location filters
        # "location": state
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError if 4xx/5xx status
        data = response.json()

        # The structure of `data` will depend on CompanyEnrich.com's actual response.
        # The following is *hypothetical*; adapt to their real fields.

        # Example expected response (fictional):
        # {
        #   "company": {
        #       "name": "Kimley-Horn",
        #       "industry": "Engineering",
        #       "size_range": "201-500",        # or "employees": 300
        #       ...
        #   },
        #   ...
        # }

        company_info = data.get("company", {})
        if not company_info:
            return {
                "industry_class": "Unknown",
                "company_size": "Unknown"
            }

        industry_class = company_info.get("industry", "Unknown")

        # Suppose we get a 'size_range' or 'employees_range' string like "201-500"
        # We'll convert it to a human-readable format for demonstration:
        size_range = company_info.get("size_range", "Unknown")

        # Optionally map known ranges to more descriptive text:
        size_mapping = {
            "1-10": "1-10 employees",
            "11-50": "11-50 employees",
            "51-100": "50-100 employees",
            "101-250": "100-250 employees",
            "201-500": "200-500 employees",
            "501-1000": "500-1,000 employees",
            "1001-5000": "1,000-5,000 employees",
            "5001-10000": "5,000-10,000 employees",
            "10001+": "10,000+ employees"
        }
        company_size = size_mapping.get(size_range, "Unknown")

        return {
            "industry_class": industry_class,
            "company_size": company_size
        }

    except requests.exceptions.RequestException as e:
        # Handle network errors, timeouts, etc.
        print(f"Error occurred while fetching business info: {e}")
        return {
            "industry_class": "Unknown",
            "company_size": "Unknown"
        }


if __name__ == "__main__":
    # Example usage:
    info = get_business_info("Kimley-Horn", "GA")
    print(info)
    # Example output (depends on live data):
    # {
    #   "industry_class": "Engineering",
    #   "company_size": "200-500 employees"
    # }

