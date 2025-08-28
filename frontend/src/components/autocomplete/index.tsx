import { Select } from 'antd';

import { AutoCompleteType } from './types';

/**
 * AutoComplete component for providing a searchable dropdown with options.
 *
 * @component
 * @param {Object} props - Component properties.
 * @param {Array<{label: string, value: string | number}>} props.options - List of options to display in the dropdown. 
 * Each option should have a `label` (display text) and a `value` (unique identifier).
 * @param {string | number} [props.defaultValue] - The default selected value in the dropdown.
 * @param {string} [props.placeholder] - Placeholder text displayed when no value is selected.
 * @param {Function} props.onChange - Callback function triggered when the selected value changes.
 * Receives the selected value as an argument.
 *
 * @returns {JSX.Element} The AutoComplete component.
 *
 */
function AutoComplete({
  options,
  placeholder,
  onChange,
}: AutoCompleteType) {
  // Map options to Ant Design's expected format
  const formattedOptions = options.map(option => ({
    label: option.displayName, // Use displayName as the label
    value: option.id,         // Use id as the value
  }));

  return (
    <Select
      showSearch
      placeholder={placeholder}
      size="large"
      defaultValue={formattedOptions[0]?.value} // Ensure it uses value from formatted options
      optionFilterProp="label"
      className="w-full"
      filterSort={(optionA, optionB) =>
        (optionA?.label ?? '').toLowerCase().localeCompare((optionB?.label ?? '').toLowerCase())
      }
      options={formattedOptions} // Pass the formatted options
      onChange={onChange}
    />
  );
}

export default AutoComplete;


