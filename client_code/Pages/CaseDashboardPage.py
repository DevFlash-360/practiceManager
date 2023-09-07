from AnvilFusion.components.DashboardPage import DashboardPage


class CaseDashboardPage(DashboardPage):
    
    def __init__(self, container_id=None, **kwargs):
        
        layout = {
            'cellSpacing': [10, 10],
            'columns': 3,
        }
        
        super().__init__(container_id=container_id, layout=layout, **kwargs)
    