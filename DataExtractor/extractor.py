import bs4
import asyncio
import json
import os
from AI import set_semaphore, get_data

def get_system_message() -> str:
    """
    Returns the system message that sets the model's behavior.
    """
    return """You are an intelligent data extractor.

Your task is to extract structured information from a webpage's text content. You have to strictly follow the provided schema as a guide. Sometimes its possible same field might not exist in the page but similar sounding field might exist, in that case you can use that field to fill the data.
No need to mention it, you can just use the field that is semantically close or commonly equivalent to the field in the schema. If you feel not all field data exists you can leave the field empty.
Return the extracted data in JSON format, adhering to the schema provided. Enclose the json output in ````json` tags to ensure proper formatting.
### Rules:
- Use only the fields defined in the schema.
- If the exact field name is not available, it's acceptable to substitute it with a semantically close or commonly equivalent field (e.g., if "name" is missing but "model" appears, use "model" for "name").
- Do not add new fields that are not part of the schema.
- If a field is not present or cannot be confidently extracted, omit it or leave it blank.
- Output should be a valid JSON object that follows the structure of the schema.
- Only include information that appears explicitly in the content."""

def create_prompt(schema: str, page_text: str) -> str:
    return f"""
Schema:
{json.dumps(schema, indent=2)}

Here is the page content:
\"\"\"
{page_text}
\"\"\"

Your task is to extract structured information from the webpage's text content, using the schema as a guide.
"""

def get_json(response: str, dumpFile):
    """
    Extracts the JSON part from the response string.
    The response is expected to be in the format:
    ```json
    { ... }
    ```
    This function will return the JSON content as a string.
    If extraction fails, dumps the response to 'failed_json_dump.txt'.
    """
    try:
        start = response.find('```json') + len('```json')
        end = response.find('```', start)
        json_str = response[start:end].strip()
        json_obj = json.loads(json_str)
        print("Successfully extracted JSON.")
        return json_obj
    except Exception as e:
        print(f"Failed to extract JSON: {e}")
        os.makedirs('.temp', exist_ok=True)
        if dumpFile:
            with open('.temp/failed_json_dump.txt', 'a', encoding='utf-8') as f:
                f.write("Failed to extract JSON:\n")
                f.write(response)
                f.write("\n\n")
        return None

def get_prompts(schema: str, page_content: str, context_length: int) -> list[str]:
    prompts = []
    for i in range(0, len(page_content), context_length):
        page_text = page_content[i:i + context_length]
        prompts.append(create_prompt(schema, page_text))
    print(f"Created {len(prompts)} prompts for schema.")
    return prompts

async def extract_data(files: list[str], schemas: list[str], context_length: int, concurrency: int, dumpFile = None):
    set_semaphore(concurrency)
    schema_data_map = {}

    async def process_prompt(file, schema, schema_idx, prompt):
        try:
            print(f"Processing prompt for file: {file}, schema index: {schema_idx}")
            response = await get_data(get_system_message(), prompt)
            if response:
                print(f"Received response for file: {file}, schema index: {schema_idx}")
                data = get_json(response, dumpFile)
                if schema_idx not in schema_data_map:
                    schema_data_map[schema_idx] = []
                if data:
                    schema_data_map[schema_idx].append(data)
                    print(f"Appended data for schema index: {schema_idx}")
                else:
                    print(f"No data extracted for file: {file}, schema index: {schema_idx}")
            else:
                print(f"No response for file: {file}, schema index: {schema_idx}")
        except Exception as e:
            print(f"Error processing file {file} with schema {schema}: {e}")

    tasks = []
    for file in files:
        print(f"Reading file: {file}")
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = bs4.BeautifulSoup(content, 'html.parser')
        page_text = soup.get_text(separator=' ', strip=True)
        for idx, schema in enumerate(schemas):
            prompts = get_prompts(schema, page_text, context_length)
            for prompt in prompts:
                tasks.append(asyncio.create_task(process_prompt(file, schema, idx, prompt)))

    print(f"Total tasks to run: {len(tasks)}")
    await asyncio.gather(*tasks)
    print("All tasks completed.")
    return schema_data_map