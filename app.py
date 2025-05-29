import streamlit as st
import requests
import os

# Set page title and favicon
st.set_page_config(
    page_title="YouTube Video Downloader",
    page_icon="▶️",
    layout="centered",
)

# Custom CSS for better UI
st.markdown("""
    <style>
        .stButton>button {
            background-color: #FF0000;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #CC0000;
        }
        .stTextInput>div>div>input {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("📥 YouTube Video Downloader")
st.markdown("""
    Paste a YouTube streaming URL below to download the video.
    *(Note: This works only with direct streaming URLs, not regular YouTube links.)*
""")

# Input URL
url = st.text_input("Enter YouTube Streaming URL:", placeholder="https://rr6---sn-ci5gup-pmge.googlevideo.com/...")

# Download button
if st.button("Download Video", key="download_button"):
    if not url:
        st.error("Please enter a valid URL!")
    else:
        try:
            # Headers to mimic a browser request
            headers = {
                'Range': f'bytes={0}-{8000}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'max-age=0',
                'Accept': '*/*',
                'DNT': '1',
                'TE': 'trailers'
            }
            # Send a GET request with streaming
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()  # Raise error if request fails

            # Get file size for progress bar
            file_size = int(response.headers.get('content-length', 0))
            st.info(f"File size: {file_size / (1024 * 1024):.2f} MB")

            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Download in chunks and save
            output_file = "downloaded_video.mp4"
            downloaded_bytes = 0

            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_bytes += len(chunk)
                        progress = int((downloaded_bytes / file_size) * 100)
                        progress_bar.progress(progress)
                        status_text.text(f"Downloading... {progress}%")

            st.success("✅ Video downloaded successfully!")
            st.balloons()

            # Provide download link
            with open(output_file, "rb") as f:
                video_bytes = f.read()
            st.download_button(
                label="Click to Save Video",
                data=video_bytes,
                file_name="downloaded_video.mp4",
                mime="video/mp4",
            )

            # Clean up (remove the file after download)
            os.remove(output_file)

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error downloading video: {e}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")

# Footer
st.markdown("---")
st.markdown("_Made with ❤️ using Streamlit_")
