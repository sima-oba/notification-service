class EntityNotFound(Exception):
    def __init__(self, entity, reason):
        if hasattr(entity, '__name__'):
            entity = entity.__name__
        super().__init__(f'Entity {entity} not found: {reason}')


class EmailError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)
