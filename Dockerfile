FROM python:3.11

#RUN mkdir /app
WORKDIR /app
ADD /app/ .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app/example_app.properties /app/config/app.properties

EXPOSE 5000
CMD ["python", "/app/main.py"]