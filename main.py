import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime

# Specify a font that includes a wide range of Unicode characters and symbols
plt.rcParams['font.family'] = 'DejaVu Sans'

# Function to load and preprocess chat data with the new format
# Function to load and preprocess chat data with the new format
# Function to load and preprocess chat data while excluding messages containing certain words
def load_and_preprocess_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        chat_lines = file.readlines()

    # Extracting timestamps, senders, and messages while excluding specific words
    data = []
    for line in chat_lines:
        match = re.match(r'\[(.*?)\] (.*?): ‎(.*)', line)
        if match:
            timestamp_str, sender, message = match.groups()
            # Words to exclude
            exclude_words = ['joined', 'using', 'this', '+91', 'left', '~']
            # Check if any of the exclude_words is in the message
            if not any(word in message for word in exclude_words):
                timestamp = datetime.strptime(timestamp_str, '%d/%m/%y, %I:%M:%S %p')
                data.append([timestamp, sender, message])

    # Creating a DataFrame with proper datetime conversion
    df = pd.DataFrame(data, columns=['Timestamp', 'Sender', 'Message'])
    return df




# Function to plot the number of messages per sender and save as an image
def plot_messages_per_sender(df, output_path='messages_per_sender.png'):
    if df.empty:
        print("No messages found in the chat data.")
        return

    sender_counts = df['Sender'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sender_counts.index, y=sender_counts.values)
    plt.title('Number of Messages per Sender')
    plt.xlabel('Sender')
    plt.ylabel('Message Count')
    plt.xticks(rotation=45)
    plt.savefig(output_path)  # Save the chart as an image
    plt.close()  # Close the chart to release resources


# Function to plot message distribution over time and save as an image
def plot_message_distribution_over_time(df, output_path='message_distribution_over_time.png'):
    df['Date'] = df['Timestamp'].dt.date
    daily_message_counts = df.groupby('Date').size()

    plt.figure(figsize=(12, 6))
    daily_message_counts.plot()
    plt.title('Message Distribution Over Time')
    plt.xlabel('Date')
    plt.ylabel('Message Count')
    plt.grid(True)
    plt.savefig(output_path)  # Save the chart as an image
    plt.close()  # Close the chart to release resources

# Function to find the most common words used
def find_most_common_words(df, top_n=10):
    words = ' '.join(df['Message']).lower().split()
    word_counts = pd.Series(words).value_counts()
    return word_counts.head(top_n)

def print_names_without_tilde(df):
    if df.empty:
        print("No messages found in the chat data.")
        return

    # Filter messages where the sender's message doesn't contain ~
    filtered_df = df[df['Message'].str.find('~') == -1]

    # Get unique sender names from the filtered DataFrame
    unique_senders = filtered_df['Sender'].unique()

    # Print the unique sender names
    print("Names that don't have ~ in their sent message:")
    for sender in unique_senders:
        print(sender)

if __name__ == '__main__':
    chat_file = '_chat.txt'

    # Load and preprocess chat data
    chat_df = load_and_preprocess_chat(chat_file)
    print_names_without_tilde(chat_df)
    # Find the sender(s) with the highest number of messages
    sender_counts = chat_df['Sender'].value_counts()
    max_messages = sender_counts.max()
    top_senders = sender_counts[sender_counts == max_messages].index.tolist()

    # Print the sender(s) with the highest number of messages
    if len(top_senders) == 1:
        print(f"The sender with the highest number of messages is: {top_senders[0]}")
    else:
        top_senders_str = ", ".join(top_senders)
        print(f"The senders with the highest number of messages are: {top_senders_str}")

    # Print out all the top 50 message senders
    print("Top 50 Message Senders:")
    top_50_senders = sender_counts.head(50)
    for i, (sender, count) in enumerate(top_50_senders.items(), start=1):
        print(f"{i}. {sender}: {count} messages")

    # Plot the number of messages per sender and save as an image
    plot_messages_per_sender(chat_df, output_path='messages_per_sender.png')

    # Plot message distribution over time and save as an image
    plot_message_distribution_over_time(chat_df, output_path='message_distribution_over_time.png')

    # Find and display the most common words
    common_words = find_most_common_words(chat_df, top_n=10)
    print('Most Common Words:')
    print(common_words)
