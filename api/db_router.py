class MyDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'api_mysql':
            return 'postgres1'  # first PostgreSQL db
        if model._meta.app_label == 'api_pg':
            return 'postgres2'  # second PostgreSQL db
        return None

    def db_for_write(self, model, **hints):
        return None  # read-only

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return False
