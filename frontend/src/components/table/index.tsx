import React from "react";
import { Space, Table, Button, message } from "antd";
import { DownloadOutlined, DeleteOutlined } from "@ant-design/icons";

import { BASE_URL } from "../../constants/configuaration";
import { rowType } from "./type";

interface DocumentTableProps {
  rows: rowType[];
  selectedSite: string;
  onFileDelete: (fileName: string) => void;
}

const downloadFiles = async (selectedSite: string, selectedFiles: string[]) => {
  try {
    const response = await fetch(`${BASE_URL}/directories/${selectedSite}/download`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ selected_files: selectedFiles }),
    });

    if (!response.ok) {
      throw new Error(`Download failed: ${response.statusText}`);
    }

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = `${selectedFiles[0].toLowerCase()}.zip`;
    link.click();
    window.URL.revokeObjectURL(downloadUrl);
    message.success("File downloaded successfully.");
  } catch (error: any) {
    console.error("Error downloading files:", error);
    message.error(`Error downloading files: ${error.message}`);
  }
};

const deleteFiles = async (selectedSite: string, selectedFiles: string[]) => {
  try {
    const response = await fetch(`${BASE_URL}/directories/${selectedSite}/delete`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        selected_files: selectedFiles,
        directory_name: selectedSite,
      }),
    });

    if (!response.ok) {
      throw new Error(`Deletion failed: ${response.statusText}`);
    }

    const result = await response.json();
    message.success("File deleted successfully.");
    return result;
  } catch (error: any) {
    console.error("Error deleting files:", error);
    message.error(`Error deleting files: ${error.message}`);
    throw error;
  }
};

const DocumentTable: React.FC<DocumentTableProps> = ({ rows, selectedSite, onFileDelete }) => {
  const handleDownload = async (record: rowType) => {
    const selectedFiles = [record.name];
    await downloadFiles(selectedSite, selectedFiles);
  };

  const handleDelete = async (record: rowType) => {
    const selectedFiles = [record.name];
    try {
      await deleteFiles(selectedSite, selectedFiles);
      onFileDelete(record.name); // Remove the deleted file from the table
    } catch {
      // Error already handled in deleteFiles
    }
  };

  return (
    <Table<rowType> dataSource={rows} rowKey="name">
      <Table.Column title="Document Name" dataIndex="name" key="name" />
      <Table.Column title="Size" dataIndex="size" key="size" />
      <Table.Column title="Last Modified Date" dataIndex="last_modified" key="last_modified" />
      <Table.Column
        title="Actions"
        key="actions"
        render={(_, record: rowType) => (
          <Space size="middle">
            <Button
              icon={<DownloadOutlined />}
              onClick={() => handleDownload(record)}
            />
            <Button
              icon={<DeleteOutlined />}
              onClick={() => handleDelete(record)}
              danger
            />
          </Space>
        )}
      />
    </Table>
  );
};

export default DocumentTable;
