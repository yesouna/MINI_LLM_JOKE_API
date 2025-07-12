# mini_llm_joke_api
Hi I-HSI

I have not done any of the bonus Features, but I will try tomorrow, if I will have time, to finish a simple UI with Gradio before the interview.

# Comments about Bonus Features (Optional)
- Add a simple frontend (e.g., Streamlit or React) ### I will try to finish a gradio UI tomorrow before the interview
- Dockerize the project ### Dockerfile would be straight forward, RUN conda env create -f env_fujutsu_mini_llm_joke_api.yml and run: SHELL ["conda", "run", "-n", "fujitsu_mini_llm_joke_api", "/bin/bash", "-c"] and expose 8000 port
- Support multiple languages (e.g., English and Mandarin jokes) ### gemma-2b does not support mandarin
- Use Redis or other caching for repeated prompts ### I agree, but repeated exactly same prompt, not similar ones.
- Add API rate limiting or token-based auth ### I agree, FastApi seems to have a built in one with time, on how many requests allowed per duration.
- Use vLLM for high-performance inference (with OpenAI-compatible endpoint) ### I don't have an nvidia gpu, that's why using transformers, vLLM better for highthroughput inference requests with its batch processing while serving local models (not through apis)


