import { StatusCodes } from "http-status-codes";
import { BASE_URL } from "../../constants/configuaration";

/**
 * Interface representing the response structure from the chat API.
 * @typedef {Object} ChatResponse
 * @property {number} status - The status code of the response.
 * @property {string} message - The message or content of the response.
 */
interface ChatResponse {
  status: number;
  message: string;
}

/**
 * Subscribes to the chat API to query chat completions based on the provided branchId and prompt.
 *
 * @param {string} branchId - The unique identifier for the branch.
 * @param {string} prompt - The message or query to send to the chat API.
 * @param {Function} onMessage - Callback function to handle the stream message.
 */
const chatPostController = (
  branchId: string,
  prompt: string,
  onMessage: (message: string, statusCode: number) => void
): void => {
  if (!prompt.trim() || !branchId.trim()) {
    onMessage(
      !prompt.trim() ? "Invalid message" : "Invalid site ID",
      StatusCodes.BAD_REQUEST
    );
    return;
  }

  try {
    // Construct the URL with query parameters
    const url = new URL(`${BASE_URL}/chat/query/${branchId}`);
    url.searchParams.append("message", prompt);

    const eventSource = new EventSource(url.toString());

    eventSource.onmessage = (event) => {
      try {
        const data = event.data;

        if (data === "[DONE]") {
          eventSource.close();
          console.log("Stream completed");
          // onMessage("Stream completed", StatusCodes.OK); // Notify completion to the frontend
          return;
        }

        // Ensure we're handling valid JSON or text messages correctly
        const parsedData = isValidJson(data) ? (JSON.parse(data) as ChatResponse) : { message: data, status: StatusCodes.OK };
        
        onMessage(parsedData.message, parsedData.status);
      } catch (error) {
        console.error("Error processing message:", error);
        onMessage("Error processing the stream.", StatusCodes.INTERNAL_SERVER_ERROR);
        eventSource.close();
      }
    };

    eventSource.onerror = (error) => {
      console.error("Stream error:", error);
      // Check if the readyState is not OPEN, indicating an error in the stream
      if (eventSource.readyState !== EventSource.OPEN) {
        onMessage("Error occurred while fetching data.", StatusCodes.INTERNAL_SERVER_ERROR);
      }
      eventSource.close();
    };
  } catch (error) {
    console.error("Error in chat query:", error);
    onMessage("Something went wrong on our end. Please try again.", StatusCodes.INTERNAL_SERVER_ERROR);
  }
};

/**
 * Helper function to check if a string is valid JSON.
 * @param {string} str - The string to check.
 * @returns {boolean} - Whether the string is valid JSON.
 */
const isValidJson = (str: string): boolean => {
  try {
    JSON.parse(str);
    return true;
  } catch {
    return false;
  }
};

export default chatPostController;
