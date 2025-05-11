import pandas as pd
import re
from datetime import datetime, timedelta

def clean_text(text):
    """
    Clean text by removing links, emojis, and special characters.
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove emojis and non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    
    # Remove special characters except basic punctuation
    text = re.sub(r'[^a-zA-Z0-9.,!?\'"\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def aggregate_and_clean_data(input_file, output_file):
    """
    Reads the CSV file, aggregates messages by hour, cleans the text, and outputs to a new CSV file.
    """
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Ensure the 'hour' column is in datetime format
    df['hour'] = pd.to_datetime(df['hour'])

    # Clean the text column
    df['text'] = df['text'].apply(clean_text)

    # Aggregate messages by hour
    aggregated_data = []
    start_time = df['hour'].min()
    end_time = df['hour'].max()
    current_time = start_time

    while current_time <= end_time:
        # Filter messages for the current hour
        messages_this_hour = df[df['hour'] == current_time]

        if not messages_this_hour.empty:
            # Combine all messages in this hour into a single text entry
            combined_text = ' | '.join(messages_this_hour['text'].tolist())
        else:
            # If no messages, set text to "No messages"
            combined_text = "No messages"

        # Append to the aggregated data
        aggregated_data.append({
            'hour': current_time.strftime('%Y-%m-%d %H:00:00'),
            'text': combined_text
        })

        # Increment the current time by 1 hour
        current_time += timedelta(hours=1)

    # Create a DataFrame from the aggregated data
    aggregated_df = pd.DataFrame(aggregated_data)

    # Save the aggregated and cleaned data to a new CSV file
    aggregated_df.to_csv(output_file, index=False)
    print(f"Aggregated and cleaned data saved to {output_file}")

# File paths
input_file = 'historical_telegram_data.csv'
output_file = 'cleaned_aggregated_telegram_data.csv'

# Run the aggregation and cleaning process
aggregate_and_clean_data(input_file, output_file)
