# Usa uma imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app/

# Cria um ambiente virtual e instala dependências
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# Define a variável de ambiente para evitar buffering no output do Python
ENV PYTHONUNBUFFERED=1

# Expõe a porta (se necessário, ajuste conforme sua aplicação)
EXPOSE 8080

# Define o comando padrão para rodar a aplicação
CMD ["/opt/venv/bin/python", "index.py"]
