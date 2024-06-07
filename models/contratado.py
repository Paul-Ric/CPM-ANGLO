from datetime import date

class Contratado:
    def __init__(self, cpf:str,
                 worker_id:str,
                 first_name:str,
                 last_name:str,
                 vendor_number:str,
                 vendor_name:str,
                 work_schedule:str,
                 site_name:str,
                 site_code:str,
                 work_location_name:str,
                 work_location_code:str, 
                 permission_to_access_restaurant:str,
                 org_unit, contract_number:str,
                 contractor_area:str,
                 contractor_management:str,
                 contractor_inspector:str, 
                 cost_center_code:str, 
                 start_date:date, 
                 end_date:date, 
                 ato:str, 
                 atw:str):
        
        self.cpf = cpf
        self.worker_id = worker_id
        self.first_name = first_name
        self.last_name = last_name
        self.vendor_number = vendor_number
        self.vendor_name = vendor_name
        self.work_schedule = work_schedule
        self.site_name = site_name
        self.site_code = site_code
        self.work_location_name = work_location_name
        self.work_location_code = work_location_code
        self.permission_to_access_restaurant = permission_to_access_restaurant
        self.org_unit = org_unit
        self.contract_number = contract_number
        self.contractor_area = contractor_area
        self.contractor_management = contractor_management
        self.contractor_inspector = contractor_inspector
        self.cost_center_code = cost_center_code
        self.start_date = start_date
        self.end_date = end_date
        self.ato = ato
        self.atw = atw
