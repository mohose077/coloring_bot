import requests
from config import REPLICATE_API_TOKEN

def generate_coloring_image(prompt: str) -> str:
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "version": "db21e45b02e0192b6f4f2a239fa7942a220232545f8704b35766c1803e5b1c6b",  # Stable Diffusion 1.5
        "input": {
            "prompt": prompt + ", black and white line art, coloring book style, simple drawing, high contrast, no background",
            "num_outputs": 1,
            "width": 512,
            "height": 512
        }
    }

    response = requests.post(url, headers=headers, json=data)
    prediction = response.json()

    # Чекаємо завершення генерації
    get_url = prediction["urls"]["get"]
    status = prediction["status"]

    while status != "succeeded":
        r = requests.get(get_url, headers=headers)
        prediction = r.json()
        status = prediction["status"]

    return prediction["output"][0]
