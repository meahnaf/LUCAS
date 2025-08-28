type SiteInformation = {
  id: string;
  displayName: string;
  location: string;
};
type TenantSiteMapping = {
  [tenantId: string]: SiteInformation[];
};

/**
 * Tenant Site Mapping
 *
 * @type {{ lucas: { id: string; displayName: string; location: string; }; }}
 */
export const TENANT_SITE_MAPPING: TenantSiteMapping = {
  lucas: [
    {
      id: 'chinchinmelbourne',
      displayName: 'CHINCHIN MELBOURNE',
      location: 'Melbourne',
    },
    {
      id: 'chinchinsydney',
      displayName: 'CHINCHIN SYDNEY',
      location: 'Sydney',
    },
    {
      id: 'grillamericano',
      displayName: 'GRILL AMERICANO',
      location: 'Melbourne',
    },
    {
      id: 'society',
      displayName: 'SOCIETY',
      location: 'Melbourne',
    },
    {
      id: 'lillian',
      displayName: 'LILLIAN',
      location: 'Melbourne',
    },
    {
      id: 'yakimono',
      displayName: 'YAKIMONO',
      location: 'Melbourne',
    },
    {
      id: 'babypizza',
      displayName: 'BABY PIZZA',
      location: 'Melbourne',
    },
    {
      id: 'hawkerhall',
      displayName: 'HAWKER HALL',
      location: 'Melbourne',
    },
    {
      id: 'kisume',
      displayName: 'KISUME',
      location: 'Melbourne',
    },
    {
      id: 'tomboden',
      displayName: 'TOMBO DEN',
      location: 'Melbourne',
    },
    {
      id: 'maisonbatard',
      displayName: 'MAISON BÂTARD',
      location: 'Melbourne',
    },
    {
      id: 'global',
      displayName: 'HEAD OFFICE',
      location: 'Melbourne',
    },
  ],
};

/**
 * Tenant Site Mapping as Object
 * Each tenant will have a mapping of site id to site name
 *
 * @type {{ lucas: Record<string, string>; }}
 */
export const TENANT_SITE_MAPPING_AS_OBJECT: {
  [tenantId: string]: Record<string, string>;
} = Object.fromEntries(
  Object.entries(TENANT_SITE_MAPPING).map(([tenantId, sites]) => [
    tenantId,
    Object.fromEntries(sites.map(({ id, displayName }) => [id, displayName])),
  ]),
);