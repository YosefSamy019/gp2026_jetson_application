from app.pages.base.scrollable_nav_base_page import ScrollableNavigationBasePage
from app.pipe_line.signals import mcu_network_queue


class NetworkPage(ScrollableNavigationBasePage):
    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)
        self.txt_label = self.create_section_text("Tasks")

    def loop(self):
        mcu_network_out = mcu_network_queue.get_last()

        if mcu_network_out is None:
            return

        self.txt_label.configure(
            text="\n".join([
                f"F: {mcu_network_out.F}",
                f"T: {mcu_network_out.T}",
                f"A: {mcu_network_out.A}",
                f"Buffer: {mcu_network_out.buffer}",
                f"Last Receive Time: {mcu_network_out.last_receive_time}",
                f"Time Gone: {mcu_network_out.time_gone_from_last_receive}",
                f"Slave Active: {mcu_network_out.slave_active}"
            ])
        )
