import logging

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.logger import Logger

driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="my option: chrome or firefox or edge"
    )


@pytest.fixture(scope='class')
def setup(request):
    global driver
    browser_name = request.config.getoption("browser")
    if browser_name == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("start-maximized")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    elif browser_name == 'firefox':
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    elif browser_name == 'edge':
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager(log_level=logging.INFO).install()))
    else:
        raise Exception("Provide valid driver name")
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # file_name = report.nodeid.replace("::", "_") + ".png"
            file_name = report.nodeid.split("::")[-1] + ".png"
            file_path = Logger.ROOT_PATH + "/screenshots/" + file_name
            _capture_screenshot(file_path)
            if file_name:
                html = '<div><img src="/screenshots/%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
