import asyncio
import aiohttp
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_chat():
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        payload = {
            "message": "¿Qué es el teorema de Pitágoras?"
        }
        
        logger.debug(f"Sending request to chat endpoint")
        try:
            async with session.post(
                'http://127.0.0.1:8000/chat',
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            ) as response:
                text = await response.text()
                logger.debug(f"Raw response: {text}")
                
                if response.status == 200:
                    try:
                        result = json.loads(text)
                        logger.info("Success Response:", json.dumps(result, indent=2, ensure_ascii=False))
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON response: {e}")
                else:
                    logger.error(f"Server Error {response.status}: {text}")
                    logger.debug(f"Response headers: {dict(response.headers)}")
                
        except aiohttp.ClientError as e:
            logger.error(f"Connection error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(test_chat())