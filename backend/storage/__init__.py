from backend.config import get_settings

settings = get_settings()


def get_storage():
    if settings.storage_backend == "azure":
        from backend.storage.azure_storage import AzureStorage
        return AzureStorage()
    from backend.storage.local_storage import LocalStorage
    return LocalStorage()
