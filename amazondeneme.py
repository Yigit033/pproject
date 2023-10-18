from selenium import webdriver
from bs4 import BeautifulSoup

def get_amazon_discount_page():
    url = "https://www.amazon.com.tr/deals?ref_=nav_cs_gb"
    driver = webdriver.Chrome()  # Google Chrome tarayıcısını başlatır.
    driver.get(url)  # Belirtilen URL'ye gidilir.
    html_content = driver.page_source  # Sayfanın HTML içeriğini alır.
    # driver.quit()  # Tarayıcıyı kapatır.

    return html_content

def parse_discount_products(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    products = soup.find_all("div", class_="s-include-content-margin")

    discount_products = []

    for product in products:
        product_title = product.find("span", class_="a-size-base-plus a-color-base a-text-normal").text.strip()
        product_price = product.find("span", class_="a-offscreen").text.strip()
        product_normal_price = product.find("span", class_="a-price a-text-price").find("span", class_="a-offscreen").text.strip()

        # İndirim hesaplama
        try:
            discount_percentage = round((1 - (float(product_price.replace(" TL", "").replace(",", ".")) / float(
                product_normal_price.replace(" TL", "").replace(",", ".")))) * 100, 2)
        except ZeroDivisionError:
            discount_percentage = 0

        if discount_percentage > 0:
            discount_products.append({
                "title": product_title,
                "price": product_price,
                "normal_price": product_normal_price,
                "discount_percentage": discount_percentage
            })

    return discount_products

def display_discount_products(discount_products):
    for product in discount_products:
        print("Ürün Adı:", product["title"])
        print("Fiyat:", product["price"])
        print("Normal Fiyat:", product["normal_price"])
        print("İndirim Oranı:", product["discount_percentage"], "%")
        print("-" * 50)

if __name__ == "__main__":
    amazon_page = get_amazon_discount_page()
    if amazon_page:
        discount_products = parse_discount_products(amazon_page)
        display_discount_products(discount_products)
