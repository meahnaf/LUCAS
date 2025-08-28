/**
 * Represents the properties for a custom button component.
 * 
 * @typedef {Object} buttonType
 * @property {string} [placeholder] - Optional placeholder text that can be displayed on the button (for certain button types).
 * @property {boolean} loading - A flag indicating whether the button is in a loading state.
 * @property {React.ReactNode} [icon] - An optional icon to display alongside the button content.
 * @property {'small' | 'middle' | 'large'} size - The size of the button, can be 'small', 'middle', or 'large'.
 * @property {'link' | 'text' | 'default' | 'primary' | 'dashed' | undefined} type - The button's style type, determining its appearance.
 * @property {() => void} onClick - A function to handle the button's click event.
 */
export type buttonType = {
  placeholder?: string;
  loading: boolean;
  icon?: React.ReactNode;
  size: 'small' | 'middle' | 'large';
  type: "link" | "text" | "default" | "primary" | "dashed" | undefined;
  onClick: () => void;
};
