import os
import httpx
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from app.handlers import LLMServiceError

load_dotenv()

AZURE_ENDPOINT = 'https://api.kadal.ai/proxy/api/v1/azure'
LM_KEY = os.getenv("LLM_API_KEY")
API_VERSION = "2024-02-15-preview"

if not LM_KEY:
    raise RuntimeError("LLM_API_KEY is missing from environment variables (.env)")
client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_version=API_VERSION,
    api_key=LM_KEY,
    timeout=30.0,
    max_retries=3,
    http_client=httpx.AsyncClient(verify=False) 
)

async def get_chat_completion(messages, model="gpt-4o-mini", temperature=0.7):
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        content = response.choices[0].message.content
        if not content:
            raise LLMServiceError("LLM returned an empty response.")
        return content
    except Exception as e:
        error_msg = f"Kadal API Error: {str(e)}"
        raise LLMServiceError(error_msg)