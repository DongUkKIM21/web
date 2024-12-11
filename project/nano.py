import urllib.parse
import requests
import xml.etree.ElementTree as ET
import json  # JSON 변환 및 파일 저장용

# Decode service key
serviceKey = "AWYZG9TEGHektwLX%2BZlhJbUrf6456wetDNJ0yN0X7Je8g4NyTvx9REDsYRsFEU5WAvuSjFnSX9Lyp9LUvESpfg%3D%3D"
decoded_key = urllib.parse.unquote(serviceKey)
print(decoded_key)

# Set up service URL
service_url = "https://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo?serviceKey=AWYZG9TEGHektwLX%2BZlhJbUrf6456wetDNJ0yN0X7Je8g4NyTvx9REDsYRsFEU5WAvuSjFnSX9Lyp9LUvESpfg%3D%3D&returnType=xml&numOfRows=100&pageNo=1&year=2024&itemCode=PM10"

# Set parameters for request
params = {
    "ServiceKey": decoded_key,
    "pageNo": "1",
    "numOfRows": "100",
    "year": "2024",
    "itemCode": "PM10"
}

# Send GET request
resp = requests.get(service_url, params=params)
root = ET.fromstring(resp.content)

# Filter only items related to "부산"
items = []
for element in root.iter('item'):
    district_name = element.find('districtName')
    
    # Ensure that district_name exists and contains '부산'
    if district_name is not None and '부산' in district_name.text:
        item = {
            'dataDate': element.find('dataDate').text if element.find('dataDate') is not None else None,
            'itemCode': element.find('itemCode').text if element.find('itemCode') is not None else None,
            'districtName': district_name.text,
            'moveName': element.find('moveName').text if element.find('moveName') is not None else None,
            'issueGbn': element.find('issueGbn').text if element.find('issueGbn') is not None else None,
            'issueDate': element.find('issueDate').text if element.find('issueDate') is not None else None,
        }
        items.append(item)

# Wrap the filtered data under the key 'Cdust'
output_data = {
    "Cdust": items
}

# Output only filtered items
for item in items:
    print(item)

# Save the extracted data as JSON
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)

print("Filtered data has been saved to 'output.json'")
