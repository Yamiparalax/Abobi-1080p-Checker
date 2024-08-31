# Abobi 1080p Checker

**Abobi Video Quality Cleaner** is a Python script designed to help video content creators by automatically deleting video files that are below a specified resolution. This tool ensures that only high-quality videos (1080p or higher) are kept, making it ideal for preparing content for various platforms.

## Features

- **Automatic Deletion**: Deletes video files that do not meet the minimum resolution criteria.
- **User-Friendly Interface**: Built with PyQt5 for an intuitive graphical interface.
- **Configurable Paths**: Allows users to specify input and output folders for processing.
- **Error Handling**: Provides detailed error messages for easy troubleshooting.

## Requirements

- Python 3.x
- PyQt5
- MoviePy
- FFmpeg
- `ffprobe` (comes with FFmpeg)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Yamiparalax/Abobi-1080p-Checker.git
   ```

2. **Navigate to the Directory**:

   ```bash
   cd abobi-video-quality-cleaner
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure FFmpeg is Installed**:
   - Make sure FFmpeg and `ffprobe` are available in your system PATH.

## Usage

1. **Run the Script**:

   ```bash
   python abobi_video_quality_cleaner.py
   ```

2. **Configure Paths and Settings**:
   - Enter the path of the folder containing your video files.
   - Specify the output folder for logging.
   - Set the minimum resolution (1080p) that files should meet to avoid deletion.

3. **Start the Process**:
   - Click the "Process Videos" button to begin cleaning up your video collection.

## Troubleshooting

- **File In Use Error**: Ensure no other programs are using the video files while the script is running.
- **Resolution Detection Issues**: Verify that FFmpeg and `ffprobe` are correctly installed and accessible.

## Contact

For any questions or support, you can reach out via:

- **Email**: [abobicarlo@gmail.com](mailto:abobicarlo@gmail.com)
- **LinkedIn**: [linkedin.com/in/abobicarlo](https://www.linkedin.com/in/abobicarlo/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.