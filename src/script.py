import ollama
import pandas as pd
from pydantic import BaseModel, Field

class SortConfiguration(BaseModel):
    columns_to_sort_by: list[str] = Field(description="A list of string column names to sort the DataFrame by, in order of priority.")
    reasoning: str = Field(description="The model's step-by-step reasoning explaining why these columns were selected.")

def read_excel_file(file_path):
    return pd.read_excel(file_path)

def query_model(df, user_request):
    with open('src/prompt.txt', 'r') as file:
        content = file.read()

    available_columns = df.columns.to_list()
    columns_and_types = df.dtypes.to_string()
    sample_rows = df.head(3).to_string()

    final_content = content.format(
        user_request=user_request,
        available_columns=available_columns,
        columns_and_types=columns_and_types,
        sample_rows=sample_rows
    )

    response = ollama.chat(
        model='llama3.2:1b',
        messages=[{'role': 'user', 'content': final_content}],
        format=SortConfiguration.model_json_schema()
    )

    output = response['message']['content']
    
    with open('src/model_output.txt', 'w') as file:
        file.write(output)
    print("\nWritten to file model_output.txt ..")

    structured_data = SortConfiguration.model_validate_json(output)
    return structured_data

def sort_data(dataframe, columns):
    return dataframe.sort_values(by=columns)

def write_excel_file(file_path, processed_data):
    processed_data.to_excel(file_path, index=False)
    print(f"\nWritten to {file_path}..")

def process_data(input_file, output_file, user_request):
    df = read_excel_file(input_file)
    sort_config = query_model(df, user_request)
    sorted_data = sort_data(df, sort_config.columns_to_sort_by)
    write_excel_file(output_file, sorted_data)

def main():
    with open('src/files.txt', 'r') as file:
        files = file.readlines()

    user_request = input("Specify how to sort the excel files.. ('Age', 'Annual Salary'): ")
    if not user_request:
        user_request = "Sort the spreadsheet by the most important columns."
        
    while files: 
        input_file = files.pop().strip()
        if not input_file:
            continue
            
        output_file = input_file
        process_data(input_file, output_file, user_request)

    print("\nDone")

if __name__ == "__main__":
    main()
