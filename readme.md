# BLS Appointment Booking Automation Script

## Overview
This Python script automates the process of logging into the BLS Italy Pakistan appointment system, checking for available appointments, and attempting to book one using the **Playwright** browser automation tool. The script is integrated with **2Captcha** to solve both image-based CAPTCHAs and reCAPTCHA v2 challenges. It periodically refreshes the page to check for new appointment availability and tries to book an appointment when it becomes available.

## Features
- **Login Automation**: Automatically logs into the BLS Italy Pakistan website using the provided credentials.
- **CAPTCHA Solving**: Utilizes the 2Captcha API to solve both image-based CAPTCHAs and reCAPTCHA v2 challenges.
- **Appointment Availability Check**: Continuously monitors for available appointments for a specified date.
- **Form Auto-fill**: Automatically fills in required fields for appointment booking (location, appointment type, etc.).
- **Error Handling and Retry**: Handles timeouts, login issues, and pop-up windows with retries to maintain stability.
- **Session Management**: Automatically logs back in if the session expires or if the user is logged out.

## Prerequisites
1. **Python**: Ensure Python 3.x is installed.
2. **Playwright**: Install Playwright and set it up by running the following commands:
   ```bash
   pip install playwright
   playwright install
   ```
3. **Pillow**: Used for image handling in CAPTCHAs. Install it with:
   ```bash
   pip install pillow
   ```
4. **Requests**: Used for sending HTTP requests (to 2Captcha and for image downloads). Install with:
   ```bash
   pip install requests
   ```

## How to Set Up
1. **2Captcha API Key**: Obtain a 2Captcha API key from [2Captcha](https://2captcha.com) and insert it into the script by replacing `'<************>'` in the `API_KEY` variable.
2. **BLS Account Credentials**: Update the placeholders `<EMAIL>` and `<PASSWORD>` in the `login` function with your BLS login credentials.
3. **Python Libraries**: Ensure all required libraries are installed:
   - Playwright
   - Pillow
   - Requests

4. **Playwright Setup**: Run the following to install the necessary browser binaries:
   ```bash
   playwright install
   ```

## How to Run
1. Ensure all dependencies are installed.
2. Run the script from the terminal:
   ```bash
   python main.py
   ```

## Key Functions

- **solve_recaptcha_v2()**: Uses 2Captcha to solve the reCAPTCHA v2 challenge and returns the solution to be used in the login process.
- **solve_captcha()**: Downloads the CAPTCHA image, sends it to 2Captcha, and returns the solution.
- **login()**: Automates the login process using the provided credentials and solved reCAPTCHA.
- **check_appointment_date()**: Checks if appointments are available for a specified date (11 September in this case).
- **main()**: The main control loop for logging in, navigating to the appointment page, checking appointment availability, and booking.

## Usage Notes
- The script checks if an appointment is available for **11 September**. If you wish to change the date, modify the `check_appointment_date()` function accordingly.
- Ensure the BLS account credentials and 2Captcha API key are correct and up-to-date in the script.
- The script runs in an infinite loop, checking for available appointments and refreshing the page regularly. To stop it, terminate the process manually.

## Disclaimer
This script is intended for educational purposes. Automating appointment booking may violate terms of service for certain websites. Use this script responsibly and at your own risk.