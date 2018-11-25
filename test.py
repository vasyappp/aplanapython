import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Search(unittest.TestCase):
    results_xpath = "//div[@class = 'bkWMgd']//div[@class = 'g']"
    result_link_xpath = ".//div[@class = 'r']/a"
    tabs_links_xpath = "//div[contains(@class, 'hdtb-mitem hdtb')]/a"
    more_button_xpath = "//*[@id = 'ow16']/a"
    more_tabs_links_xpath = "//div[@jsowner = 'ow16']/a"
    image_results_xpath = "//div[@jscontroller = 'Q7Rsec']"

    def setUp(self):
        self.drv = webdriver.Chrome('chromedriver.exe')
        self.drv.get('http://www.google.com/ncr')

    def test_search(self):
        # Проверка открытия страницы Google
        assert 'Google' in self.drv.title
        elm = self.drv.find_element_by_name('q')

        # Поиск selenide
        elm.send_keys('selenide')
        elm.send_keys(Keys.RETURN)
        assert 'No results found' not in self.drv.page_source

        # Проверка того, что первый результат ведет на сайт selenide.org
        results = self.drv.find_elements_by_xpath(self.results_xpath)
        assert str(self.get_link(results[0])).find("selenide.org") != -1

        # Выбор вкладки Картинки
        tab = self.find_tab(['Images', 'Картинки'])
        assert tab is not None
        tab.click()

        # Проверка того, что первый результат в поиске картинок связан с сайтом selenide.org
        image_results = self.drv.find_elements_by_xpath(self.image_results_xpath)
        assert str(image_results[0].text).find("selenide.org") != -1

        # Возврат к разделу поиска Все
        tab = self.find_tab(['All', 'Все'])
        assert tab is not None
        tab.click()

        # Проверка того, что первый результат вновь ведет на сайт selenide.org
        results = self.drv.find_elements_by_xpath(self.results_xpath)
        assert str(self.get_link(results[0])).find("selenide.org") != -1

    def get_link(self, elem):
        return elem.find_element_by_xpath(self.result_link_xpath).get_attribute("href")

    def find_tab(self, tab_name):
        # Поиск вкладки в видимых ссылках
        tabs = self.drv.find_elements_by_xpath(self.tabs_links_xpath)
        for tab in tabs:
            # Если вкладка найдена, возвращаем ее и выходим из функции
            if tab.text in tab_name:
                return tab

        # Если вкладка не найдена, нажимаем на кнопку "Еще" и ищем нужную вкладку среди появившихся
        more_button = self.drv.find_element_by_xpath(self.more_button_xpath)
        more_button.click()
        tabs = self.drv.find_elements_by_xpath(self.more_tabs_links_xpath)
        for tab in tabs:
            if tab.text in tab_name:
                return tab
        return None

    def tearDown(self):
        self.drv.close()


if __name__ == '__main__':
    unittest.main()
