

class CategoryPageInfor:
    """Get category info in page"""
    def __init__(self):
        self.total_pages = 0
        self.total_elements = 0

    @property
    def total_pages(self):
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value):
        self._total_pages = value

    @property
    def total_elements(self):
        return self._total_elements

    @total_elements.setter
    def total_elements(self, value):
        self._total_elements = value
