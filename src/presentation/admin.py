import sqlmodel
from fastapi_amis_admin.admin import settings as auth_settings
from fastapi_user_auth import admin

from infrastructire import settings as app_settings

site = admin.AuthAdminSite(
    settings=auth_settings.Settings(
        database_url="sqlite:///amisadmin.db?check_same_thread=False",
        site_title=app_settings.app_name,
        version=app_settings.version,
        language="Python",
        debug=app_settings.debug,
    )
)
auth = site.auth


async def create_admin_user():
    await site.db.async_run_sync(sqlmodel.SQLModel.metadata.create_all, is_session=False)
    # Creates a default administrator, username: admin, password: admin, please change the password in time!!!
    await auth.create_role_user("admin")
    # Creates the default super administrator, username: root, password: root, please change the password in time!!!
    await auth.create_role_user("root")
    # Run the startup method of the site, load the casbin strategy, etc.
    await site.router.startup()
    # Add a default casbin rule
    if not auth.enforcer.enforce("u:admin", site.unique_id, "page", "page"):
        await auth.enforcer.add_policy("u:admin", site.unique_id, "page", "page", "allow")
