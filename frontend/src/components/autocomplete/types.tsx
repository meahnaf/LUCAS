/**
 * Represents an option in the autocomplete dropdown.
 * 
 * @interface AutoCompleteOptionType
 * @property {string} id - The unique identifier for the option.
 * @property {string} displayName - The name to display for the option.
 * @property {string} location - The location or category associated with the option.
 */
export interface AutoCompleteOptionType {
  id: string;
  displayName: string;
  location: string;
}

/**
 * Represents the configuration and behavior for the autocomplete component.
 * 
 * @interface AutoCompleteType
 * @property {AutoCompleteOptionType[]} options - The list of options available in the autocomplete dropdown.
 * @property {string} placeholder - The placeholder text displayed in the input field.
 * @property {(value: string) => void} onChange - A callback function triggered when the input value changes.
 */
export interface AutoCompleteType {
  options: AutoCompleteOptionType[];
  placeholder: string;
  onChange: (value: string) => void;
}
