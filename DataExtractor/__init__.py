from Utils import Config
from .extractor import extract_data
import asyncio
import os
import json
import csv
import re

def readable_json(json_str):
    # Remove leading/trailing whitespace and ensure it's a valid JSON string
    try:
        # Try loading the string directly
        return json.loads(json_str)
    except json.JSONDecodeError:
        # If it fails, try to fix common issues (like trailing commas)
        # Remove trailing commas before closing braces/brackets
        fixed_str = re.sub(r',(\s*[}\]])', r'\1', json_str.strip())
        return json.loads(fixed_str)


def _write_to_csv(counter: int, schema: dict, data: list[dict], output_dir)->str:
    field_names = list(schema.keys())
    print(f"Processing schema index {counter} with fields: {field_names}")
    csv_path = os.path.join(output_dir, f"schema_{counter}.csv")
    print(f"Writing to CSV: {csv_path}")
    with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)
    print(f"Finished writing {csv_path}")
    return csv_path

def write_to_csv(schemas: list[str], schema_data: dict, config: Config):
    print("Starting to write CSV files...")
    csv_files = []
    csv_writer_func = _write_to_csv
    if config.extractor['csvWriter'] and callable(config.extractor['csvWriter']):
        csv_writer_func = config.extractor['csvWriter']

    output_dir = os.path.join(config.tempDir, config.extractor['csvDir'])
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory for CSVs: {output_dir}")
    json_schema = []
    for idx, schema in enumerate(schemas):
        try:
            json_obj = readable_json(schema)[0]
        except:
            error_path = os.path.join(output_dir, f"schema_{idx}_error.json")
            with open(error_path, "w", encoding="utf-8") as errorfile:
                json.dump(
                    {
                        "schema": schema},
                    errorfile,
                    ensure_ascii=False,
                    indent=2
                )
            json_obj = {}
            pass
        json_schema.append(json_obj)

    for idx, data_list in schema_data.items():
        schema = json_schema[idx]
        all_data = []
        if not schema:
            data_path = os.path.join(output_dir, f"Data{idx}.json")
            with open(error_path, "w", encoding="utf-8") as errorfile:
                json.dump(
                    {
                        "data": data_list,
                    },
                    errorfile,
                    ensure_ascii=False,
                    indent=2
                )
            print(f"Failed  schema at index {idx}. Data  written to {data_path}")
            continue
        
        for json_object_list in data_list:
            all_data.extend( json_object_list )

        csv_files.append(csv_writer_func( idx, schema, all_data, output_dir ))

    print("All CSV files written.")
    return csv_files

def extract_data_from_html(files: list[str], schemas: list[str], config: Config):
    print("Starting data extraction from HTML files...")
    data = asyncio.run(extract_data(files, schemas, config.extractor['contextLength'], config.extractor['concurrentExtractions'], config.dumpFile))
    print("Extraction complete.")
    if config.extractor['csvDir']:
        print("CSV directory specified, writing extracted data to CSV files.")
        return write_to_csv(schemas, data, config)
    print("Returning extracted data as dictionary.")
    return data