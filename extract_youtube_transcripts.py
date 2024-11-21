from youtube_transcript_api import YouTubeTranscriptApi
import os

# Dictionary of seasons and their YouTube video links
season_videos = {
    "Season1": "-vBFOsN3jZA",
    "Season2": "4Mm3VA2pJAM",
    "Season3": "IBjDKOvKXNk",
    "Season4": "CYh5b6jK9X4",
    "Season5": "luosdaRCWSU",
    "Season6": "EsMcUp4Tw8U",
    "Season7": "rCU_RFcb8wg"
}

# Directory to save transcripts
output_dir = "transcripts"
os.makedirs(output_dir, exist_ok=True)

# Function to fetch and save transcript for a video
def fetch_and_save_transcript(video_id, season):
    try:
        print(f"Fetching transcript for {season}...")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Save the transcript to a file
        file_path = os.path.join(output_dir, f"{season}_transcript.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            for entry in transcript:
                file.write(f"{entry['start']:.2f}s: {entry['text']}\n")

        print(f"Transcript saved for {season}: {file_path}")
    except Exception as e:
        print(f"Failed to fetch transcript for {season}: {e}")

# Loop through each season and extract transcripts
for season, video_id in season_videos.items():
    fetch_and_save_transcript(video_id, season)

print("All transcripts fetched and saved!")
