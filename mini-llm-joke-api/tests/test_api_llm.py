from dotenv import dotenv_values
import requests


ENV_ACCESS=dotenv_values()
API_URL = ENV_ACCESS['API_URL']
MAX_RESPONSE_TOKENS=ENV_ACCESS['MAX_RESPONSE_TOKENS']



# validty of values with correct "prompt" key
def test_prompts_values():
    
    test_cases = [("",400),("    ",400), ("joke about",400), ("tell me a joke about cats",200)]
    
    for prompt, expected_status in test_cases:
        payload = {"prompt": prompt}
        
        response = requests.post(
            f"{API_URL}/generate",
            json=payload
        )
        
        # assert response codes
        assert response.status_code == expected_status, f"Prompt: '{prompt}' got {response.status_code}, expected {expected_status}"
        
        # assert message for # codes
        if expected_status == 400:
            assert "Retry! empty or very short prompt" in response.json().get("detail", "")
        
        # just for simplicity tokens=words response max size
        if expected_status == 200:
            cnt_wrds=len(response.json().get("response", "").split()) if response.json().get("response", "") else 0
            assert cnt_wrds<=int(MAX_RESPONSE_TOKENS)

# validty of keys with correct values 
def test_prompts_keys():
    # keys for prompts
    test_cases = [("request",400),(" ",400), (" ",400),("PROMPT",400), ("prompt",200)]
    for prompt, expected_status in test_cases:
        payload = {prompt: "tell me a joke about cats"}
        
        response = requests.post(
            f"{API_URL}/generate",
            json=payload
        )
    # assert codes
    assert response.status_code == expected_status, f"Prompt: '{prompt}' got {response.status_code}, expected {expected_status}"



"""
all test passed: pytest test_api_llm.py

======================================================================================= test session starts ========================================================================================
platform darwin -- Python 3.9.23, pytest-8.4.1, pluggy-1.5.0
rootdir: /Users/yassine/Desktop/BOTS/Fujitsu_to_I-HSI/mini-llm-joke-api/tests
plugins: anyio-4.9.0
collected 1 item                                                                                                                                                                                   

test_api_llm.py .                                                                                                                                                                            [100%]

======================================================================================== 1 passed in 45.24s ========================================================================================
(env_fujitsu_mini-llm-joke-api) yassine@Yassines-MacBook-Pro tests % pytest test_api_llm.py
======================================================================================= test session starts ========================================================================================
platform darwin -- Python 3.9.23, pytest-8.4.1, pluggy-1.5.0
rootdir: /Users/yassine/Desktop/BOTS/Fujitsu_to_I-HSI/mini-llm-joke-api/tests
plugins: anyio-4.9.0
collected 2 items                                                                                                                                                                                  

test_api_llm.py ..                                                                                                                                                                           [100%]

=================================================================================== 2 passed in 77.30s (0:01:17) ===================================================================================
======================================================================================== 1 passed in 31.78s =======================================================================================    
"""