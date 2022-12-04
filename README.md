# wcscrapper
This is a project that combines data engineering (extract-transform-load), a backend powered by Django and a frontend using AJAX

[Project Preview](https://i.gyazo.com/b7303a26e96d60a7c95cdf08c56dc313.png)

This project aims at representing an ETL for 2022 Male World Cup results. 

When run, it uses a webpage to retrieve all the matches data in a very comfortable UI.

Additionally, it uses Selenium and BeautifulSoup to obtain repeatedly data from a website.

# Get started

1. Download the chromium driver for the scheduled scrapping script
2. Save the chromium driver inside ``web_scrapping`` folder
3. Create a virtual environment using the  ``requirements.txt``
4. Open the terminal, go to ``\django_wcapp\django_wcapp\`` folder and run the following command `python manage.py migrate`
5. Make sure Chrome is downloaded
6. Run the `main.py` file.

# Notes

This project was not conceived to be commercial in any way or shape.
