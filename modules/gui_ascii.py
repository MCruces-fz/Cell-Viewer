from modules.parent_gui import CellsApp


class CellsAppASCII(CellsApp):
    def update_datetime(self):
        self.from_date = self.cal_from.get_date()
        self.to_date = self.cal_from.get_date()
