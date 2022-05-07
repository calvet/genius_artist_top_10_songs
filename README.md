# genius_artist_top_10_songs
Integração com a API do Genius para capturar as top 10 músicas mais tocadas de algum artista.
Feito com Flask, Redis e DynamoDB.

### Requisitos:
- Python 3+
- Redis Server 3.0
- DynamoDB Server (ou instância rodando na AWS)
- Conta no Genius API

### Compatibilidade:
Linux e Windows

### Como configurar o ambiente:
• Configure o arquivo ".env" na pasta raíz do projeto com as seguintes informações:
```
FLASK_ENV=production
DEBUG=False

GENIUS_ACCESS_TOKEN= ** GENIUS API ACCES TOKEN **

REDIS_HOST=** REDIS HOST ADDRESS **
REDIS_PORT=** REDIS PORT NUMBER **
REDIS_DAYS_EXPIRE=7

AWS_ACCESS_KEY_ID=** AWS ACCESS KEY **
AWS_SECRET_ACCESS_KEY=** AWS SECRET ACCESS KEY **
```

• Após configurar o arquivo ".env", você precisará instalar os requisitos do projeto com o seguinte comando:
```pip install -r requirements.txt```

• Pronto! Configurado. Se tudo deucerto nos passos anteriores, agora você só precisa abrir o "Command Prompt" ou "bash" e rodar o seguinte comando na pasta:
```flask run```
ou simplesmente:
```python -m app.py```

### Como consultar os dados do Artista na API:
- Você precisa fazer uma requisição com o método "GET" para a url a seguir:
```http://127.0.0.1:5000/api/v1/get_artist_top_songs/NOME_DO_ARTISTA```
(substitua NOME_DO_ARTISTA pelo nome do seu artista favorito)

### Retorno dos dados da API:
- Se tudo der certo com sua requisição, você receberá o seguinte retorno (exemplo):
```
{
  "artist_name": "David Guetta",
  "message": "Foram encontrados as top 10 musicas deste artista!",
  "songs_list": [
          "2U by David Guetta (Ft. Justin Bieber)",
          "One Last Time by Ariana Grande",
          "Lovesick Girls by BLACKPINK",
          "So Far Away by Martin Garrix & David Guetta (Ft. Jamie Scott & Romy Dya)","Titanium by David Guetta (Ft. Sia)",
          "Hey Mama by David Guetta (Ft. Afrojack, Bebe Rexha & Nicki Minaj)",
          "Goodbye by Jason Derulo & David Guetta (Ft. Nicki Minaj & Willy William)",
          "Say My Name by David Guetta, Bebe Rexha & J Balvin",
          "I Gotta Feeling by Black Eyed Peas",
          "Flames by David Guetta & Sia"
  ],
  "status":"success"
}
```

~ opcionalmente: você pode adicionar no parâmetro da URL a seguinte flag "?cache=False", assim evitará de trazer dados em cache ~


