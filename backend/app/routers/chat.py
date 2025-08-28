from fastapi import APIRouter, Response, status
from starlette.responses import StreamingResponse
import logging
from ..modules.ragRetrivalProcess import retrive_rag_info

router = APIRouter(prefix="/chat")

@router.get("/query/{siteid}/", tags=["query"])
async def query(siteid: str, message: str):
    """Chat completions API with internal data and streaming support.
    Args:
        siteid (str): site identifier.
        message (str): chat query from the user.
    Returns:
        Streaming response
    """
    try:
        if not message:
            return Response("Invalid message", status_code=status.HTTP_400_BAD_REQUEST)
        if not siteid:
            return Response("Invalid siteid", status_code=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve information using the RAG system (assuming this is already implemented)
        res_text = retrive_rag_info(message, siteid, "lucas")

        def message_generator():
            try:
                for chunk in res_text:
                    # Extract the content of the chunk (if it's not None)
                    content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta else ''
                    if content:  # Only yield non-empty content
                        # Send each chunk with the required 'data:' prefix and double newline
                        yield f"data: {content}\n\n"
                    else:
                        logging.warning("Empty content in chunk")
                
                # After all chunks are sent, indicate the stream is complete
                yield "data: [DONE]\n\n"
            
            except Exception as e:
                logging.error(f"Streaming error: {str(e)}")
                yield "data: Error occurred while streaming data.\n\n"
            finally:
                logging.info("Stream closed.")

        # Return a StreamingResponse with text/event-stream media type
        return StreamingResponse(message_generator(), media_type='text/event-stream')

    except Exception as e:
        logging.error(f"Error in chat query: {str(e)}")
        return Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
