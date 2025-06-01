from datetime import datetime
from src.large_language_model.tipos_base.base_tools import BaseTool
from src.database.models.posts import PostRedeSocial
from src.database.tipos_base.database import Database

class SavePostTool(BaseTool):

    @property
    def function_declaration(self):
        return self.save_post_to_database

    def save_post_to_database(self,
                              post_content: str,
                              file_id: int | None = None,
                              ) -> dict:
        """
        Save a post to the database.
        :param post_content: The content of the post to be saved.
        :param file_id: Optional ID of an attached file. Ex: image, video, etc.
        :return: A dictionary with the status of the operation.
        """

        try:

            with Database.get_session() as session:
                post = PostRedeSocial(
                    conteudo=post_content,
                    anexo_id=file_id,
                    ultima_atualizacao=datetime.now())
                session.add(post)
                session.commit()
                return {
                        'output': {
                            'info': 'Post saved successfully',
                            'post_id': post.id,
                        }
                    }
        except Exception as e:
            return {
                'error': str(e)
            }

    def call_chat_display(self) -> str:
        return "Salvando post na base de dados..."

    def call_result_display(self, result: dict) -> str:
        if 'error' in result:
            return 'Erro ao salvar post: ' + result['error']

        post_id = result.get('output', {}).get('post_id')

        if post_id is None:
            return 'Erro: ID do post não encontrado no resultado.'

        return f"Post salvo com sucesso! ID do post: {post_id}"