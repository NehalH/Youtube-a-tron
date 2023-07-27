import praw
import requests
import os
import traceback
import credentials

def download_top_videos(subreddit_name, output_folder):
    # Replace contents of credentials.py with your Reddit api details.
    reddit = praw.Reddit(client_id=credentials.client_id,
                         client_secret=credentials.client_secret,
                         user_agent=credentials.user_agent)


    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(limit=1, time_filter='all')  # Fetch top 100 posts of all time

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    video_count = 0

    for post in top_posts:
        if post.is_video:
            video_url = post.media['reddit_video']['fallback_url']
            media_extension = 'mp4'
            media_title = post.title + '.' + media_extension
            media_path = os.path.join(output_folder, media_title)

            print(f"Downloading video: {media_title}")
            try:
                response = requests.get(video_url)

                if response.status_code == 200:
                    with open(media_path, 'wb') as f:
                        f.write(response.content)

                    print("Download complete!")
                    video_count += 1

                    if video_count == 10:  # Stop after downloading 10 videos
                        break
                else:
                    print(f"Failed to download video. Status code: {response.status_code}")
            except Exception as e:
                print("An error occurred:")
                print(traceback.format_exc())

    if video_count == 0:
        print("No video posts found in the top 100 posts of all time.")

if __name__ == "__main__":
    subreddit_name = "nextfuckinglevel"  # Replace this with the subreddit of your choice
    output_folder = "N:/Box/WorkSpace/Project/praw test/downloaded_media" 
    download_top_videos(subreddit_name, output_folder)
