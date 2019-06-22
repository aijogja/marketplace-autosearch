from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from config import SETTINGS
import time


PARAMS = SETTINGS['tokopedia']


def main():
    # Variable2
    viewed_products = []

    # Chrome Option
    chrome_options = Options()
    if SETTINGS['headless']:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path='./chromedriver',
        options=chrome_options
    )
    driver.get('https://www.tokopedia.com')
    print('Opening the browser ...')
    searchbox_el = driver.find_element_by_id('search-keyword')
    searchbox_el.send_keys(PARAMS['keyword'])
    searchbox_el.submit()
    print('Submit the keyword')

    def view_product(produk):
        print('klik produk')
        driver.execute_script("arguments[0].click();", produk)
        time.sleep(5)
        driver.back()

    def pagination_clicker():
        """
        Pagination Loop
        """
        # wait the results
        paginations = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "GUHElpkt"))
        )
        products_toko = driver.find_elements_by_class_name('vlEGRFVq')
        url = parse.urlsplit(driver.current_url)
        qs = parse.parse_qs(url.query)

        if 'page' in qs:
            print('Page %s' % qs.get('page')[0])
        else:
            print('Page 1')

        # list products
        try:
            for prd in products_toko:
                product_link = prd.find_element_by_class_name('_2rQtYSxg')
                if product_link.text in PARAMS['shop_name']:
                    product_title = prd.find_element_by_tag_name('h3')
                    print("%s (%s)" % (product_title.text, product_link.text))
                    if (product_title.text in PARAMS['view_products'] and
                            product_title.text not in viewed_products):
                        viewed_products.append(product_title.text)
                        view_product(prd)

            # break the search
            if 'page' in qs and qs.get('page')[0] == PARAMS['deep']:
                print('Complete')
                return None

            for pagination in paginations:
                if pagination.text == '>':
                    driver.execute_script("arguments[0].click();", pagination)
                    pagination_clicker()
        except StaleElementReferenceException:
            pagination_clicker()

    pagination_clicker()


if __name__ == '__main__':
    main()
