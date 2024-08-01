FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]