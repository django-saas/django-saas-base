from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS


def create_permissions(app_config, verbosity=2, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    if not app_config.models_module:
        return

    if app_config.label != "saas_base":
        return

    try:
        Permission = apps.get_model(app_config.label, "Permission")
    except LookupError:
        return

    existed_perms = set(Permission.objects.values_list("name", flat=True).all())

    perms = []
    if "tenant.read" not in existed_perms:
        perms.append(Permission(name="tenant.read", description="Read permission for tenants"))
    if "tenant.write" not in existed_perms:
        perms.append(Permission(name="tenant.write", description="Write permission for tenants"))
    if "tenant.admin" not in existed_perms:
        perms.append(Permission(name="tenant.admin", description="Admin permission for tenants"))

    if perms:
        Permission.objects.using(using).bulk_create(perms, ignore_conflicts=True)
    if verbosity >= 2:
        for perm in perms:
            print(f"Adding saas_base.Permission '{perm.name}'")
