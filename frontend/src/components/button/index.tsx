import React from 'react';
import { Button } from 'antd';

import { buttonType } from './type';

/**
 * CustomButton component for rendering a button with optional loading and icon states.
 *
 * @component
 * @param {Object} props - Component properties.
 * @param {boolean} props.loading - Determines whether the button should display a loading spinner.
 * @param {React.ReactNode} [props.icon] - An optional icon to be displayed on the button.
 * @param {string} [props.placeholder=""] - Text or label displayed inside the button.
 * @param {string} props.type - The type of button (e.g., "primary", "default", "dashed", "link", etc.).
 * @param {string} props.size - The size of the button (e.g., "large", "middle", "small").
 * @param {Function} props.onClick - Callback function triggered when the button is clicked.
 *
 * @returns {JSX.Element} The CustomButton component.
 */
function CustomButton({
  loading,
  icon,
  placeholder = '',
  type,
  size,
  onClick,
}: buttonType) {
  return (
    <Button 
      icon={icon} 
      loading={loading} 
      type={type} 
      size={size} 
      onClick={() => onClick()} 
      className="w-full"
    >
      {placeholder}
    </Button>
  );
}

export default CustomButton;
