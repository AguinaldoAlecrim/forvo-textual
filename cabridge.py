import requests
from bs4 import BeautifulSoup

class Dictionary:
    def getDictionary(self, APalavra: str) -> dict:
        """
        Busca a tradução de inglês para português de uma palavra no site do Cambridge Dictionary.

        Args:
            APalavra (str): A palavra a ser buscada.

        Returns:
            dict: Um dicionário contendo as seguintes chaves:
                - consulta: A palavra que foi buscada.
                - traducao: A tradução de inglês para português da palavra.
                - explicacao: Uma lista de strings, cada uma contendo uma definição da palavra.
                - explitrad: Uma lista de strings, cada uma contendo uma tradução de uma definição.
                - example: Uma lista de strings, cada uma contendo uma frase de exemplo usando a palavra.

                Se ocorrer um erro durante a busca, todos os valores no dicionário serão listas vazias.
        """
        jsonResultante = {}
        try:
            header = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }
            url = 'https://dictionary.cambridge.org/pt/dicionario/ingles-portugues/' + APalavra
            htmlResult = requests.get(url, headers=header)
            soup = BeautifulSoup(htmlResult.content, 'html.parser')
            
            jsonResultante['consulta'] = soup.find('span', class_='hw dhw').get_text()
            jsonResultante['explicacao'] = [elem.get_text().strip() for elem in soup.find_all('div', class_='def ddef_d db')]
            jsonResultante['explitrad'] = list(set([elem.get_text().strip() for elem in soup.find_all('span', class_='trans dtrans dtrans-se')]))
            jsonResultante['example'] = [elem.get_text().strip() for elem in soup.find_all('span', class_='eg deg')]
            
            return jsonResultante
        except Exception as e:
            jsonResultante['consulta'] = []
            jsonResultante['explicacao'] = []
            jsonResultante['explitrad'] = []
            jsonResultante['example'] = []
            jsonResultante['error'] = [str(e)]
            return jsonResultante