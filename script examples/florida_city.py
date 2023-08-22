import requests

def get_florida_cities():
    api_key = 'AIzaSyAOIh9JtdZaWKx7lES8Pt4nLarwrJ7nYUQ'
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': 'Florida, USA',
        'key': api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()
  

    print(data)  # 输出 API 返回的 JSON 数据
    florida_cities = []

    if data['status'] == 'OK':
        results = data['results']
        for result in results:
            address_components = result['address_components']
            for component in address_components:
                if 'locality' in component['types'] and 'political' in component['types']:
                    city_name = component['long_name']
                    florida_cities.append(city_name)

    return florida_cities


florida_cities = get_florida_cities()
print(florida_cities)
