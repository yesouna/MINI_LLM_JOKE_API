from dotenv import dotenv_values
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import HTTPException
from pydantic import BaseModel

ENV_ACCESS=dotenv_values()
ACCESS_TOKEN = ENV_ACCESS['ACCESS_TOKEN']
MODEL_NAME = ENV_ACCESS['MODEL_NAME']
MAX_RESPONSE_TOKENS =  ENV_ACCESS['MAX_RESPONSE_TOKENS']
MIN_PROMPT_WORDS = ENV_ACCESS['MIN_PROMPT_WORDS']


# laod model and tokenizer once at start of fastapi server and keep as long as running
@asynccontextmanager
async def load_model_tokenizer(app: FastAPI):

    # cpu only no cuda gpu in my machine
    global  device
    device = torch.device("cpu") 
    
    global tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=ACCESS_TOKEN)
    except Exception as e:
        tokenizer = None
        error_msg=f"Fail loading tokenizer: {tokenizer}, Error {e}"
        print(error_msg) # python logging with # levels or fastapi own logger
        raise ValueError(error_msg) 

    global model
    try:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            token=ACCESS_TOKEN,
            torch_dtype= torch.float32,
            device_map="cpu"
        )
    except Exception as e:
        model=None
        error_msg=f"Fail loading tokenizer: {model}, Error {e}"
        print(error_msg) 
        raise ValueError(error_msg) 

    if tokenizer and model:
        succes_msg=f"Sucess loaded tokenizer: {tokenizer}, and model {model}"
        print(succes_msg) 
        
    yield

# start load tokenzier and model 
app = FastAPI(lifespan=load_model_tokenizer)



# post request "/generate" with prompt: in body and returns a response:
# request format
class FormatRequest(BaseModel):
    prompt: str
    
# response format
class FormatResponse(BaseModel):
    response: str

@app.post("/generate", response_model=FormatResponse)
async def generate_text(request: FormatRequest):
    if not model or not tokenizer:
        raise HTTPException(status_code=500, detail="Fail Model or tokenizer not loaded")
    
    # check prompt none, empty, non empty only spaces, or very short prompt
    if not request.prompt or not request.prompt.strip() or  len(request.prompt.split())<=int(MIN_PROMPT_WORDS):
        raise HTTPException(
            status_code=400,
            detail="Retry! empty or very short prompt"
        )
    try:
        # Tokenize input prompt
        inputs = tokenizer(request.prompt, return_tensors="pt").to(device)
        
        """
        # Generate inference using hugging face generate, still pytorch underneath 
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=int(MAX_RESPONSE_TOKENS), 
            do_sample=True,
            temperature=0.7,
            top_p=0.8
        )
        """      
        # generate inference using pytorch 
        outputs = inputs.input_ids.clone()  

        # Generation loop
        for _ in range(int(MAX_RESPONSE_TOKENS)):
            # Forward pass (get next-token logits)
            with torch.no_grad():
                logits = model(outputs).logits[:, -1, :]  # Get last token logits

            # similar to as in hf temperature =0.7
            logits = logits / 0.7
            probs = torch.softmax(logits, dim=-1)

            # similar to as in hf do_sample=True, to enable pobabilistic sampling to ramdomly sample from pobable next tokens
            # and we limit sampling to small set of tokens with cumulative probability >=80%
            # Top-p =0.8
            sorted_probs, sorted_indices = torch.sort(probs, descending=True)
            cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
            sorted_indices_to_remove = cumulative_probs > 0.8
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0  # Keep at least one token
            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            probs[:, indices_to_remove] = 0  # Zero out low-probability tokens

            # Sample next token
            next_token = torch.multinomial(probs, num_samples=1)

            # Append to output
            outputs = torch.cat([outputs, next_token], dim=-1)

            # stop ifat end of sequence token
            if next_token.item() == tokenizer.eos_token_id:
                break
        

        # Decode and clean response
        response_text = tokenizer.decode(outputs[0], clean_up_tokenization_spaces=True, skip_special_tokens=True)
        special_chars= ["\\n","\n", "\n1", "\n2","\n3", "\\", "\""]
        for sp_ch in special_chars:
            response_text = response_text.replace(sp_ch, ' ') 
        response_text=' '.join(response_text.split()).strip()

        # Remove the input prompt from the response if it's included
        if response_text.startswith(request.prompt):
            response_text = response_text[len(request.prompt):].strip()
        
        return {"response": response_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fail generating response to prompt: {str(e)}")
