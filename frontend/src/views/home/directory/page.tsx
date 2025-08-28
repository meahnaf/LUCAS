import { useState, useEffect } from "react";
import { DatabaseOutlined } from "@ant-design/icons";

import AutoComplete from "../../../components/autocomplete";
import CustomTable from "../../../components/table";
import { rowType } from "../../../components/table/type";
import UploadArea from "../../../components/uploadarea";
import { TENANT_ID } from "../../../constants/configuaration";
import { fetchFilesForDirectory } from "../../../controllers/directory/directorycontroller";
import { TENANT_SITE_MAPPING } from "../chat/tenantSiteMapping";

function DirectoryView() {
  const [filesData, setFilesData] = useState<{ rows: rowType[] }>({ rows: [] });
  const [selectedSite, setSelectedSite] = useState<string>(TENANT_SITE_MAPPING[TENANT_ID][0].id);

  // Fetch files when the selected site changes
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const files = await fetchFilesForDirectory(selectedSite);
        setFilesData({ rows: files });
      } catch (error) {
        console.error("Error fetching files:", error);
        setFilesData({ rows: [] });
      }
    };

    fetchFiles();
  }, [selectedSite]);

  
  // Handle file deletion: Remove the deleted file from the state
  const handleFileDelete = (deletedFile: string) => {
    setFilesData((prevData) => ({
      rows: prevData.rows.filter((file) => file.name !== deletedFile),
    }));
  };

  return (
    <div className="flex flex-col items-center">
      <div className="md:w-1/2 w-full md:p-0 p-4 space-y-5 flex flex-col mt-5">
        <AutoComplete
          placeholder="Branch"
          options={TENANT_SITE_MAPPING[TENANT_ID]}
          onChange={(value) => setSelectedSite(value)}
        />
        <div className="w-full">
          <UploadArea siteId={selectedSite} />
        </div>
        <div className="p-2 bg-neutral-50 dark:bg-neutral-800 rounded-md">
          <div className="flex flex-row space-x-2 dark:text-white">
            <DatabaseOutlined />
            <div className="dark:text-white">Database</div>
          </div>
        </div>
        <CustomTable
          rows={filesData.rows}
          selectedSite={selectedSite}
          onFileDelete={handleFileDelete}
        />
      </div>
    </div>
  );
}

export default DirectoryView;
