import os
import pandas as pd
import matplotlib.pyplot as plt

# Path to the folder containing transcript files
transcripts_folder = "transcripts"

# Initialize a DataFrame to store results
data = {
    "Season": [],
    "Episode": [],
    "Wow Count": [],
}

# Process each transcript file
for filename in os.listdir(transcripts_folder):
    if filename.endswith("_transcript.txt"):
        season = filename.split("_")[0]  # Extract season name
        filepath = os.path.join(transcripts_folder, filename)
        
        # Read the transcript file
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().lower()  # Convert to lowercase for case-insensitive matching

        # Count occurrences of "wow"
        wow_count = content.count("wow")
        
        # Save the results
        data["Season"].append(season)
        data["Episode"].append(filename)  # Use filename as episode identifier
        data["Wow Count"].append(wow_count)

# Create a DataFrame
df = pd.DataFrame(data)

# Group by Season for analysis
season_summary = df.groupby("Season").agg(
    Total_Wows=("Wow Count", "sum"),
    Avg_Wows_Per_Episode=("Wow Count", "mean"),
    Episodes=("Episode", "count")
).reset_index()

# Calculate overall totals and averages
total_wows_all_seasons = df["Wow Count"].sum()
avg_wows_per_episode_all_seasons = df["Wow Count"].mean()

# Add overall summary to the DataFrame
overall_summary = pd.DataFrame({
    "Season": ["All Seasons"],
    "Total_Wows": [total_wows_all_seasons],
    "Avg_Wows_Per_Episode": [avg_wows_per_episode_all_seasons],
    "Episodes": [df["Episode"].count()],
})

season_summary_with_overall = pd.concat([season_summary, overall_summary], ignore_index=True)

# Identify the episode with the most wows
max_wow_episode = df[df["Wow Count"] == df["Wow Count"].max()]

# Write results to an Excel file
output_file = "Kitchen_Nightmares_Wow_Analysis.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Detailed Analysis")
    season_summary_with_overall.to_excel(writer, index=False, sheet_name="Season Summary")
    max_wow_episode.to_excel(writer, index=False, sheet_name="Most Wow Episode")

# Generate bar chart: Total wows per season
plt.figure(figsize=(10, 6))
plt.bar(season_summary["Season"], season_summary["Total_Wows"], color='skyblue')
plt.title("Total 'Wow' Count Per Season", fontsize=14)
plt.xlabel("Season")
plt.ylabel("Total 'Wow' Count")
plt.tight_layout()
plt.savefig("Total_Wows_Per_Season.png")
plt.show()

# Generate pie chart: Proportion of wows by season
plt.figure(figsize=(8, 8))
plt.pie(
    season_summary["Total_Wows"],
    labels=season_summary["Season"],
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Paired.colors,
)
plt.title("Proportion of 'Wow' Count by Season", fontsize=14)
plt.savefig("Wow_Proportion_Pie_Chart.png")
plt.show()

# Save confirmation message
print(f"Analysis complete! Results saved to '{output_file}', bar chart as 'Total_Wows_Per_Season.png', and pie chart as 'Wow_Proportion_Pie_Chart.png'.")
