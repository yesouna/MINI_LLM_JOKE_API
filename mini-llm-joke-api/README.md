###### mini_llm_joke_api: CPU ONLY VERSION with hf and pytorch | no cuda nor vllm

#### create conda environemnt with yml file
conda env create -f env_mini-llm-joke-api.yml
conda activate env_mini-llm-joke-api



#### change .env 
put ur hg access token: ACCESS_TOKEN = "XXXXX"
If you want to try another model, change env variables model and token accordingly and get access from hf, enable cuda (if you have an nvidia gpu) and change device type to 'cuda' in main.py
#### run under app/
uvicorn main:app --reload


#### run under tests/
pytest test_api_llm.py


