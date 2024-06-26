# MoneyMaker: Automated Video Creater
This project automates the process of creating videos from Reddit posts. It fetches hot posts from a specified subreddit, converts the text to speech using a pre-trained TTS model, combines the generated speech with a background video, transcribes the audio to generate subtitles, and finally overlays these subtitles on the video. The result is a fully processed video with synchronized audio and subtitles.

## Table of Contents
- [MoneyMaker](#MoneyMaker)
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Features
- Fetch hot posts from a specified subreddit.
- Convert post titles and content to speech.
- Combine generated speech with a background video.
- Transcribe audio to generate subtitles.
- Overlay subtitles on the video.

## Requirements
Ensure you have the following packages installed. You can install them using `pip`:
1. torch==2.0.1
2. numpy==1.24.2
3. soundfile==0.10.3.post1
4. praw==7.6.0
5. moviepy==1.0.3
6. transformers==4.18.0
7. datasets==2.4.0
8. whisper==1.1.0
9. python>=3.8.0

## Setup
1. Set up your Reddit API credentials: Go to Reddit Apps and create a new application to get your client_id, client_secret, and user_agent.
2. Modify the script with your paths and subreddit: Set the paths for the background video, audio, intermediate video, output video, and SRT file.
Specify the subreddit you want to fetch posts from.

## Usage
1. Clone the repository:
   ```
    git clone https://github.com/pranavdhawann/MoneyMaker.git
    cd MoneyMaker
   ```
2. Create a virtual environment:
   ```
    python3 -m venv env
    source env/bin/activate  # For Linux and macOS
    env\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```
    pip install -r requirements.txt
   ```
4. Run the script:
   ```
    python MoneyMaker.py
   ```

## Future Work
- [ ] User Interface: Develop a graphical user interface (GUI) to allow users to configure settings, select subreddits, and manage paths more easily.
- [ ] Post Filtering and Selection: Add features to filter Reddit posts based on specific criteria (e.g., keyword matching, post length, or upvote count).
- [ ] Batch Processing: Enable batch processing to generate multiple videos from multiple subreddits or a larger number of posts in a single run.
- [ ] Content Moderation: Implement content moderation features to automatically filter out inappropriate or sensitive content from the fetched Reddit posts.

## Contributing
Contributions are welcome! Feel free to give input to this repository and submit pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
