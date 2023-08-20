import requests
from bs4 import BeautifulSoup
import re
import base64

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from io import BytesIO



class Forvo:
    def __init__(self):
        self.defaultProtocol = 'https:'
        self._AUDIO_HTTP_HOST='audio12.forvo.com'
        self.PHPSESSID='3caua289gurjfrvqbn1btjne76'

    def _get(self, expression) -> str:
        """
        Faz uma requisição HTTP para a página do Forvo e obtém o conteúdo HTML 
        associado à busca de uma expressão no idioma inglês (EUA).

        Args:
            expression (str): A expressão que será buscada no Forvo.

        Returns:
            str: O conteúdo HTML da página do Forvo associado à busca da expressão.

        Raises:
            None.

        Example:
            >>> html_content = get('hello')
            >>> print(html_content[:200])  # Imprime os primeiros 200 caracteres do HTML.
            <!DOCTYPE html>
            <html class="no-js" lang="en">
            <head>
            <title>Forvo: the pronunciation dictionary. All the words in the world pronounced by native speakers</title>
            <meta http-equiv="X-UA-Compatible" content="I
        """
        url = f"https://forvo.com/search/{expression}/en_usa/"

        # Informações da requisição (se houver) podem ser atualizadas conforme necessário
        payload = {}
        headers = {
            'Cookie': f'PHPSESSID={self.PHPSESSID}',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        # Faz a requisição HTTP para a página do Forvo
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text
    
    def _getDadosOfAudios(self,html_content: str) -> str:
        """
        Obtém o conteúdo do atributo 'onclick' de uma div com a classe 'play'
        a partir do conteúdo HTML fornecido.

        Args:
            html_content (str): O conteúdo HTML da página que será analisado.

        Returns:
            str: O conteúdo do atributo 'onclick' da div com a classe 'play',
                ou uma string vazia se a div não for encontrada.

        Example:
            >>> html_content = "<div class='play' onclick='funcao1();'>...</div>"
            >>> conteudo_onclick = getDadosOfAudios(html_content)
            >>> print(conteudo_onclick)
            "funcao1();"
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Utilizando o método find para obter o primeiro elemento div com a classe "play"
        elemento_div = soup.find('div', class_='play')

        # Verificando se o elemento div foi encontrado antes de acessar o atributo onclick
        if elemento_div:
            # Acessando o conteúdo do atributo onclick
            conteudo_onclick = elemento_div.get('onclick')
        else:
            conteudo_onclick = ""

        return conteudo_onclick



    def _getParameters(self, txtFuncPlayer: str) -> list:
        """
        Extrai os parâmetros da função 'Play' a partir de uma string.

        Args:
            txtFuncPlayer (str): A string que contém a chamada da função 'Play'
                                com seus parâmetros.

        Returns:
            list: Uma lista contendo osprint('Palavra não encontrada\nPressione enter para voltar.')
            input() parâmetros extraídos da função 'Play'
                sem as aspas duplicadas.

        Example:
            >>> txtFuncPlayer = "Play(3173525,'OTQ0MzUzNi8zOS85NDQzNTM2XzM5XzI1MjcubXAz','OTQ0MzUzNi8zOS85NDQzNTM2XzM5XzI1Mjcub2dn',false,'by8xL28xXzk0NDM1MzZfMzlfMjUyNy5tcDM=','by8xL28xXzk0NDM1MzZfMzlfMjUyNy5vZ2c=','h','love','English');return false;"
            >>> parametros = getParameters(txtFuncPlayer)
            >>> print(parametros)
            ['3173525', 'OTQ0MzUzNi8zOS85NDQzNTM2XzM5XzI1MjcubXAz', 'OTQ0MzUzNi8zOS85NDQzNTM2XzM5XzI1Mjcub2dn', 'false', 'by8xL28xXzk0NDM1MzZfMzlfMjUyNy5tcDM=', 'by8xL28xXzk0NDM1MzZfMzlfMjUyNy5vZ2c=', 'h', 'love', 'English']
        """
        # Usando expressão regular para extrair os parâmetros da função 'Play'
        padrao = r"Play\((.*?)\);"
        try:
            # Encontrando todos os matches com a expressão regular
            matches = re.findall(padrao, txtFuncPlayer)

            # Se houver matches, eles serão colocados em uma lista chamada "parametros"
            parametros = matches[0].split(',')

            # Removendo as aspas duplicadas dos parâmetros
            parametros_sem_aspas = [self._strip_quotes(parametro) for parametro in parametros]

            return parametros_sem_aspas
        except:
            return []

    def _strip_quotes(self, s: str) -> str:
        """
        Remove as aspas no início e no fim de uma string, se existirem.

        Args:
            s (str): A string da qual as aspas serão removidas.

        Returns:
            str: A string sem as aspas no início e no fim.

        Example:
            >>> s = "'OTQ0MzUzNi8zOS85NDQzNTM2XzM5XzI1MjcubXAz'"
            >>> resultado = _strip_quotes(s)
            >>> print(resultado)
            OTQ0MzUzNi8zOS85NDQzNTM2XzM5XzI1MjcubXAz
        """
        if s.startswith("'") and s.endswith("'"):
            return s[1:-1]
        return s


    def _base64_decode(self, textInBase64:str) -> str:
        # Decodificando a string em Base64
        string_decodificada = base64.b64decode(textInBase64).decode('utf-8')

        return string_decodificada

    def _getUrlMp3(self,fPath):
        return self.defaultProtocol + "//" + self._AUDIO_HTTP_HOST + "/audios/mp3/" + fPath

    def _reproduzir_audio(self, url: str) -> bytes:
        """
        Reproduz o áudio a partir de uma URL para um arquivo MP3 utilizando o Pygame.

        Args:
            url (str): A URL para o arquivo MP3 a ser reproduzido.

        Returns:
            bytes: Os dados de áudio em formato bytes, referentes ao conteúdo do arquivo MP3.

        Raises:
            Exception: Se ocorrer algum erro durante a reprodução ou requisição do áudio.

        Example:
            >>> # Crie uma instância da classe que contém o método _reproduzir_audio
            >>> minha_classe = MinhaClasse()
            >>> url = "https://example.com/audio.mp3"
            >>> # Chame o método _reproduzir_audio para reproduzir o áudio a partir da URL
            >>> audio_data = minha_classe._reproduzir_audio(url)
            >>> # Você pode chamar o método novamente para reproduzir o áudio novamente
            >>> minha_classe._reproduzir_audio(url)
        """
        try:
            # Criação do dicionário de headers com o valor do PHPSESSID e o User-Agent
            headers = {
                'Cookie': f'PHPSESSID={self.PHPSESSID}',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }

            # Faz uma requisição HTTP para obter o conteúdo do arquivo MP3
            response = requests.get(url, headers=headers)

            # Verifica se a requisição foi bem-sucedida (status code 200)
            if response.status_code == 200:
                # Inicializa a biblioteca pygame
                pygame.mixer.init()

                # Carrega o conteúdo do áudio no mixer do pygame
                audio_data = BytesIO(response.content)
                pygame.mixer.music.load(audio_data)

                # Reproduz o áudio
                pygame.mixer.music.play()

                # Aguarda até que a reprodução seja concluída
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                # Encerra a biblioteca pygame
                pygame.mixer.quit()

                # Retorna os dados de áudio em formato bytes
                return response.content

            else:
                print(f"Erro ao acessar a URL: {response.status_code}")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            raise e

        return None

        
    def repetir_audio(self, lstaudio):
        """
        Reproduz o áudio várias vezes a partir dos dados de áudio fornecidos.

        Args:
            audio_data (BytesIO): Os dados de áudio em formato BytesIO.
            

        Returns:
            None.
        """
        try:
            audio_data_copy = BytesIO(lstaudio)
            # Inicializa a biblioteca pygame
            pygame.mixer.init()

            # Carrega o conteúdo do áudio no mixer do pygame
            pygame.mixer.music.load(audio_data_copy)

            # Reproduz o áudio
            pygame.mixer.music.play()

            # Aguarda até que a reprodução seja concluída
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Encerra a biblioteca pygame
            pygame.mixer.quit()

        except Exception as e:
            pygame.mixer.quit()
            print(f"Ocorreu um erro: {e}")


    def play(self, word: str):
        htmlcode = self._get(word)

        if htmlcode == None: return False

        dadosOfAudios = self._getDadosOfAudios(htmlcode)
        parameters = self._getParameters(dadosOfAudios)
        if len(parameters) > 0:
            base64Code = self._base64_decode(parameters[4])            
            ret = self._reproduzir_audio(self._getUrlMp3(base64Code))
            if ret == None:
                return False

            return ret
        return False

            