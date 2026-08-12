from playwright.sync_api import Page, expect
from models.ui_models import UIUserDemoQA
from constants.base_urls import (
    DEMOQA_AUTOMATION_PRACTICE_FORM,
    DEMOQA_CHECK_BOX,
    DEMOQA_WEB_TABLES,
    DEMOQA_DYNAMIC_PROPERTIES,
    DEMOQA_RADIO_BUTTON,
    DEMOQA_TEXT_BOX,
)
import time


def test_text_box(page: Page, ui_user_data: UIUserDemoQA):
    page.goto(DEMOQA_TEXT_BOX)
    page.fill(selector="#userName", value=f"{ui_user_data.userName}")
    page.fill(selector="#userEmail", value=ui_user_data.userEmail)
    page.locator("#currentAddress").fill("Test address")
    page.fill(selector="#permanentAddress", value="Test permanent address")
    page.locator("#submit").click()
    expect(page.locator("#output #name")).to_have_text(f"Name:{ui_user_data.userName}")
    expect(page.locator("#output #email")).to_have_text(
        f"Email:{ui_user_data.userEmail}"
    )
    expect(page.locator("#output #currentAddress")).to_have_text(
        "Current Address :Test address"
    )
    expect(page.locator("#output #permanentAddress")).to_have_text(
        "Permanent Address :Test permanent address"
    )


def test_web_tables(page: Page, ui_user_data: UIUserDemoQA):
    page.goto(DEMOQA_WEB_TABLES)
    page.get_by_role("button", name="Add").click()
    page.locator(
        '.modal-header #registration-form-modal:has-text("Registration Form")'
    ).is_visible()
    page.get_by_placeholder("First Name").fill(ui_user_data.firstName)
    page.get_by_placeholder("Last Name").fill(ui_user_data.lastName)
    page.locator("#userEmail").fill(ui_user_data.userEmail)
    page.locator("#age").fill(f"{ui_user_data.userAge}")
    page.locator("#salary").fill(f"{ui_user_data.userSalary}")
    page.get_by_placeholder("Department").fill(f"{ui_user_data.userDepartament}")
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_role("cell", name=ui_user_data.firstName))


def test_practice_form(page: Page, ui_user_data: UIUserDemoQA):
    page.goto(DEMOQA_AUTOMATION_PRACTICE_FORM)
    page.get_by_placeholder("First Name").fill(ui_user_data.firstName)
    page.get_by_placeholder("Last Name").type(ui_user_data.lastName)
    page.locator("#userEmail").type(ui_user_data.userEmail)
    page.check("#gender-radio-1")
    page.get_by_placeholder("Mobile Number").type(f"{ui_user_data.userPhoneNumber}")
    default_date_of_birth = page.get_attribute("#dateOfBirthInput", "value")
    page.locator("#subjectsInput").fill("Maths")
    page.get_by_text("Maths", exact=True).click()
    page.get_by_role("checkbox", name="Sports").click()
    page.get_by_role("checkbox", name="Music").click()
    page.get_by_role("textbox", name="Current Address").fill("Test address")
    page.locator("#react-select-3-input").fill("NCR")
    page.get_by_text("NCR", exact=True).click()
    page.locator("#react-select-4-input").fill("Delhi")
    page.get_by_text("Delhi", exact=True).click()
    assert default_date_of_birth == time.strftime("%d %b %Y")
    footer_value = "© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED."
    footer_find = page.locator("footer span").text_content()
    assert footer_find == footer_value


def test_radio_button_active(page: Page):
    page.goto(DEMOQA_RADIO_BUTTON)
    page.is_enabled("#yesRadio")
    page.is_enabled("#impressiveRadio")
    page.is_disabled("#noRadio")

def test_check_box_visible(page: Page):
    page.goto(DEMOQA_CHECK_BOX)
    page.get_by_title("Home").is_visible()
    page.get_by_title("Desktop").is_hidden()
    page.locator(".rc-tree-switcher").click()
    page.get_by_title("Desktop").is_visible()

def test_dynamic_properties(page: Page):
    page.goto(DEMOQA_DYNAMIC_PROPERTIES)
    page.locator("#visibleAfter").is_hidden()
    page.wait_for_selector("#visibleAfter", state="visible", timeout=10000)


def test_expect(page: Page):
    page.goto(DEMOQA_RADIO_BUTTON)
    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")
    expect(no_radio).to_be_disabled()  
    expect(yes_radio).to_be_enabled()  
    expect(impressive_radio).to_be_enabled()  
    page.locator('[for="yesRadio"]').click()  
    expect(yes_radio).to_be_checked()  
    expect(impressive_radio).not_to_be_checked() 
