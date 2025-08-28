import React, { useState } from "react";
import Markdown from "react-markdown";
import { BeatLoader } from "react-spinners";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { CopyOutlined, CheckOutlined } from "@ant-design/icons";

import { chatType } from "./types";

/**
 * ChatBox component that displays chat messages, handles loading state, and allows copying message content.
 *
 * @component
 * @param {Object} props - Component properties.
 * @param {string} props.content - The content of the chat message to be displayed.
 * @param {boolean} props.chatBot - Flag indicating whether the message is from the chat bot.
 * @param {boolean} props.isLoading - Flag indicating whether the content is still loading.
 *
 * @returns {JSX.Element} The ChatBox component, rendering a chat message with optional loading state and copy functionality.
 */

function ChatBox({ content, chatBot, isLoading }: chatType) {
  const [isCopied, setIsCopied] = useState(false);

  /**
   * Handles the copy action, copying the content to the clipboard.
   */
  const handleCopy = () => {
    navigator.clipboard
      .writeText(content)
      .then(() => {
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
      })
      .catch((err) => {
        console.error("Failed to copy: ", err);
      });
  };

  const renderAvatar = () => {
    if (chatBot) {
      return (
        <img
          src={`/assets/nexlogo.png`}
          alt="Nexzap Logo"
          className="w-6 h-6 object-cover rounded-lg flex-shrink-0 border p-1 mr-3"
        />
      );
    }
    return null;
  };

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="flex items-center space-x-2 p-1">
          <BeatLoader size={8} color="#1677ff" />
        </div>
      );
    }
    if (chatBot) {
      return (
        <Markdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
          className="dark:text-white text-sm sm:text-base"
          components={{
            table: ({ node, ...props }) => (
              <div className="overflow-x-auto">
                <table
                  {...props}
                  className="table-auto border-collapse rounded-lg w-full text-sm sm:text-base"
                >
                  {props.children}
                </table>
              </div>
            ),
            th: ({ node, ...props }) => (
              <th
                {...props}
                className="px-0 py-1 border rounded-lg bg-gray-50 dark:bg-neutral-800 font-medium text-sm sm:text-base"
              />
            ),
            td: ({ node, ...props }) => (
              <td
                {...props}
                className="px-2 py-2 border rounded-lg text-sm sm:text-base"
              />
            ),
            tr: ({ node, ...props }) => (
              <tr
                {...props}
                className="border-b last:border-none rounded-lg text-sm sm:text-base"
              />
            ),
          }}
        >
          {content}
        </Markdown>
      );
    }
    return <span className="text-sm sm:text-base">{content}</span>;
  };

  const renderCopyButton = () => {
    if (chatBot && !isLoading) {
      return (
        <button
          className="bottom-0 left-2 p-1 rounded-full border-none"
          onClick={handleCopy}
        >
          {isCopied && !isLoading ? (
            <CheckOutlined style={{ color: "#52c41a" }} />
          ) : (
            <CopyOutlined style={{ color: "#8c8c8c" }} />
          )}
        </button>
      );
    }
    return null;
  };

  return (
    <div
      className={`flex ${
        chatBot ? "justify-start" : "justify-end"
      } w-full h-auto items-start space-x-2`}
    >
      {renderAvatar()}
      <div
        className={`rounded-md ${
          chatBot
            ? "p-0 relative"
            : "bg-gray-50 dark:bg-neutral-800 dark:text-white p-3"
        } w-auto`}
      >
        {renderContent()}
        {renderCopyButton()}
      </div>
    </div>
  );
}

export default ChatBox;
