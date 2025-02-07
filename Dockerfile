# Usar a imagem oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app/

# Instalar as dependências do projeto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expor a porta em que o Dash irá rodar
EXPOSE 8050

# Definir o comando para rodar o app
CMD ["python", "index.py"]
