import time
import requests
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright, TimeoutError

API_KEY = '<************>' # 2Captcha API key
SITE_KEY = '6LcVdzUqAAAAAPGbSct68gBCV0Rh3QWAVJdYlMh0'
LOGIN_URL = "https://blsitalypakistan.com/account/login//"
APPOINTMENT_URL = "https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment"
LOGOUT_URL = "https://blsitalypakistan.com/"

def solve_captcha(captcha_image_url):
    response = requests.get(captcha_image_url)
    img = Image.open(BytesIO(response.content))
    img.save("captcha.png")

    with open("captcha.png", "rb") as captcha_file:
        response = requests.post(
            "http://2captcha.com/in.php",
            files={"file": captcha_file},
            data={"key": API_KEY, "method": "post"}
        )

    captcha_id = response.text.split('|')[1]
    for _ in range(20):
        response = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}")
        if response.text == 'CAPCHA_NOT_READY':
            time.sleep(5)
            continue
        elif 'OK' in response.text:
            captcha_solution = response.text.split('|')[1]
            return captcha_solution.strip()
        else:
            raise Exception(f"Error solving captcha: {response.text}")

def solve_recaptcha_v2():
    captcha_response = requests.post(
        "http://2captcha.com/in.php",
        data={
            "key": API_KEY,
            "method": "userrecaptcha",
            "googlekey": SITE_KEY,
            "pageurl": APPOINTMENT_URL
        }
    )

    if captcha_response.text.startswith('OK|'):
        captcha_id = captcha_response.text.split('|')[1]
    else:
        raise Exception(f"Error sending reCAPTCHA solving request: {captcha_response.text}")

    result_url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}"

    for _ in range(20):
        result_response = requests.get(result_url)
        if result_response.text == 'CAPCHA_NOT_READY':
            time.sleep(5)
            continue
        elif result_response.text.startswith('OK|'):
            return result_response.text.split('|')[1]
        else:
            raise Exception(f"Error getting reCAPTCHA solution: {result_response.text}")

def check_appointment_date(page):
    calendar = page.query_selector('table.table-condensed')
    if calendar:
        day_11 = calendar.query_selector('td[data-date="1726012800000"]')
        if day_11 and "disabled" not in day_11.get_attribute("class"):
            return True
    return False

def login(page):
    try:
        page.goto(LOGIN_URL)
        page.fill('input[placeholder="Enter Email"]', "<EMAIL>") # Enter your email
        page.fill('input[placeholder="Enter Password"]', "<PASSWORD>") # Enter your password

        recaptcha_solution = solve_recaptcha_v2()
        page.evaluate(f'document.getElementById("g-recaptcha-response").value = "{recaptcha_solution}"')
        page.click('button[name="submitLogin"]')
        print("Logged in successfully.")
    except Exception as e:
        print(f"Login failed: {e}")
        page.reload()

def main():
    with sync_playwright() as p:
        while True:
            try:
                browser = p.firefox.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                login(page)

                time.sleep(1)
                while True:
                    try:
                        page.goto(APPOINTMENT_URL)
                    except TimeoutError as e:
                        print(f"Page load timeout: {e}, retrying...")
                        page.reload()
                        continue
                    except Exception as e:
                        print(f"Error navigating to appointment page: {e}")
                        page.reload()
                        continue

                    if page.url == LOGOUT_URL:
                        print("Logged out, logging in again.")
                        login(page)
                        continue

                    try:
                        popup = page.query_selector('a.cl')
                        if popup:
                            popup.click()
                            print("Popup closed successfully.")
                    except Exception as e:
                        print(f"Popup closure failed: {e}, continuing...")

                    try:
                        # Select Islamabad center
                        page.select_option('select#valCenterLocationId', label="Islamabad (Pakistan)")
                        time.sleep(2)

                        page.select_option("select#valCenterLocationTypeId", label="National - Work")
                        selected_value = page.evaluate("() => document.getElementById('valCenterLocationTypeId').value")
                        print(f"Selected value: {selected_value}")
                        time.sleep(2)

                        page.select_option('select#valAppointmentForMembers', label="Individual")
                        time.sleep(2)
                    except Exception as e:
                        print(f"Form selection error: {e}, retrying...")
                        page.reload()
                        continue
                    while True:
                        if page.url == LOGOUT_URL:
                            print("Logged out, logging in again.")
                            break
                              
                        try:
                            if check_appointment_date(page):
                                print("Appointment for 11 September is available.")
                                captcha_image_url = page.get_attribute('#Imageid', 'src')
                                second_captcha_solution = solve_captcha(captcha_image_url)
                                page.fill('#captcha_code_reg', second_captcha_solution)
                                print("Second captcha filled.")

                                page.check('#agree')
                                page.click('#valBookNow')
                                print("Appointment booked for 11 September.")
                                return
                            
                            else:
                                print("Appointment for 11 September is not available. Refreshing page...")
                                page.reload()
                        except Exception as e:
                            print(f"Error checking appointment: {e}, retrying...")
                            page.reload()

                    time.sleep(1)
                    page.reload()
           

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            
            finally:
                context.close()
                browser.close()
                print("Session ended, restarting...")

if __name__ == "__main__":
    main()
