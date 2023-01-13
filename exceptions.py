class BaseLazyPropertyException(Exception):
    
    def __init__(self, desciptor_name) -> None:
        self.desciptor_name = desciptor_name
        
class DeletedLazyProperty(BaseLazyPropertyException):
    
    def __str__(self):
        return f"The lazyproperty {self.desciptor_name} has been deleted."