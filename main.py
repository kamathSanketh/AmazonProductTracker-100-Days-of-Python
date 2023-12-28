import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
import os

URL = os.environ.get("URL")
USER_AGENT = os.environ.get("USER_AGENT")
ACCEPT_LANG = os.environ.get("ACCEPT_LANG")
SET_PRICE = float(os.environ.get("SET_PRICE"))
response = requests.get(URL, headers={"User-Agent": USER_AGENT, "Accept-Language": ACCEPT_LANG})
response.raise_for_status()
page = response.text
soup = BeautifulSoup(page, "lxml")
price = float(soup.find(class_="a-price-whole").get_text() + soup.find(class_="a-price-fraction").get_text())
if price <= SET_PRICE:
    my_email = os.environ.get("my_email")
    my_password = os.environ.get("my_password")
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=os.environ.get("to_addrs"),
                            msg=f"Send:Happy Birthday!"
                                f"\n"
                                f"\n"
                                f"Your desired product is at ${price}. Buy it through the link below."
                                f"\n{URL}"
                            )
        connection.close()