from typing import Any, Callable
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from enum import StrEnum
from src.large_language_model.base_tools import BaseTool

class ImageGenerationModel(StrEnum):
    """
    Enum para os modelos de geração de imagens disponíveis.
    """
    GEMINI_2_0_FLASH = 'gemini-2.0-flash-preview-image-generation'

    def __str__(self):
        return self.value


#https://ai.google.dev/gemini-api/docs/image-generation?hl=pt-br
class ImageGenerationTool(BaseTool):
    """
    Classe para gerar imagens usando o modelo Gemini 2.0 Flash.
    """
    def __init__(self, api_key: str or None = None, *args, **kwargs):


        api_key = api_key or os.getenv("GEMINI_API")

        if not api_key:
            raise ValueError(
                "API key must be provided either as an argument or through the GEMINI_API environment variable.")

        self.client = genai.Client(api_key=api_key)
        super().__init__()

    @property
    def function_declaration(self) -> Callable[..., Any]:
        return self.generate_image


    def generate_image(self, prompt: str) -> bytes:
        """
        Generate an image for a given prompt.

        The prompt must be written in English and should be as detailed as possible to achieve the best results.
        It must start with "Generate an image".
        """

        raise NotImplementedError("Criar um cache e salvar a imagem gerada, senão o modelo vai ficar extramamente lento")

        if not prompt or prompt == 'prompt':
            raise ValueError("Prompt must not be empty.")


        response = self.client.models.generate_content(
            model=ImageGenerationModel.GEMINI_2_0_FLASH,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(f"Texto ignorado do gerador de imagens: {part.text}")
            elif part.inline_data is not None:
                return part.inline_data.data

        raise ValueError("No image data found in the response. Please check the prompt and try again.")

    def call_chat_display(self) -> str:
        return "Gerando imagem com o modelo Gemini 2.0 Flash..."

    def call_result_display(self, result: Any) -> Image:

        if isinstance(result, bytes):
            return Image.open(BytesIO(result))

        if isinstance(result, dict):
            return Image.open(BytesIO(result['output']))

        raise ValueError("Result must be of type bytes or dict containing 'output' key with image data.")


    def get_result_as_part(self, result: Any) -> types.Part:
        return types.Part.from_function_response(
            name=self.function_name,
            response={
                    'output': result,
                }
        )


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('../../.env')

    client = genai.Client(api_key=os.getenv("GEMINI_API"))

    contents = ('Hi, can you create a 3d rendered image of a pig '
                'with wings and a top hat flying over a happy '
                'futuristic scifi city with lots of greenery, holding a sign with the writting "Hello World"?')

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
          response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
      if part.text is not None:
        print(f"Texto ignorado do gerador de imagens: {part.text}")
      elif part.inline_data is not None:
        image = Image.open(BytesIO((part.inline_data.data)))
        image.save('gemini-native-image.png')
        image.show()
