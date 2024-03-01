class DbRouter:

    def db_for_read(self, model, **hints):
        return 'read_db'    

    def db_for_write(self, model, **hints):
        return 'write_db'

    def allow_relation(self, obj1, obj2, **hints):
        return True
