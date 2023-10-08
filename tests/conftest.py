import allure
import pytest
from appium.options.android import UiAutomator2Options
from appium import webdriver
from selene import browser
import os
import config
from utils import helper


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    options = UiAutomator2Options().load_capabilities({

        'platformName': config.settings.android_platform,
        'platformVersion': config.settings.android_version,
        'deviceName': config.settings.android_device,

        'app': config.settings.app_url,

        'bstack:options': {
            'projectName': config.settings.project_name,
            'buildName': config.settings.build_name,
            'sessionName': config.settings.session_name,

            'userName': config.settings.b_username,
            'accessKey': config.settings.b_key
        }
    })

    browser.config.driver = webdriver.Remote(config.settings.browserstack_url, options=options)

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    helper.attach_bstack_video(session_id)
