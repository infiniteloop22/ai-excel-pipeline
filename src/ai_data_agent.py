import pandas as pd
import ollama
from pydantic import BaseModel
import typing

class SortProcess(BaseModel):
    reasoning: str

def read_excel_file(file_path):
    return pd.read_excel(file_path)

def query_model(prompt, df):
    with open(prompt, 'r', encoding="utf-8") as file:
        content = file.read()

    '''
    columns_and_types = df.dtypes.to_string()
    sample_rows = df.head(3).to_string()

    df_context_string = f"""
    DATASET COLUMNS & TYPES:
    {columns_and_types}

    SAMPLE ROWS:
    {sample_rows}
    """

    final_content = content.format(df=df_context_string)
    '''

    response = ollama.chat(
        model='llama3.2:1b',
        messages=[{'role': 'user', 'content': final_content}],
        format=SortProcess.model_json_schema()
        #stream=True
        #options={"keep_alive": 0}
    )

    output = response['message']['content']
    with open('model_output.txt', 'w') as file:
        file.write(output)
    print("written to file model_output.txt ..")

def get_columns(dataframe):
    return dataframe.columns.to_list()

def sort_data(dataframe, columns):
    return dataframe.sort_values(by=columns)

def write_excel_file(file_path, processed_data):
    processed_data.to_excel(file_path, index=False)
    print(f"\nWritten to {file_path}..")

def process_data(input_file, output_file, user_request):
    df = read_excel_file(input_file)

    #query = query_model()
    query = query_model("src/prompt.txt", df)
    #columns = get_columns(df)
    #sorted_data = sort_data(df, columns)
    #write_excel_file(output_file, sorted_data)

def main():
    with open("src/files.txt", 'r') as files:
        files = files.readlines()
    while files: # while not empty list
        input_file = files.pop().strip() # removes whitespaces and newline characters
        output_file = input_file
        user_request = "Show me significant data from the file."
        process_data(input_file, output_file, user_request)

    print("\nFinished!")

if __name__ == "__main__":
    main()