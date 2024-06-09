import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

@pytest.fixture
def URL():
    return 'http://127.0.0.1:5000' # URL of the program


@pytest.fixture
def driver():
    my_driver = webdriver.Chrome()
    return my_driver
