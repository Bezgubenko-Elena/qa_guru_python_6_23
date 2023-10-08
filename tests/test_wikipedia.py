from allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import be, browser, have


def test_search():
    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')

    with step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


def test_open_article():
    with step('Tap on article'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/horizontal_scroll_list_item_text')).click()

    with step('Check content ion page'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/horizontal_scroll_list_item_text')).should(
            be.not_.present)
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/view_news_fullscreen_story_text')).should(be.present)
