import os
import pandas as pd
import logging
from constants import COUNTRY_TO_CONTINENT

def detect_delimiter(file_path):
    delimiters = [',', ';', '\t']
    counts = {delimiter: 0 for delimiter in delimiters}

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            sample = file.read(1024)  # Read a sample of the file
            for delimiter in delimiters:
                counts[delimiter] = sample.count(delimiter)
    except Exception as e:
        logging.error(f"Error detecting delimiter: {e}")

    return max(counts, key=counts.get)

def process_data(root_dir, exchange_rate_file, output_file):
    all_data = []
    required_columns = ['Transaction', 'Country', 'Currency', 'Client']
    total_csv_files = 0
    total_csv_read_success = 0
    total_excel_files = 0
    total_excel_read_success = 0

    if os.path.isdir(root_dir):
        logging.info(f"Accessing Year: {root_dir}")

        for month in os.listdir(root_dir):
            month_path = os.path.join(root_dir, month)
            if os.path.isdir(month_path):
                logging.info(f"  Accessing Month: {month}")
                for day in os.listdir(month_path):
                    day_path = os.path.join(month_path, day)
                    if os.path.isdir(day_path):
                        logging.info(f"    Accessing Day: {day}")
                        for file_name in os.listdir(day_path):
                            file_path = os.path.join(day_path, file_name)
                            logging.info(f"      Processing file: {file_name}")

                            try:
                                if file_name.endswith('.csv'):
                                    total_csv_files += 1
                                    delimiter = detect_delimiter(file_path)
                                    temp_data = pd.read_csv(file_path, nrows=0, sep=delimiter)
                                    available_columns = temp_data.columns
                                    logging.info(f"      Available columns in {file_name}: {list(available_columns)}")

                                    cols_to_use = [col for col in required_columns if col in available_columns]
                                    logging.info(f"      Columns to be used from {file_name}: {cols_to_use}")

                                    if cols_to_use:
                                        data = pd.read_csv(file_path, usecols=cols_to_use, sep=delimiter)
                                        data['day'] = day
                                        total_csv_read_success += 1
                                    else:
                                        logging.warning(f"      Skipping file {file_name}: No required columns found.")
                                        continue

                                elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                                    total_excel_files += 1
                                    temp_data = pd.read_excel(file_path, nrows=0)
                                    available_columns = temp_data.columns
                                    logging.info(f"      Available columns in {file_name}: {list(available_columns)}")

                                    cols_to_use = [col for col in required_columns if col in available_columns]
                                    logging.info(f"      Columns to be used from {file_name}: {cols_to_use}")

                                    if cols_to_use:
                                        data = pd.read_excel(file_path, usecols=cols_to_use)
                                        data['day'] = day
                                        total_excel_read_success += 1
                                    else:
                                        logging.warning(f"      Skipping file {file_name}: No required columns found.")
                                        continue

                                else:
                                    logging.warning(f"      Skipping non-CSV/Excel file: {file_name}")
                                    continue

                                logging.info(f"      Successfully read: {file_name}")
                                all_data.append(data)

                            except Exception as e:
                                logging.error(f"      Error reading {file_name}: {e}")

    if all_data:
        final_data = pd.concat(all_data, ignore_index=True)
        exchange_rates_df = pd.read_excel(exchange_rate_file, skiprows=6)
        exchange_rates_dict = exchange_rates_df.set_index('CODE')['RATE'].to_dict()
        final_data['Continent'] = final_data['Country'].map(COUNTRY_TO_CONTINENT)
        final_data['Total_in_USD'] = final_data.apply(
            lambda row: row['Transaction'] * exchange_rates_dict.get(row['Currency'], 1),
            axis=1
        )
        final_data.to_csv(output_file, index=False)
        logging.info(f"Data saved to {output_file}")

        logging.info("Final combined data:")
        logging.info(f"\n{final_data.head()}")

        logging.info("\nSummary of processed files:")
        logging.info(f"Total CSV files processed: {total_csv_files}")
        logging.info(f"Total CSV files read successfully: {total_csv_read_success}")
        logging.info(f"Total Excel files processed: {total_excel_files}")
        logging.info(f"Total Excel files read successfully: {total_excel_read_success}")

        return (
            f"Total CSV files processed: {total_csv_files}\n"
            f"Total CSV files read successfully: {total_csv_read_success}\n"
            f"Total Excel files processed: {total_excel_files}\n"
            f"Total Excel files read successfully: {total_excel_read_success}\n"
            f"Data saved to {output_file}"
        )
    else:
        logging.info("No data found.")
        return None
