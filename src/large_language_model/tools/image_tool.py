from typing import Any, Callable, Union
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from enum import StrEnum
from src.large_language_model.tipos_base.base_tools import BaseTool
from src.database.models.files_database import Arquivo, TipoArquivoEnum
from datetime import datetime

from src.settings import DEBUG


class ImageGenerationModel(StrEnum):
    """
    Enum para os modelos de geração de imagens disponíveis.
    """
    GEMINI_2_0_FLASH = 'gemini-2.0-flash-preview-image-generation'

    def __str__(self):

        match self:
            case ImageGenerationModel.GEMINI_2_0_FLASH:
                return "Gemini 2.0 Flash"
            case _:
                return self.value


#https://ai.google.dev/gemini-api/docs/image-generation?hl=pt-br
class ImageGenerationTool(BaseTool):
    """
    Classe para gerar imagens usando o modelo Gemini 2.0 Flash.
    """

    generative_model: ImageGenerationModel = ImageGenerationModel.GEMINI_2_0_FLASH

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


    _generated_image_cache: dict[int, Arquivo] = {}

    def generate_image(self, prompt: str) -> dict:
        """
        Generate an image for a given prompt.

        :param prompt: The prompt must be written in English and should be as detailed as possible to achieve the best results.
        It must start with "Generate an image".
        """

        try:

            if not prompt or prompt == 'prompt':
                raise ValueError("Prompt must not be empty.")


            response = self.client.models.generate_content(
                model=self.generative_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )

            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    print(f"Texto ignorado do gerador de imagens: {part.text}")
                elif part.inline_data is not None:

                    buffer = BytesIO()
                    Image.open(BytesIO(part.inline_data.data)).convert("RGB").save(buffer, format="JPEG")
                    jpeg_bytes = buffer.getvalue()
                    now = datetime.now()
                    nome_arquivo = f"{self.generative_model.name}-{now.strftime('%Y%m%d%H%M%S')}.jpeg"


                    # criar instância de Arquivo para armazenar a imagem
                    novo_arquivo = Arquivo(
                        nome=nome_arquivo,
                        tipo=TipoArquivoEnum.jpeg,
                        ultima_atualizacao=now,
                        bytes_arquivo=jpeg_bytes
                    )

                    novo_arquivo.save()
                    self._generated_image_cache[novo_arquivo.id] = novo_arquivo

                    return {
                        'output': {
                            'info': 'The image has been generated successfully and the user can already view it in the chat.',
                            'id': novo_arquivo.id,
                        }
                    }

            raise ValueError("No image data found in the response. Please check the prompt and try again.")
        except Exception as e:
            if DEBUG:
                raise e

            return {
                'error': str(e)
            }

    def call_chat_display(self) -> str:
        return f"Gerando imagem com o modelo {str(self.generative_model)}..."

    def call_result_display(self, result: dict) -> Union[str, Image]:

        if 'error' in result:
            return 'Erro ao gerar imagem: ' + result['error']

        image_id = result.get('output', {}).get('id')

        if image_id is None:
            return 'Erro: ID da imagem não encontrado no resultado.'

        if image_id in self._generated_image_cache:
            arquivo = self._generated_image_cache[image_id]
            image = Image.open(BytesIO(arquivo.bytes_arquivo))
            return image

        arquivo = Arquivo.get_from_id(image_id)

        if arquivo is None:
            return 'Erro: Arquivo não encontrado na base de dados.'

        self._generated_image_cache[image_id] = arquivo
        image = Image.open(BytesIO(arquivo.bytes_arquivo))
        return image

    def get_result_as_part(self, result: dict) -> types.Part:
        return types.Part.from_function_response(
            name=self.function_name,
            response=result
        )


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('../../../.env')

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
