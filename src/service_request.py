class ServiceRequest:
    VALID_PRIORITIES = {"Emergency", "Standard", "Low"} #The priority levels for service requests: Emergency (highest), Standard (middle), Low (lowest)
    
    
    def __init__(self, request_id: str, service_type: str, description: str, priority: str, requester_name: str):

        if priority not in ServiceRequest.VALID_PRIORITIES: 
            raise ValueError("Invalid. Priority must be: Emergency, Standard, or Low")  #Make sure that all priorities are valid. therwise, reject
        self.request_id = request_id         #Store service request id
        self.service_type = service_type     #Store service type
        self.description = description       #Store service description
        self.priority = priority             #Store service priority
        self.requester_name = requester_name #Store service requester name


    def __repr__(self):         #String format of object
        return(f"ServiceRequest("
               f"id = '{self.request_id}', "
               f"type = '{self.service_type}', "
               f"priority = '{self.priority}', "
               f"requester_name = '{self.requester_name}')")
    
    def display_info(self):     #Format for printing request details
        return(f"Request ID: {self.request_id} | "
               f"Priority: {self.priority} | "
               f"Service: {self.service_type} | "
               f"Requester: {self.requester_name} | "
               f"Description: {self.description} | ")
               