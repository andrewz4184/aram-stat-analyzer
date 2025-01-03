Riot API Statistical Analyzer

A full-stack web application designed to analyze and display statistics for players in the League of Legends game mode ARAM (All Random All Mid). This project serves as a personal exploration into web development, covering both front-end and back-end implementation, API usage, and integration of public resources for dynamic image sourcing.

Key Features

Player Data Analysis: Retrieve and analyze statistics from up to 1000 matches per player.
Real-Time Image Loading: Dynamically source and display champion and item images to enhance user experience.
API Integration: Utilized Riot Games API for data retrieval, with optimized requests adhering to rate limits (50 calls/minute).
Challenges and Limitations
Due to recent changes in the Riot API, some features were affected, requiring updates to the codebase. Additionally, the free developer key provided by Riot has stringent limitations, leading to potential long runtimes or errors when analyzing players with extensive match histories.

Technologies Used

Back-End: Python (Flask)
Front-End: HTML, CSS
API: Riot Games API
Others: Public databases for image resources
