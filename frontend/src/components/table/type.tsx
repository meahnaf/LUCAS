/**
 * Represents the data for a single row in a table or list.
 * 
 * @typedef {Object} rowType
 * @property {string} size - The size of the item (e.g., file size, or any other measurement unit).
 * @property {string} name - The name or title of the item (e.g., file name, row title).
 * @property {string} last_modified - The timestamp indicating when the item was last modified, in string format (e.g., ISO string, or any date format).
 */
export type rowType = {
    size: string;
    name: string;
    last_modified: string;
  };
  