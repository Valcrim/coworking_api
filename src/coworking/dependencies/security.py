from services.security import SecurityService

def get_security_service() -> SecurityService:
    service = SecurityService()
    return service