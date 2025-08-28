import React from "react";
import { Segmented } from "antd";
import { useNavigate } from "react-router-dom";
import { FolderOutlined, RobotOutlined } from "@ant-design/icons";

function TabBar() {
  const navigate = useNavigate();
  const handleOnChange = (option: string) => {
    navigate(`/home/${option}`);
  };
  return (
    <Segmented
      defaultValue="chat"
      cellSpacing="100px"
      options={[
        { label: "Chat", value: "chat", icon: <RobotOutlined /> },
        { label: "Directory", value: "directory", icon: <FolderOutlined /> },
      ]}
      block
      onChange={(value) => handleOnChange(value)}
    />
  );
}

export default TabBar;
