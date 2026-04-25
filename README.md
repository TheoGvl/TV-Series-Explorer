# TV Series Explorer

A high-performance TV show discovery application built with Python and Flet. Explore thousands of series, check ratings, and read summaries in a sleek, streaming-inspired desktop interface perfectly adapted for the latest Flet framework standards.

## Features

* **Dynamic Discovery:** Search for any TV series in real-time using data from the [TVmaze API](https://www.tvmaze.com/api).
* **Responsive Grid:** Automatically adjusts the number of posters displayed based on your window size, featuring perfectly cropped background images.
* **Detailed Insights:** Clicking on any show card opens a modern, animated Bottom Sheet displaying:
    * High-quality poster artwork.
    * IMDb-style ratings, premiere dates, and running status.
    * Sleek, pill-shaped genre badges.
    * Sanitized plot summaries.
* **Streaming Aesthetic:** A deep dark mode (`#0F111A`) interface with bold red accents and subtle drop shadows.
* **Bulletproof Architecture:** Fully compatible with Flet 0.80+, utilizing safe null-handling for robust JSON parsing.

## Prerequisites

* **Python 3.8+**
* The **Flet** UI framework
* The **Requests** library

Install the necessary dependencies using pip:
```
pip install flet requests
```
