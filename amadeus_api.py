# amadeus_api.py
import requests
import os

class AmadeusAPI:
    def __init__(self):
        # API_KEY = '1RIJKyIv2gPHu3EAEbFcmQKKHZQftHlF'  # Replace with your actual API key
        # API_SECRET = 'SDzzWw2zSqWanTxb'  # Replace with your actual API secret            
        self.api_key = "jb8VZHNabXGoAjKcNbnEEjMgAHa3Cb1M"  # Set this in your environment
        self.api_secret = "wUJs0VLupGAFaBGi"  # Set this in your environment

        # Check if API key and secret are available, otherwise raise an error
        if not self.api_key or not self.api_secret:
            raise ValueError("API Key or Secret not set in environment variables.")
        
        self.token, self.token_expiry = self.get_access_token()  # Fetch token on initialization

    def get_access_token(self, retries=3):
        """Fetch OAuth2 access token from Amadeus API with retry on network failure."""
        import time
        auth_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        last_error = None
        for attempt in range(retries):
            try:
                response = requests.post(auth_url, data=data, timeout=15)
                print(f"Auth Response Status Code: {response.status_code}")
                print(f"Auth Response Content: {response.text}")
                if response.status_code == 200:
                    token_info = response.json()
                    return token_info['access_token'], token_info.get('expires_in', 900)
                else:
                    raise Exception(f"Failed to get token: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError as e:
                last_error = e
                wait = 2 ** attempt
                print(f"Amadeus connection error (attempt {attempt+1}/{retries}), retrying in {wait}s... {e}")
                time.sleep(wait)
            except requests.exceptions.Timeout as e:
                last_error = e
                print(f"Amadeus token request timed out (attempt {attempt+1}/{retries})")
                time.sleep(2 ** attempt)
        raise Exception(f"Amadeus unreachable after {retries} retries: {last_error}")

    def ensure_valid_token(self):
        """Check if the token is valid or expired and refresh if necessary."""
        if not self.token or self.token_expiry <= 0:
            print("Token expired or not available. Fetching a new one...")
            self.token, self.token_expiry = self.get_access_token()

    def get_airport_city(self, city_name):
        """Get IATA code of an airport from a city name."""
        self.ensure_valid_token()
        url = f"https://test.api.amadeus.com/v1/reference-data/locations?keyword={city_name}&subType=AIRPORT"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers, timeout=15)

        # Handle token expiration (401 Unauthorized)
        if response.status_code == 401:
            print("Token invalid or expired. Refreshing token...")
            self.token, self.token_expiry = self.get_access_token()
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if data['data']:
                return data['data'][0]['iataCode']
            else:
                print(f"No IATA code found for {city_name}.")
                return None
        else:
            raise Exception(f"Error fetching IATA code: {response.status_code} - {response.text}")

    def search_flights(self, origin, destination, departure_date, adults=1):
        """Search flights between origin and destination on a specific date."""
        self.ensure_valid_token()
        url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': adults,
            'max': 5  # Limit results
        }

        response = requests.get(url, headers=headers, params=params, timeout=15)
    
        if response.status_code == 200:
            return response.json().get('data', [])
        else: 
            raise Exception(f"Flight search failed: {response.status_code} - {response.text}")
        
    def get_city_code(self, city_name):
        """Fetch the city code and geographic coordinates for the given city."""
        self.ensure_valid_token()
        url = "https://test.api.amadeus.com/v1/reference-data/locations"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"keyword": city_name, "subType": "CITY"}

        response = requests.get(url, headers=headers, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                city = data["data"][0]
                return {
                    "iataCode": city.get("iataCode"),
                    "latitude": city.get("geoCode", {}).get("latitude"),
                    "longitude": city.get("geoCode", {}).get("longitude"),
                }
        raise Exception(f"Error fetching city data: {response.status_code} - {response.text}")

    def get_airline_name(self, carrier_code):
        """Fetch the airline name using the carrier code."""
        self.ensure_valid_token()  # Ensure the token is valid
        url = f"https://test.api.amadeus.com/v1/reference-data/airlines"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"airlineCodes": carrier_code}

        response = requests.get(url, headers=headers, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if data['data']:
                return data['data'][0]['commonName']  # Return the airline name
            else:
                print(f"No airline found for carrier code {carrier_code}.")
                return carrier_code
        else:
            print(f"Error fetching airline name for {carrier_code}: {response.status_code} - {response.text}")
            return carrier_code
        

    def fetch_hotel_list_by_city(self, city_code):
        """Fetch a list of hotels in a given city using the city code."""
        try:
            self.ensure_valid_token()  # Ensure the token is valid
            url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
            headers = {"Authorization": f"Bearer {self.token}"}
            params = {"cityCode": city_code}

            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                hotels = response.json().get('data', [])
                if not hotels:
                    return []
                return [
                    {"hotelId": hotel["hotelId"], "name": hotel["name"]}
                    for hotel in hotels
                ]
            else:
                raise Exception(f"Failed to fetch hotels: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error fetching hotel list: {e}")
            return []

    def fetch_hotel_offers(self, hotel_ids, check_in_date, check_out_date, adults=1):
        try:
            max_chunk_size = 20
            self.ensure_valid_token()
            all_offers = []

            for i in range(0, len(hotel_ids), max_chunk_size):
                chunk = hotel_ids[i:i + max_chunk_size]
                url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
                headers = {"Authorization": f"Bearer {self.token}"}
                params = {
                    "hotelIds": ",".join(chunk),
                    "adults": adults,
                    "checkInDate": check_in_date,
                    "checkOutDate": check_out_date,
                }

                response = requests.get(url, headers=headers, params=params, timeout=15)
                if response.status_code == 200:
                    all_offers.extend(response.json().get("data", []))
                elif response.status_code == 400:
                    print(f"API Error: {response.json()}")  # Log error details
                    continue  # Skip invalid chunks
                else:
                    raise Exception(f"Failed to fetch hotel offers: {response.status_code} - {response.text}")

            return all_offers

        except Exception as e:
            print(f"Error fetching hotel offers: {e}")
            return []
        
    # def search_hotels(self, latitude, longitude, check_in_date, check_out_date, adults=1, radius=10):
    #     """Search for hotels near a given location."""
    #     self.ensure_valid_token()
    #     url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
    #     headers = {"Authorization": f"Bearer {self.token}"}
    #     params = {
    #         "latitude": latitude,
    #         "longitude": longitude,
    #         "checkInDate": check_in_date,
    #         "checkOutDate": check_out_date,
    #         "adults": adults,
    #         "radius": radius,  # Radius in kilometers
    #         "radiusUnit": "KM",
    #         "bestRateOnly": True,
    #         "currency": "USD",  # Currency for pricing
    #         "hotelSource": "ALL"
    #     }

    #     response = requests.get(url, headers=headers, params=params)
    #     if response.status_code == 200:
    #         return response.json().get('data', [])  # Return hotel offers
    #     else:
    #         raise Exception(f"Hotel search failed: {response.status_code} - {response.text}")
        
    # def search_flights_with_time(self, origin, destination, departure_date, departure_time, adults=1):
    #     """Search flights between origin and destination on a specific date and within a given departure time."""
    #     flights = self.search_flights(origin, destination, departure_date, adults)
        
    #     # Convert the departure time to a datetime object
    #     departure_time = datetime.strptime(departure_time, "%H:%M")
        
    #     filtered_flights = []
        
    #     for flight in flights:
    #         departure_time_str = flight.get('itineraries', [{}])[0].get('segments', [{}])[0].get('departure', {}).get('at', '')
    #         departure_time_flight = datetime.strptime(departure_time_str, "%Y-%m-%dT%H:%M:%S")
            
    #         # Compare the flight's departure time to the provided time
    #         if departure_time.time() == departure_time_flight.time():
    #             filtered_flights.append(flight)
        
    #     return filtered_flights

    # def get_flight_details(self, flight_id):
    #     """Fetch detailed flight information for a given flight ID."""
    #     self.ensure_valid_token()
    #     url = f"https://test.api.amadeus.com/v1/booking/flight-orders/{flight_id}"
    #     headers = {
    #         'Authorization': f'Bearer {self.token}',
    #         'Content-Type': 'application/json'
    #     }

    #     response = requests.get(url, headers=headers)

    #     if response.status_code == 401:
    #         print("Token expired. Fetching a new one...")
    #         self.token, self.token_expiry = self.get_access_token()
    #         headers['Authorization'] = f'Bearer {self.token}'
    #         response = requests.get(url, headers=headers)

    #     if response.status_code == 200:
    #         return response.json().get('data', {})
    #     else:
    #         raise Exception(f"Error fetching flight details: {response.status_code} - {response.text}")

    # def update_flight(self, flight_id, update_type, contact, update_value):
    #     """Update flight details based on type (date, destination, or boarding)."""
    #     self.ensure_valid_token()

    #     url = f"https://test.api.amadeus.com/v1/booking/flight-orders/{flight_id}/change-{update_type}"
        
    #     if update_type not in ["date", "destination", "boarding"]:
    #         raise ValueError("Invalid update type. Choose from 'date', 'destination', or 'boarding'.")

    #     headers = {
    #         'Authorization': f'Bearer {self.token}',
    #         'Content-Type': 'application/json'
    #     }

    #     data = {
    #         "contact": contact,
    #         f"new_{update_type}": update_value
    #     }

    #     response = requests.post(url, headers=headers, json=data)

    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         raise Exception(f"Failed to update flight {update_type}: {response.status_code} - {response.text}")

    # def cancel_flight(self, flight_id):
    #     """Cancel a flight with the given flight ID."""
    #     self.ensure_valid_token()

    #     url = f"https://test.api.amadeus.com/v1/booking/flight-orders/{flight_id}/cancel"

    #     headers = {
    #         'Authorization': f'Bearer {self.token}',
    #         'Content-Type': 'application/json'
    #     }

    #     response = requests.post(url, headers=headers)

    #     if response.status_code == 200:
    #         return response.json()  # Return the cancellation confirmation
    #     else:
    #         raise Exception(f"Failed to cancel flight: {response.status_code} - {response.text}")