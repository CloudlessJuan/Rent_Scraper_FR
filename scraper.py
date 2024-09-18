import requests
import os
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import io

def fetch_and_upload_city_data():
    # Definir las ciudades y sus respectivos IDs
    cities = {
        "Envigado": "596f30cb-3582-416e-a071-71634190a703",
        "La estrella": "c19b4e81-f003-408a-b7db-4bbcb9b3b6d5",
        "Caldas": "5499b608-1002-43a3-9215-01c40ffae22b",
        "Sabaneta": "241a17ef-3aa0-485c-93aa-689fc2f2d114",
        "Itaguí": "cf5dc27a-9e05-4b0a-b98a-0715fe4e5d2b",
        "Bello": "9feb0402-fc35-4538-8ca1-d53c0fec2c35",
        "Copacabana": "b8f0f380-18c4-49ee-a6b3-92b454846718",
        "Girardota": "0affff3e-ec6a-421e-a2d4-8b198493cff9",
        "Barbosa": "1041113c-cced-48fc-a1d5-c10002214f67",
        "Medellín": "183f0a11-9452-4160-9089-1b0e7ed45863"
    }

    # URL de la API
    url = "https://search-service.fincaraiz.com.co/api/v1/properties/search"

    # Headers de la solicitud
    headers = {
        "Host": "search-service.fincaraiz.com.co",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://www.fincaraiz.com.co/arriendo/casas-y-apartamentos/medellin/antioquia",
        "Content-Type": "application/json",
        "Origin": "https://www.fincaraiz.com.co",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4",
        "TE": "trailers"
    }

    def get_blob_service_client_sas():
        account_url = os.environ["blobaccount"]
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url, credential=credential)

        return blob_service_client

    def upload_blob_stream(blob_service_client, container_name, data, file_name):
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
        input_stream = io.BytesIO(json.dumps(data).encode('utf-8'))
        blob_client.upload_blob(input_stream, blob_type="BlockBlob", overwrite=True)
        print(f"Archivo '{file_name}' subido al blob.")

    def make_request(city_name, city_id, rows):
        data = {
            "variables": {
                "rows": rows,
                "params": {
                    "page": 1,
                    "order": 2,
                    "operation_type_id": 2,
                    "property_type_id": [1, 2],
                    "locations": [
                        {
                            "country": [
                                {
                                    "name": "Colombia",
                                    "id": "858656c1-bbb1-4b0d-b569-f61bbdebc8f0",
                                    "slug": "country-48-colombia"
                                }
                            ],
                            "name": city_name,
                            "location_point": {
                                "coordinates": [-75.57786065131165, 6.249816589298594],
                                "type": "point"
                            },
                            "id": city_id,
                            "type": "CITY",
                            "slug": [f"city-colombia-05-{city_id}"],
                            "estate": {
                                "name": "Antioquia",
                                "id": "2d63ee80-421b-488f-992a-0e07a3264c3e",
                                "slug": "state-colombia-05-antioquia"
                            },
                            "label": f"{city_name}<br/><span style='font-size:12px'>Antioquia</span>"
                        }
                    ],
                    "currencyID": 4,
                    "m2Currency": 4,
                    "bedrooms": [2]
                },
                "page": 1,
                "source": 10
            },
            "query": ""
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la solicitud: {response.status_code}")
            print(response.text)
            return None

    def extract_fields(data):
        extracted_data = []
        current_datetime = datetime.now().strftime("%Y-%m-%d")

        for hit in data['hits']['hits']:
            source = hit['_source']['listing']
            entry = {
                "address": source.get('address'),
                "bathrooms": source.get('technicalSheet')[3].get('value'),
                "bedrooms": source.get('technicalSheet')[7].get('value'),
                "code": source.get('code'),
                "description": source.get('description'),
                "facilities": ", ".join([facility['name'] for facility in source.get('facilities', []) if facility.get('name')]),
                "id": source.get('id'),
                "latitude": source.get('latitude'),
                "longitude": source.get('longitude'),
                "location": source.get('locations').get('location_main').get('name'),
                "city": source.get('locations').get('city')[0].get('name'),
                "commune": source.get('locations').get('commune')[0].get('name') if source.get('locations').get('commune') else None,
                "m2": source.get('m2'),
                "owner_name": source.get('owner').get('name'),
                "owner_type": source.get('owner').get('type'),
                "price": source.get('price').get('amount'),
                "admin_included": source.get('price').get('admin_included'),
                "stratum": source.get('technicalSheet')[0].get('value'),
                "title": source.get('title'),
                "updated_at": source.get('updated_at'),
                "query_datetime": current_datetime
            }
            extracted_data.append(entry)
        return extracted_data

    all_extracted_data = []

    def fetch_data_for_city(city_name, city_id):
        # Obtener el número total de registros
        initial_response = make_request(city_name, city_id, 1)

        if initial_response:
            total_records = initial_response['hits']['total']['value']
            print(f"Total de registros para {city_name}: {total_records}")

            # Obtener todos los registros
            final_response = make_request(city_name, city_id, total_records)

            if final_response:
                extracted_data = extract_fields(final_response)
                all_extracted_data.extend(extracted_data)  # Añadir datos de la ciudad a la lista general

    # Ejecutar para cada ciudad
    for city_name, city_id in cities.items():
        fetch_data_for_city(city_name, city_id)

    # Subir un solo archivo JSON con todos los datos combinados
    current_datetime = datetime.now().strftime("%y%m%d")
    file_name = f"{current_datetime}_fincaraiz.json"
    blob_service_client = get_blob_service_client_sas()
    upload_blob_stream(blob_service_client, "json", all_extracted_data, file_name)
    print("fetched data")

#fetch_and_upload_city_data()
