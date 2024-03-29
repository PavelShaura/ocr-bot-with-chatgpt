import logging
from typing import Any, Dict

import g4f

data: Dict[int, Dict[str, Any]] = {
    1: {
        "model": "gpt-3.5-turbo",
        "provider": g4f.Provider.FlowGpt
    },
    2: {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "provider": g4f.Provider.HuggingChat,
    },
    3: {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "provider": g4f.Provider.HuggingFace,
    },
    4: {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "provider": g4f.Provider.HuggingFace,
    },
    5: {
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "provider": g4f.Provider.HuggingChat,
    },
    6: {
        "model": "openchat/openchat_3.5",
        "provider": g4f.Provider.HuggingChat
    },
}


async def chat_completion(prompt: str, model: str, provider: g4f.Provider) -> Any:
    """
    Запрашивает текст ответа на промт от модели ИИ.

    :param prompt: Текст, который будет использован в качестве начального запроса.
    :type prompt: str
    :param model: Название модели ИИ.
    :type model: str
    :param provider: Поставщик модели ИИ.
    :type provider: g4f.Provider
    :return: Ответ от модели ИИ.
    :rtype: Any
    """
    response = await g4f.ChatCompletion.create_async(
        model=model, messages=[{"role": "user", "content": prompt}], provider=provider
    )
    return response


async def try_models(prompt_text: str) -> Any:
    """
    Попытка запросить текст ответа у различных моделей ИИ.

    :param prompt_text: Текст, который будет использован в качестве начального запроса.
    :type prompt_text: str
    :return: Ответ от модели ИИ.
    :rtype: Any
    """
    for key, item in data.items():
        try:
            provider_name = str(item["provider"]).split(".")[2]
            response = await chat_completion(
                prompt_text, model=item["model"], provider=item["provider"]
            )
            logging.info(
                f"Response from the AI for model {item['model']}, provider {provider_name}"
            )
            return response
        except Exception as e:
            logging.info(
                f"An error {e}. -> Occurred while requesting a response from the AI for model {item['model']}, provider {item['provider']}"
            )

    raise Exception("All models failed to generate a response")
