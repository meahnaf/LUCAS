/**
 * Represents the configuration options for a text input field.
 * 
 * @typedef {Object} textFieldType
 * @property {string} [placeholder] - The placeholder text displayed in the input field when it is empty.
 * @property {'large' | 'middle' | 'small'} [size] - The size of the input field, which can be 'large', 'middle', or 'small'.
 * @property {string} [value] - The current value of the input field.
 * @property {(event: React.ChangeEvent<HTMLInputElement>) => void} [onChange] - A callback function that handles the change event when the user types in the input field.
 */
export type textFieldType = {
    placeholder?: string;
    size?: 'large' | 'middle' | 'small';
    value?: string;
    onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  };
  