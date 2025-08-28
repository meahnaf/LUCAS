import React, { useState } from 'react';
import { Upload, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';

import { BASE_URL } from '../../constants/configuaration';

const { Dragger } = Upload;

interface UploadAreaProps {
  siteId: string;
}

const handleUpload = async (file: File, siteId: string): Promise<void> => {
  const formData = new FormData();
  formData.append('uploaded_files', file); // Match backend parameter name

  try {
    const response = await fetch(`${BASE_URL}/directories/${siteId}/upload`, {
      method: 'POST',
      body: formData,
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Upload failed');
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
};

const UploadArea: React.FC<UploadAreaProps> = ({ siteId }) => {
  const [fileList, setFileList] = useState<any[]>([]);

  const props = {
    name: 'uploaded_files', // Match backend parameter name
    multiple: true,
    fileList, // Bind the fileList state to the component
    customRequest: async ({
      file,
      onSuccess,
      onError,
      onProgress,
    }: any) => {
      try {
        // Handle upload progress if needed
        onProgress?.({ percent: 50 });

        await handleUpload(file, siteId);
        onProgress?.({ percent: 100 });
        onSuccess?.('ok');
      } catch (error: any) {
        onError?.(error);
        message.error(`Failed to upload ${file.name}: ${error.message}`);
      }
    },
    onChange(info: any) {
      const { status, name } = info.file;

      if (status === 'done') {
        message.success(`${name} uploaded successfully.Please refresh the page`);

        // Clear the file list when all uploads are complete
        if (info.fileList.every((file: any) => file.status === 'done')) {
          setFileList([]); // Reset the file list
        }
      } else if (status === 'error') {
        message.error(`${name} upload failed.`);
      }

      // Update the file list state
      setFileList([...info.fileList]);
    },
  };

  return (
    <div className="upload-container">
      <Dragger {...props}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">
          Click or drag file to this area to upload
        </p>
        <p className="ant-upload-hint">
          Support for single or bulk upload. Strictly prohibited from uploading
          company data or other banned files.
        </p>
      </Dragger>
    </div>
  );
};

export default UploadArea;
