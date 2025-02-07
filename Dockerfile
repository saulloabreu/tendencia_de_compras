# Usa uma imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app/

# Atualiza o gerenciador de pacotes e instala dependências do sistema
RUN apt-get update && apt-get install -y python3-venv

# Cria o ambiente virtual e instala dependências
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip \
    && /opt/venv/bin/python -m pip install -r requirements.txt

# Define a variável de ambiente para evitar buffering no output do Python
ENV PYTHONUNBUFFERED=1

# Expõe a porta (ajuste conforme necessário)
EXPOSE 8080

# Define o comando padrão para rodar a aplicação
CMD ["/opt/venv/bin/python", "index.py"]
