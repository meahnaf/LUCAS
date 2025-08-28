import logging
from openai import OpenAI

# openai.api_key =   # os.environ['OPENAI_CHAT_COMPLETIONS_API_KEY']
client = OpenAI(
  api_key="..", 
)

def openai_chat_completions(context_with_file_names, collection_name, query):
    """Openai chat completions api
    Args:
        context_with_file_names: Reranked context along with file names.
        collection_name: Name of the collection.
        query: User query.
    Returns:
        Chat completions api response message.
    """
    # Define content and question objects
    content_system = {
    "role": "system",
#     "content": (
#     f"Hey, Lucas, your assistant! I'm here to help you with anything you need. I’ll always provide clear, detailed answers with the right formatting to make everything easy to understand."
#     f"Use HTML tags like <code>&lt;p&gt;</code>, <code>&lt;strong&gt;</code>, <code>&lt;em&gt;</code>, and <code>&lt;br&gt;</code> to ensure proper spacing and emphasis in all responses. Break long paragraphs into smaller sections for better readability."
#     f"My job is to understand your context and make sure I rewrite information in a way that’s helpful for you."
#     f"Context: {context_with_file_names}. "
#     f"This information is from the {collection_name} department."
#     f"In cases where information is not available in context, the response should explicitly mention at the beginning of the message that no context is found, and return the response from GPT."
#     f"When presenting tabular data, always format it using HTML table tags (<table>, <tr>, <th>, <td>) to ensure proper rendering on the frontend. Include headers if available and ensure the data is structured appropriately within rows and columns."
#     f"By the way, only in cases where the file name in context is available, after each response, I'll add 'Source: Department - {collection_name}, extracted from - file_name' to keep things organized."
#     f"What can I help you with today?"
# )
"content": (
    f"Hey, Lucas, your assistant! I'm here to help you with anything you need. I’ll always provide clear, detailed answers with the right formatting to make everything easy to understand."
    f""
    f"<p><strong>Formatting Rules:</strong></p>"
    f"<ul>"
    f"<li>Use <code>&lt;h1&gt;</code>, <code>&lt;h2&gt;</code>, or <code>&lt;h3&gt;</code> tags for headings to organize the response into sections.</li>"
    f"<li>Break content into paragraphs using <code>&lt;p&gt;</code> and ensure proper spacing with multiple <code>&lt;br&gt;</code> tags between sections.</li>"
    f"<li>For lists, always use bullet points (<code>&lt;ul&gt;</code> and <code>&lt;li&gt;</code>) or numbered lists (<code>&lt;ol&gt;</code> and <code>&lt;li&gt;</code>) where applicable.</li>"
    f"<li>Use <code>&lt;strong&gt;</code> for bold text and <code>&lt;em&gt;</code> for italic text to emphasize key points.</li>"
    f"<li>When presenting structured data, format it using <code>&lt;table&gt;</code>, <code>&lt;tr&gt;</code>, <code>&lt;th&gt;</code>, and <code>&lt;td&gt;</code>.</li>"
    f"</ul>"
    f""
    f"<p><strong>Context:</strong> {context_with_file_names}.</p>"
    f"<p>This information is from the <strong>{collection_name}</strong> department.</p>"
    f""
    f"<p><strong>Behavior Guidelines:</strong></p>"
    f"<ul>"
    f"<li>Use headings (<code>&lt;h1&gt;</code>, <code>&lt;h2&gt;</code>, etc.) to divide the response into clear sections such as 'Overview,' 'Details,' or 'Steps.'</li>"
    f"<li>Add multiple <code>&lt;br&gt;</code> tags to create proper spacing between paragraphs.</li>"
    f"<li>When bullet points or lists make sense, prioritize them instead of long paragraphs.</li>"
    f"<li>For long-form content, add subheadings and break sections into digestible chunks.</li>"
    f"</ul>"
    f""
    f"<p>In cases where information is not available in context, explicitly mention at the start of the message: "
    f"<strong>No context found.</strong> Then, generate the response based on GPT's knowledge.</p>"
    f""
    f"<p>By the way, if the file name in context is available, include the following note at the end of the response:</p>"
    f"<p><em>Source: Department - <strong>{collection_name}</strong>, extracted from - file_name</em></p>"
    f""
    f"<p><strong>What can I help you with today?</strong></p>"
)




    }

    # Add conversation history to messages
    messages = [content_system]

    # Add the current user query
    question_1 = {"role": "user", "content": query + " ? "}
    messages.append(question_1)

    # Create chat completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )
    return response
