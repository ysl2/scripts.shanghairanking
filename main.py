import numpy
import pandas
import selenium
import webdriver_manager.chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm.auto import tqdm


TIMEOUT = 10
TASKS = {
    'bcur': {
        'year': '202510',
        'columns': ['排名', '学校名称', '标签', '省市', '类型'],
        'xpathss': [
            ['./td[1]/div'],
            ['./td[2]/div/div[2]/div[1]/div/div/span'],
            ['./td[2]/div/div[2]/p'],
            ['./td[3]'],
            ['./td[4]'],
        ]
    },
    'arwu': {
        'year': '2024',
        'columns': ['排名', '学校名称', '国家', '国家/地区排名'],
        'xpathss': [
            ['./td[1]/div'],
            ['./td[2]/div/div[2]/div/span', './td[2]/div/div[2]/div[1]/div/div/span'],
            ['./td[3]'],
            ['./td[4]'],
        ]
    },
}


def get_driver():
    service = selenium.webdriver.ChromeService(
        webdriver_manager.chrome.ChromeDriverManager().install()
    )
    options = selenium.webdriver.ChromeOptions()
    options.add_argument('--headless')
    return selenium.webdriver.Chrome(service=service, options=options)


def find_elements(row, xpaths):
    for xpath in xpaths:
        if (tmp1 := row.find_elements(By.XPATH, xpath)):
            return tmp1[0].text


def main():
    driver = get_driver()
    for taskname, task in tqdm(TASKS.items()):
        df = pandas.DataFrame(columns=task['columns'])
        driver.get(f'https://www.shanghairanking.cn/rankings/{taskname}/{task["year"]}')
        pages = int(WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content-box"]/ul/li[8]/a'))
        ).text)
        for page in tqdm(range(1, pages + 1)):
            content_box = WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content-box"]'))
            )
            for row in tqdm(content_box.find_elements(By.XPATH, './div[2]/table/tbody/tr')):
                df.loc[len(df)] = [find_elements(row, xpaths) for xpaths in task['xpathss']]
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(content_box, TIMEOUT).until(
                    EC.element_to_be_clickable((By.XPATH, './ul/li[contains(@class, "ant-pagination-next")]/a'))
                )
            )
        df.replace([numpy.nan, ''], '-', inplace=True)
        df.to_csv(f'{taskname}{task["year"]}.csv', index=False, encoding='utf-8')
    driver.quit()


if __name__ == '__main__':
    main()
