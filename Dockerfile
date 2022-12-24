FROM python:3
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
RUN wget https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip && unzip chromedriver_linux64.zip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable
COPY . /code/
RUN ["python","django_wcapp/django_wcapp/manage.py","migrate"]
CMD ["python", "main.py"]