from app.pages.base.scrollable_nav_base_page import ScrollableNavigationBasePage

import scheduler.scheduler as scheduler


class SchedulerPage(ScrollableNavigationBasePage):
    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)
        self.tasks_txt_label = self.create_section_text("Tasks")
        self.queues_txt_label = self.create_section_text("Queues")
        self.locks_txt_label = self.create_section_text("Locks")

    def loop(self):
        report = scheduler.get_report()
        self.tasks_txt_label.configure(text="\n".join(report['tasks']))
        self.queues_txt_label.configure(text="\n".join(report['queues']))
        self.locks_txt_label.configure(text="\n".join(report['locks']))
