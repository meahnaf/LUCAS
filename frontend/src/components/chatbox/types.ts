/**
 * Represents the properties for a chat message in the chat component.
 * 
 * @typedef {Object} chatType
 * @property {boolean} chatBot - A flag indicating whether the message is from the chat bot (true) or a user (false).
 * @property {string} content - The content of the chat message to be displayed.
 * @property {boolean} [isLoading] - An optional flag indicating whether the chat content is still loading. If not provided, defaults to false.
 */
export type chatType = {
  chatBot: boolean;
  content: string;
  isLoading?: boolean;
};
