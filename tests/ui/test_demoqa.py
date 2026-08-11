from playwright.sync_api import Page, expect
from utils.data_generator import DataGenerator
import time


def test_text_box(page: Page):
    page.goto('https://demoqa.com/text-box')
    page.fill(selector='#userName', value='testQa')
    time.sleep(5)
    page.fill(selector='#userEmail', value= 'test@gmail.com')
    time.sleep(5)
    page.locator('#currentAddress').fill('Test address')
    time.sleep(5)
    page.fill(selector='#permanentAddress', value='Test permanent address')
    time.sleep(5)
    page.locator('#submit').click() # можно сначала определить локатор, а потом кликнуть
    expect(page.locator('#output #name')).to_have_text('Name:testQa')
    expect(page.locator('#output #email')).to_have_text('Email:test@gmail.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :Test address')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :Test permanent address')
    
def test_web_tables(page: Page):
    page.goto('https://demoqa.com/webtables')
    page.get_by_role('button', name='Add').click()
    page.locator('.modal-header #registration-form-modal:has-text("Registration Form")').is_visible()
    first_name = DataGenerator.generate_firstname()
    page.get_by_placeholder("First Name").fill(first_name)
    page.get_by_placeholder("Last Name").fill(DataGenerator.generate_lastname())
    page.locator("#userEmail").fill(DataGenerator.generate_random_email())
    page.locator("#age").fill(f"{DataGenerator.generate_age()}")
    page.locator("#salary").fill(f"{DataGenerator.generate_salary()}")
    page.get_by_placeholder("Department").fill(DataGenerator.generate_departament())
    time.sleep(5)
    page.get_by_role('button', name='Submit').click()
    expect(page.get_by_role('cell', name=first_name))
    
def test_practice_form(page: Page):
    page.goto('https://demoqa.com/automation-practice-form')
    first_name = DataGenerator.generate_firstname()
    page.get_by_placeholder("First Name").fill(first_name)
    page.get_by_placeholder("Last Name").type(DataGenerator.generate_lastname())
    page.locator("#userEmail").type(DataGenerator.generate_random_email())
    page.check('#gender-radio-1')
    page.get_by_placeholder("Mobile Number").type(f"{DataGenerator.generate_mobile_number()}")
    default_date_of_birth = page.get_attribute("#dateOfBirthInput", "value")
    page.locator('#subjectsInput').fill('Maths')
    page.get_by_text('Maths', exact=True).click()
    page.get_by_role("checkbox", name="Sports").click()
    page.get_by_role("checkbox", name="Music").click()
    page.get_by_role("textbox", name="Current Address").fill('Test address')
    page.locator('#react-select-3-input').fill('NCR')
    page.get_by_text('NCR', exact=True).click()
    page.locator('#react-select-4-input').fill('Delhi')
    page.get_by_text('Delhi', exact=True).click()
    assert default_date_of_birth == time.strftime("%d %b %Y")
    footer_value = "© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED."
    footer_find = page.locator('footer span').text_content()
    assert footer_find == footer_value
    

def test_radio_button_active(page: Page):
    page.goto('https://demoqa.com/radio-button')
    page.is_enabled("#yesRadio")
    page.is_enabled("#impressiveRadio")
    page.is_disabled("#noRadio")
    
def test_check_box_visible(page: Page):
    page.goto('https://demoqa.com/checkbox')
    page.get_by_title("Home").is_visible()
    page.get_by_title("Desktop").is_hidden()
    page.locator(".rc-tree-switcher").click()
    page.get_by_title("Desktop").is_visible()
    
def test_dynamic_properties(page: Page):
    page.goto("https://demoqa.com/dynamic-properties")
    page.locator("#visibleAfter").is_hidden()
    page.wait_for_selector("#visibleAfter", state="visible", timeout=10000)
    
from playwright.sync_api import Page, expect


def test_expect(page: Page):
    page.goto("https://demoqa.com/radio-button")
    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")
    expect(no_radio).to_be_disabled()  
    expect(yes_radio).to_be_enabled()  
    expect(impressive_radio).to_be_enabled()  
    page.locator('[for="yesRadio"]').click()  
    expect(yes_radio).to_be_checked()  
    expect(impressive_radio).not_to_be_checked() 
