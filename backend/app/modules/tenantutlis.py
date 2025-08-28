from config.tenant_site_mapping import tenant_site_mapping
from modules.constant import default_tenant_name


def get_site_id_by_display_name(display_name):
    """
    Retrieves the site ID by matching the display name in the tenant-site mapping.

    Args:
        display_name (str): The display name of the site.

    Returns:
        str: The site ID that corresponds to the given display name, or None if no match is found.
    """
    for site in tenant_site_mapping[default_tenant_name]:
        if site['displayName'] == display_name:
            return site['id']
    return None

def get_site_name_by_id(site_id):
    """
    Retrieves the tenant name by matching the site ID in the tenant-site mapping.

    Args:
        site_id (str): The ID of the site.

    Returns:
        str: The tenant name that corresponds to the given site ID, or None if no match is found.
    """
    for site in tenant_site_mapping[default_tenant_name]:
        if site['id'] == site_id:
            return site['displayName']
    return None
