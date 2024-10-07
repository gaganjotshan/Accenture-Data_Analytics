import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['Datetime'] = pd.to_datetime(df['Datetime'], format="%d/%m/%y %H:%M")
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    df = df.dropna(subset=['Score'])
    df['Month'] = df['Datetime'].dt.strftime('%B')
    return df

# Analyze top categories
def analyze_top_categories(df, n=5):
    category_popularity = df.groupby('Category')['Score'].sum().sort_values(ascending=False)
    top_n_categories = category_popularity.head(n)
    total_score = category_popularity.sum()
    top_n_percentage = (top_n_categories.sum() / total_score) * 100
    return top_n_categories, top_n_percentage

# Plot top categories
def plot_top_categories(top_categories, top_percentage):
    plt.figure(figsize=(12, 8))
    plt.pie(top_categories.values, labels=top_categories.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'Top {len(top_categories)} Content Categories by Popularity\n(accounting for {top_percentage:.2f}% of total score)')
    plt.axis('equal')
    plt.show()

# Analyze reaction types for top categories
def analyze_reactions(df, top_categories):
    reaction_percentages = df[df['Category'].isin(top_categories.index)].groupby(['Category', 'Reaction Type']).size().unstack(fill_value=0)
    reaction_percentages = reaction_percentages.div(reaction_percentages.sum(axis=1), axis=0) * 100
    return reaction_percentages

# Plot reaction heatmap
def plot_reaction_heatmap(reaction_percentages):
    plt.figure(figsize=(15, 10))
    sns.heatmap(reaction_percentages, annot=True, fmt='.1f', cmap='YlOrRd', cbar_kws={'label': 'Percentage of Reactions'})
    plt.title('Distribution of Reaction Types for Top Categories')
    plt.xlabel('Reaction Type')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.show()

# Find maximum reaction type for each category
def get_max_reactions(reaction_percentages):
    max_reactions = reaction_percentages.idxmax(axis=1)
    result_df = pd.DataFrame({
        'Category': max_reactions.index,
        'Max Reaction Type': max_reactions.values,
        'Percentage': reaction_percentages.max(axis=1)
    })
    return result_df.sort_values('Percentage', ascending=False)

# Plot maximum reaction types
def plot_max_reactions(result_df):
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(result_df['Category'], result_df['Percentage'], height=0.4)
    ax.set_xlabel('Percentage')
    ax.set_title('Maximum Reaction Type and Percentage by Category')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{result_df["Percentage"].iloc[i]:.2f}%', 
                ha='left', va='center', fontweight='bold', fontsize=8)
        ax.text(width/2, bar.get_y() + bar.get_height()/2, result_df['Max Reaction Type'].iloc[i], 
                ha='center', va='center', fontweight='bold', fontsize=8, color='white')
    
    plt.tight_layout()
    plt.subplots_adjust(left=0.3)
    plt.show()

# Analyze posts per month
def analyze_posts_per_month(df):
    posts_per_month = df['Month'].value_counts().sort_index()
    max_month = posts_per_month.idxmax()
    max_posts = posts_per_month.max()
    return posts_per_month, max_month, max_posts

# Plot posts per month
def plot_posts_per_month(posts_per_month, max_month, max_posts):
    plt.figure(figsize=(12, 6))
    bars = posts_per_month.plot(kind='bar')
    plt.title('Number of Posts per Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Posts')
    plt.xticks(rotation=45)
    
    for i, v in enumerate(posts_per_month):
        plt.text(i, v, str(v), ha='center', va='bottom')
    
    plt.text(posts_per_month.index.get_loc(max_month), max_posts, f'Max: {max_posts}', 
             ha='center', va='bottom', fontweight='bold', color='red')
    
    plt.tight_layout()
    plt.show()

def analyze_top_categories(df, n=5):
    category_popularity = df.groupby('Category')['Score'].sum().sort_values(ascending=False)
    top_n_categories = category_popularity.head(n)
    total_score = category_popularity.sum()
    top_n_percentage = (top_n_categories.sum() / total_score) * 100
    
    # Calculate percentage for each category
    top_n_df = pd.DataFrame({
        'Category': top_n_categories.index,
        'Score': top_n_categories.values,
        'Percentage Score': (top_n_categories / total_score) * 100
    })
    
    return top_n_df, top_n_percentage

def create_top_categories_table(top_n_df, reaction_percentages):
    # Get max reaction type and percentage for each category
    max_reactions = reaction_percentages.idxmax(axis=1)
    max_reaction_percentages = reaction_percentages.max(axis=1)
    
    # Add max reaction type and percentage to the DataFrame
    top_n_df['Max Reaction Type'] = max_reactions
    top_n_df['Max Reaction Percentage'] = max_reaction_percentages
    
    # Reorder columns
    top_n_df = top_n_df[['Category', 'Score', 'Percentage Score', 'Max Reaction Type', 'Max Reaction Percentage']]
    
    return top_n_df

# Main execution
if __name__ == "__main__":
    file_path = './Task 3_Final Content Data set.csv'
    df = load_and_preprocess_data(file_path)
    
    top_5_df, top_5_percentage = analyze_top_categories(df, 5)
    plot_top_categories(top_5_df['Score'], top_5_percentage)
    
    reaction_percentages = analyze_reactions(df, top_5_df['Category'])
    plot_reaction_heatmap(reaction_percentages)
    
    # Create and save the top 5 categories table as a DataFrame
    top_5_table_df = create_top_categories_table(top_5_df, reaction_percentages)
    
    # Display the DataFrame
    print("\nTop 5 Categories Analysis:")
    print(top_5_table_df.to_string(index=False, float_format=lambda x: f'{x:.2f}'))
    
    # You can now use top_5_table_df for further analysis or save it to a file if needed
    # For example, to save to a CSV file:
    top_5_table_df.to_csv('top_5_categories_analysis.csv', index=False)
    with open('table_output.txt', 'w') as f:
        f.write( top_5_table_df.to_string(index=False))
    
    max_reactions_df = get_max_reactions(reaction_percentages)
    plot_max_reactions(max_reactions_df)
    
    posts_per_month, max_month, max_posts = analyze_posts_per_month(df)
    plot_posts_per_month(posts_per_month, max_month, max_posts)
    
    print(f"\nThe month with the maximum number of posts is {max_month} with {max_posts} posts.")