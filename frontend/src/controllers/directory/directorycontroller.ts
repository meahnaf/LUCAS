import { rowType } from "../../components/table/type";
import { BASE_URL } from "../../constants/configuaration";

export async function fetchFilesForDirectory(
  siteId: string
): Promise<rowType[]> {
  const apiUrl = `${BASE_URL}/directories/${siteId}/files`;

  try {
    const response = await fetch(apiUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch files: ${response.statusText}`);
    }

    const files = await response.json();

    const transformedFiles: rowType[] = files.map((file: any) => ({
      size: file.size.toString(),
      name: file.name,
      last_modified: file.last_modified,
    }));

    return transformedFiles;
  } catch (error) {
    console.error("Error fetching files:", error);
    throw new Error("Failed to retrieve files. Please try again later.");
  }
}
