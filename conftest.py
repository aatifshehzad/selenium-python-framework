import os
import yaml
import logging
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = None
browser = None
pytest.root_folder = str(Path(__file__).parent)
config_path = pytest.root_folder + os.sep + "config.yml"
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


@pytest.fixture(scope='session')
def get_browser(request, config):
    if "browser" not in config:
        return request.config.getoption("--browser")
    elif config["browser"] not in supported_browsers:
        raise Exception(f'"{config["browser"]}" is not a supported browser')
    else:
        return config["browser"]


@pytest.fixture(scope='session')
def get_timeout(config):
    if ("time_out" in config) and (config["time_out"] is not None) and (config["time_out"] != ""):
        return config["time_out"]
    else:
        return default_wait_time


@pytest.fixture(scope='session')
def get_url(config):
    if ("url" in config) and ("url" is not None) and ("url" != ""):
        return config["url"]
    else:
        return default_url


@pytest.fixture(scope='class')
def setup(request, config, get_browser, get_timeout, get_url):
    global driver
    global browser
    browser = get_browser
    if browser == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        if config["headless"]:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    elif browser == 'firefox':
        firefox_options = webdriver.FirefoxOptions
        if config["headless"]:
            firefox_options.headless = True
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    elif browser == 'edge':
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager(log_level=logging.INFO).install()))
    else:
        raise Exception("Provide valid driver name")
    driver.maximize_window()
    driver.implicitly_wait(get_timeout)
    driver.get(get_url)
    request.cls.driver = driver
    yield
    driver.close()
    driver.quit()


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
            file_path = pytest.root_folder + os.sep + "screenshots" + os.sep + file_name
            _capture_screenshot(file_path)
            if file_name:
                html = '<div><img src="/screenshots/%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
