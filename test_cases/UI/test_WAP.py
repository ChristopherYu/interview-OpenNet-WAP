import datetime
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


def _is_video_playing(driver: WebDriver) -> bool:
    """
    Returns true if text of ele_current_time(p[data-a-target='player-seekbar-current-time']) is not 00:00:00.
    :param driver: WebDriver
    :return bool
    """
    count = 0
    try:
        while count < 30:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p[data-a-target='player-seekbar-current-time']")))
            ele_current_time = driver.find_element(By.CSS_SELECTOR, "p[data-a-target='player-seekbar-current-time']")
            if ele_current_time.text != "00:00:00":
                return True
            count += 1
            time.sleep(1000)
        return False
    except NoSuchElementException:
        return False


class TestTwitch:
    def test_video(self, driver: WebDriver) -> None:
        # step 1 : go to twitch
        driver.get('https://m.twitch.tv')
        assert driver.title == 'Twitch'
        assert driver.current_url == 'https://m.twitch.tv/'

        # step 2 : click search icon
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="搜尋"]'))).click()

        # step 3 : input StarCraft ii
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input')))
        input_box = driver.find_element(By.CSS_SELECTOR, 'input')
        input_box.send_keys("StarCraft II")
        input_box.send_keys(Keys.ENTER)

        # step 4 : scroll two times
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'section')))
        sections = driver.find_elements(By.CSS_SELECTOR, 'section')
        driver.execute_script("arguments[0].scrollIntoView(true);", sections[1])
        driver.execute_script("arguments[0].scrollIntoView(true);", sections[2])

        # step 5 : select a video
        # if channel has watching limitation, this case would fail
        videos = driver.find_elements(By.CSS_SELECTOR, 'img.tw-image')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(videos[-1])).click()

        # step 6 : if video started, take a screenshot
        # close popup windows
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='關閉音訊靜音通知']"))).click()
        except:
            pass

        if _is_video_playing(driver):
            driver.save_screenshot(f"../../screenshot/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png")
        else:
            assert False
