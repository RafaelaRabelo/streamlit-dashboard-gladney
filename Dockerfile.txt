# Usar uma imagem oficial do Python
FROM python:3.10-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar tudo do seu projeto para dentro do container
COPY . /app

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta padrão do Streamlit
EXPOSE 8501

# Rodar o Streamlit
CMD ["streamlit", "run", "test_looker.py", "--server.port=8501", "--server.enableCORS=false"]
