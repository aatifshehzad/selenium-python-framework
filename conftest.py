import os
from pathlib import Path
import yaml
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.logger import Logger

driver = None
config_path = str(Path(__file__).parent) + os.sep + "config.yml"
default_wait_time = 10
supported_browsers = ["chrome", "firefox", "edge"]
default_url = "https://www.google.com/"


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="my option: chrome or firefox or edge"
    )


@pytest.fixture(scope='session')
def config():
    config_file = open(config_path, "r")
    return yaml.full_load(config_file)


@pytest.fixture(scope='class')
def setup(request, config):
    global driver
    if "browser" not in config:
        raise Exception('The config file does not contain "browser"')
    elif config["browser"] not in supported_browsers:
        raise Exception(f'"{config["browser"]}" is not a supported browser')

    if config["browser"] == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        if config["headless"]:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    elif config["browser"] == 'firefox':
        firefox_options = webdriver.FirefoxOptions
        if config["headless"]:
            firefox_options.headless = True
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    elif config["browser"] == 'edge':
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager(log_level=logging.INFO).install()))
    else:
        raise Exception("Provide valid driver name")
    driver.maximize_window()
    if (config["time_out"] is not None) and (config["time_out"] != ""):
        driver.implicitly_wait(config["time_out"])
    else:
        driver.implicitly_wait(default_wait_time)

    if ("url" in config) and ("url" is not None) and ("url" != ""):
        driver.get(config["url"])
    else:
        driver.get(default_url)
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
