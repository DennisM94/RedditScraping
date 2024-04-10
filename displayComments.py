import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('comments.db')
c = conn.cursor()

def clean_database():
    c.execute('''
        DELETE FROM comment_list
        WHERE rowid NOT IN (
            SELECT MAX(rowid) FROM comment_list GROUP BY comment
        )
    ''')

    c.execute('''
        DELETE FROM word_count
        WHERE rowid NOT IN (
            SELECT MAX(rowid) FROM word_count GROUP BY word
        )
    ''')

    conn.commit()


def display_top_words():
    # Fetch and print the top 10 most used words
    c.execute('SELECT word, count FROM word_count ORDER BY count DESC LIMIT 10')
    top_words = c.fetchall()
    print("\nTop 10 Most Used Words:")
    for word, count in top_words:
        print(f"{word}: {count}")

def display_data():
    c.execute('SELECT word, count FROM word_count ORDER BY count DESC LIMIT 15')
    word_counts = c.fetchall()
    print("\nWord Counts:")
    for word, count in word_counts:
        print(f"{word}: {count}")

    # Visualize word counts using a bar chart
    words = [word for word, _ in word_counts]
    counts = [count for _, count in word_counts]

    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.title('Word Counts')
    plt.xticks(rotation=45)
    plt.show()

def display_data_filtered():
    # Fetch and print the top 15 most used words, excluding common words
    c.execute('''
        SELECT word, count
        FROM word_count
        WHERE word NOT IN ('a', 'the', 'he', 'she', 'it', 'i', 'with', 'to', 'and', 'of', 'is', 'in', 'for', 'that', 'was', '*', 'you', 'I', ' I', 'I ', 'from', 'on', 'at', 'this', 'my', 'me', 'are', 'be', 'have', 'has', 'we', 'our', 'your', 'will', 'as', 'but', 'not', 'or', 'if', 'so', 'do', 'by', 'an', 'can', 'just', 'about', 'out', 'up', 'all', 'what', 'when', 'how', 'where', 'why', 'who', 'which', 'then', 'than', 'them', 'their', 'they', 'there', 'these', 'those', 'would', 'could', 'should', 'may', 'might', 'must', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could', 'ought', 'need', 'dare', 'used', 'ought', 'need', 'dare', 'used', 'make', 'made', 'let', 'help', 'helped', 'helping', 'keep', 'kept', 'keeping', 'call', 'called', 'calling', 'hear', 'heard', 'hearing', 'see', 'saw', 'seeing', 'seem', 'seemed', 'seeming', 'look', 'looked', 'looking', 'feel', 'felt', 'feeling', 'smell', 'smelled', 'smelling', 'taste', 'tasted', 'tasting', 'sound', 'sounded', 'sounding', 'appear', 'appeared', 'appearing', 'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could', 'need', 'dare', 'used', 'use', 'if', 'it', 'It', 'also', 'lf', 'If', 'You')
        ORDER BY count DESC
        LIMIT 15
    ''')
    word_counts = c.fetchall()
    print("\nFiltered Word Counts:")
    for word, count in word_counts:
        print(f"{word}: {count}")

    # Visualize filtered word counts using a bar chart
    words = [word for word, _ in word_counts]
    counts = [count for _, count in word_counts]

    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.title('Filtered Word Counts')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == '__main__':
    clean_database()
    display_data_filtered()