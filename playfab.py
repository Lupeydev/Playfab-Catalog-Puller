import requests
import json

# ======================
# CONFIGURATION
# ======================
TITLE_ID = "8d85f"        # Replace with your PlayFab Title ID
CUSTOM_ID = "daddyvdb"  # Any unique identifier for testing
CATALOG_VERSION = "Cosmetics"   # The catalog version you want to fetch

# ======================
# 1️⃣ LOGIN
# ======================
LOGIN_URL = f"https://{TITLE_ID}.playfabapi.com/Client/LoginWithCustomID"

login_payload = {
    "TitleId": TITLE_ID,
    "CustomId": CUSTOM_ID,
    "CreateAccount": True
}

headers = {
    "Content-Type": "application/json",
    "X-PlayFabSDK": "PythonCustom"
}

login_resp = requests.post(LOGIN_URL, headers=headers, json=login_payload)
login_data = login_resp.json()

if login_resp.status_code != 200 or "SessionTicket" not in login_data.get("data", {}):
    print("Login failed:", json.dumps(login_data, indent=2))
    exit(1)

session_ticket = login_data["data"]["SessionTicket"]
print("✅ Login successful. SessionTicket acquired.")

# ======================
# 2️⃣ GET CATALOG ITEMS
# ======================
CATALOG_URL = f"https://{TITLE_ID}.playfabapi.com/Client/GetCatalogItems"

headers["X-Authorization"] = session_ticket

catalog_payload = {
    "CatalogVersion": CATALOG_VERSION
}

print(f"\nRequesting catalog '{CATALOG_VERSION}'...")

catalog_resp = requests.post(CATALOG_URL, headers=headers, json=catalog_payload)
catalog_data = catalog_resp.json()

if catalog_resp.status_code != 200:
    print("Failed to get catalog:", json.dumps(catalog_data, indent=2))
else:
    catalog_items = catalog_data.get("data", {}).get("Catalog", [])
    if not catalog_items:
        print(f"⚠️ Catalog is empty. Make sure '{CATALOG_VERSION}' is published and has items.")
    else:
        print(f"✅ Retrieved {len(catalog_items)} items from catalog '{CATALOG_VERSION}':\n")
        for item in catalog_items:
            print(json.dumps(item, indent=2))
