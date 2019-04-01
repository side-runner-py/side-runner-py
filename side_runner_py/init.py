from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from .config import Config


def initialize(driver_url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'ja_JP'})

    cap = options.to_capabilities()

    if Config.HTTP_PROXY or Config.HTTPS_PROXY or Config.NO_PROXY:
        proxy = Proxy()
        proxy.sslProxy = Config.HTTPS_PROXY
        proxy.httpProxy = Config.HTTP_PROXY
        proxy.noProxy = Config.NO_PROXY
        proxy.proxyType = ProxyType.MANUAL
        proxy.add_to_capabilities(cap)

    driver = webdriver.Remote(
        command_executor=driver_url,
        desired_capabilities=cap)

    return driver
