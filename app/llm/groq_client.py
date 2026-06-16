import json
import logging
from typing import Optional, Dict, Any, List
from groq import Groq
from groq import APIError, APIConnectionError, RateLimitError
import time
from app.config.settings import Config

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        if not self.api_key:
            logger.warning("GROQ_API_KEY is not set. LLM features will fail.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
        self.model = Config.GROQ_MODEL

    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        json_mode: bool = False,
        temperature: float = 0.2,
        retries: int = 3
    ) -> Optional[str]:
        """
        Sends a request to Groq and returns the string response.
        Handles rate limits and retries gracefully.
        """
        if not self.client:
            return "Error: Groq client not configured."

        for attempt in range(retries):
            try:
                response_format = {"type": "json_object"} if json_mode else None
                
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    temperature=temperature,
                    response_format=response_format
                )
                
                return chat_completion.choices[0].message.content

            except RateLimitError as e:
                wait_time = 2 ** attempt
                logger.warning(f"Groq rate limit hit. Retrying in {wait_time}s... (Attempt {attempt+1}/{retries})")
                time.sleep(wait_time)
            except (APIError, APIConnectionError) as e:
                logger.error(f"Groq API Error: {str(e)}")
                if attempt == retries - 1:
                    return None
                time.sleep(2 ** attempt)
            except Exception as e:
                logger.exception("Unexpected error calling Groq.")
                return None
                
        logger.error("Groq API failed after all retries.")
        return None

    def stream_response(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7
    ):
        """
        Returns a generator yielding streaming chunks from Groq.
        """
        if not self.client:
            yield "Error: Groq client not configured."
            return

        try:
            stream = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=temperature,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.exception("Streaming error calling Groq.")
            yield "Sorry, I encountered an error while generating a response."

# Singleton instance
groq_client = GroqClient()
