###### mini_llm_joke_api: CPU ONLY VERSION with hf and pytorch | no cuda nor vllm

#### create conda environemnt with yml file
conda env create -f env_fujutsu_mini_llm_joke_api.yml
conda activate env_fujitsu_mini-llm-joke-api

[plz note that conda env yml file has more packages for gradio UI and speech transcription, for a UI part that I did not finish yet]


#### change .env 
put ur hg access token: ACCESS_TOKEN = "XXXXX"
If you want to try another model, change env variables model and token accordingly and get access from hf, enable cuda (if you have an nvidia gpu) and change device type to 'cuda' in main.py
#### run under app/
uvicorn main:app --reload


#### run under tests/
pytest test_api_llm.py


