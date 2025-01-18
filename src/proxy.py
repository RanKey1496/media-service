import requests
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS

gateway = ApiGateway("https://i.instagram.com", access_key_id='', access_key_secret='')
gateway.start()

session = requests.Session()
session.mount("https://i.instagram.com", gateway)

response = session.get("https://i.instagram.com/api/v1/users/web_profile_info/?username=brazilian_301")
print(response.status_code)

# Only run this line if you are no longer going to run the script, as it takes longer to boot up again next time.
gateway.shutdown()