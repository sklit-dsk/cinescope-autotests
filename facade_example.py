class Computer:
    def power_on(self): print("Computer: powering on")
    def load_os(self): print("Computer: loading OS")

class IDE:
    def open(self, project_path: str): print(f"IDE: opening {project_path}")

class Browser:
    def open(self, url: str): print(f"Browser: opening {url}")

class Messenger:
    def connect(self): print("Messenger: connecting")
    def set_status(self, status: str): print(f"Messenger: status -> '{status}'")


class WorkdayFacade:
    
    def __init__(self):
        self.computer = Computer()
        self.ide = IDE()
        self.browser = Browser()
        self.messenger = Messenger()
        
    def start_work_day(self, project_path: str, jira_url: str):
        self.computer.power_on()
        self.computer.load_os()
        self.ide.open(project_path)
        self.browser.open(jira_url)
        self.messenger.connect()
        self.messenger.set_status("online")



workday = WorkdayFacade()
workday.start_work_day("/projects/my-app", "https://jira.company.com")

# После реализации вот это должно вывести все шесть строк по порядку:
"""
Computer: powering on
Computer: loading OS
IDE: opening /projects/my-app
Browser: opening https://jira.company.com
Messenger: connecting
Messenger: status -> online
"""