from import_export import resources
from .models import *


class DataResources(resources.ModelResource):
    class meta:
        model = Data


class DataSource(resources.ModelResource):
    class meta:
        model = Data_source


class ManageStore(resources.ModelResource):
    class meta:
        model = Manage_store
        