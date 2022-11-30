FROM python:3.8.5

RUN apt-get update
RUN apt-get install wkhtmltopdf -y
WORKDIR /app
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
COPY ./requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 --use-deprecated=legacy-resolver install -r requirements.txt
COPY . .
CMD ["python","main.py"]
