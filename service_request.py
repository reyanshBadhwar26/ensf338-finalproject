class ServiceRequest:
    VALID_PRIORITIES = {"Emergency", "Standard", "Low"}
    
    
    def __init__(self, request_id: str, service_type: str, description: str, priority: str, requester_name: str):

        if priority not in ServiceRequest.VALID_PRIORITIES: 
            raise ValueError("Invalid. Priority must be: Emergency, Standard, or Low")
        self.request_id = request_id
        self.service_type = service_type
        self.description = description
        self.priority = priority
        self.requester_name = requester_name


    def __repre__(self):
        return(f"ServiceRequest("
               f"id = '{self.request_id}', "
               f"type = '{self.service_type}', "
               f"priority = '{self.priority}', "
               f"requester_name = '{self.requester_name}')")
    
    def display_info(self):
        return(f"Request ID: {self.request_id} | "
               f"Priority: {self.priority} | "
               f"Service: {self.service_type} | "
               f"Requester: {self.requester_name} | "
               f"Description: {self.description} | ")
               