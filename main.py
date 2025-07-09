import json
import time
import requests
import base64
from config import api_key1, secret_key1

# Initialization
class FusionBrainAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        response.raise_for_status()
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        response.raise_for_status()
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']
            attempts -= 1
            time.sleep(delay)
        return None
    
    def sv_img(self, base64_string, filepath):
        try:
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(base64_string[0]))
            print(f"Image successfully saved to {filepath}")
        except Exception as e:
            print(f"Error saving image to {filepath}: {e}")

if __name__ == '__main__':
    api = FusionBrainAPI(
        'https://api-key.fusionbrain.ai/',
        api_key1,
        secret_key1
    )

    prompt = input("Masukkan prompt: ")
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id, images=1)
    files = api.check_generation(uuid)


    if files:
        print("✅ Gambar berhasil dihasilkan dan akan disimpan:")
        for idx, img_base64 in enumerate(files):
            filename = f"gen_img_{idx+1}.png"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(img_base64))
            print(f"- {filename} disimpan.")
    else:
        print("❌ Gagal menghasilkan gambar.")
