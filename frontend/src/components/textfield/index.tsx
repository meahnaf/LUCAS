import React from 'react';
import { Input } from 'antd';

import { textFieldType } from './type';

/**
 * TextField component that renders an input field with customizable size, placeholder, value, and change handler.
 *
 * @component
 * @param {Object} props - Component properties.
 * @param {string} props.placeholder - The placeholder text for the input field.
 * @param {string} props.size - The size of the input field (e.g., 'small', 'middle', 'large').
 * @param {string} props.value - The value of the input field.
 * @param {function} props.onChange - The function to call when the input value changes.
 *
 * @returns {JSX.Element} The Input component with the provided properties.
 */


function TextField({ placeholder, size, value, onChange }: textFieldType) {
  return (
    <Input 
      size={size} 
      placeholder={placeholder} 
      onChange={onChange} 
      className='w-full' 
      value={value}
    />
  );
}

export default TextField;
