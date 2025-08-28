import React, { useState, useCallback } from "react";
import { ArrowUpOutlined } from "@ant-design/icons";

import AutoComplete from "../../../components/autocomplete";
import CustomButton from "../../../components/button";
import ChatBox from "../../../components/chatbox";
import { chatType } from "../../../components/chatbox/types";
import TextField from "../../../components/textfield";
import { TENANT_ID } from "../../../constants/configuaration";
import chatPostController from "../../../controllers/chat/chatcontroller";
import { TENANT_SITE_MAPPING } from "./tenantSiteMapping";

function ChatView() {
  const [chatData, setChatData] = useState<chatType[]>([
    {
      chatBot: true,
      content: "Hello! I'm here to help you. What can I assist you with today?",
      isLoading: false,
    },
  ]);
  const [loading, setLoading] = useState<boolean>(false);
  const [branch, setBranch] = useState<string>(TENANT_SITE_MAPPING[TENANT_ID][0].id);
  const [prompt, setPrompt] = useState<string>("");

  // handle message submission
  const handleSubmit = useCallback(async () => {
    if (!prompt.trim()) return;

    // Add the user's message to the chat data
    const newUserMessage: chatType = { chatBot: false, content: prompt };
    setChatData((prevData) => [...prevData, newUserMessage]);

    // Add a temporary loading message for the chatbot
    const loadingMessage: chatType = { chatBot: true, content: "", isLoading: true };
    setChatData((prevData) => [...prevData, loadingMessage]);

    setLoading(true);

    // Start the streaming request to backend
    chatPostController(branch, prompt, (message: string) => {
      
      if (message) {
        // Update the loading message with real-time content from the response
        setChatData((prevData) => {
          const updatedData = [...prevData];
          updatedData[updatedData.length - 1] = {
            ...updatedData[updatedData.length - 1],
            content: updatedData[updatedData.length-1].content + message,
            isLoading: false,
          };
          return updatedData;
        });
      }
    });

    setLoading(false);
    setPrompt(""); // Reset prompt input after submission
  }, [prompt, branch]);

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex flex-col h-full items-center">
      <div
        className={`flex-1 ${chatData.length === 0 ? "overflow-y-hidden" : "overflow-y-auto"} p-5 md:w-6/12 w-full mx-auto`}
      >
        <div className="flex flex-col space-y-8 w-full">
          {chatData.map((chat, index) => (
            <div key={index} className={`flex ${chat.chatBot ? "justify-start" : "justify-end"}`}>
              <div className="w-3/4">
                <ChatBox
                  chatBot={chat.chatBot}
                  content={chat.content}
                  isLoading={chat.isLoading}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="md:w-6/12 w-full p-4">
        <div className="mx-auto flex md:flex-row flex-col md:space-x-3 space-y-3 md:space-y-0 items-center justify-center">
          <div className="md:w-4/12 w-full">
            <AutoComplete
              placeholder="Select Branch"
              options={TENANT_SITE_MAPPING[TENANT_ID]}
              onChange={(value: string) => setBranch(value)}
            />
          </div>
          <div className="md:w-8/12 w-full flex flex-row space-x-3">
            <div className="rounded-lg w-full">
              <TextField
                placeholder="Ask a question"
                size="large"
                value={prompt}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPrompt(e.target.value)}
              />
            </div>
            <div className="flex-shrink-0">
              <CustomButton
                loading={loading}
                size="large"
                type="primary"
                icon={<ArrowUpOutlined />}
                onClick={handleSubmit}
              />
            </div>
          </div>
        </div>
        <div className="text-center text-gray-400 mt-1 text-sm">
          AI can make mistakes. Always verify important info.
        </div>
      </div>
    </div>
  );
}

export default ChatView;
