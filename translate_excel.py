import requests
import pandas as pd
import numpy as np  # Import numpy directly

# Define the API key, endpoint, and bearer token
API_ENDPOINT = "https://api.gatewaydigital.ai/v1/completion-messages"

def translate_names_in_excel(input_file, output_file, source_column, target_language):
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f'Error reading Excel file: {str(e)}')
        return

    if source_column not in df.columns:
        print(f'Excel file must contain a "{source_column}" column')
        return

    # Clean the DataFrame
    df[source_column].replace([np.inf, -np.inf], np.nan, inplace=True)  # Use numpy directly
    df[source_column].fillna('', inplace=True)
    df[source_column] = df[source_column].astype(str)
    
    translated_names = []
    
    for name in df[source_column]:
        if not name.strip():
            translated_names.append('')
            continue

        print(name)
        print(type(name))
        print(target_language)
        payload = {
            "inputs": {
                "query": name,
                "Target_language": target_language
            },
            "response_mode": "blocking",
            "user": "0508d53a-8ae2-4d2c-8574-134ead1d1153"
        }
        headers = {
            'Authorization': 'Bearer app-A5woE3MDKmtsuugsjy0s75hr',
            'Content-Type': 'application/json'
        }
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        print(response.status_code)

        if response.status_code == 200:
            result = response.json()
            translated_text = result.get('answer', '')
            translated_names.append(translated_text)
        else:
            print(f'Failed to translate "{name}". Status code: {response.status_code}, Response: {response.text}')
            translated_names.append(None)
    
    df[f'Translated_{source_column}'] = translated_names
    df.to_excel(output_file, index=False)
    print(f'Translated names saved to {output_file}')

if __name__ == '__main__':
    input_file = '/home/pritikuchhadiya/Downloads/excel_translate/Lebanon_Data.xlsx'  # Replace with your input file path
    output_file = 'translated_output_labanon.xlsx'  # Replace with your output file path
    source_column = 'english name'  # Replace with the name of the column to translate
    target_language = 'arabic'  # Replace with the target language

    translate_names_in_excel(input_file, output_file, source_column, target_language)
