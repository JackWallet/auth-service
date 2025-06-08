class DomainError(Exception):
    """For the violation of general domain rules,
    in our case raised when trying to change the immutable
    attributes of an entity
    """


class DomainFieldValidationError(DomainError):
    """Raised when violating the rule for domain field entity"""
