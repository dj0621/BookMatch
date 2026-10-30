# BookMatch

BookMatch is a Discord bot I built using Python that helps people find books based on their reading preferences. Instead of spending time searching for something to read, users can answer a few questions and get five book recommendations that match their interests.

I started this project to get more experience with Python and learn how to use AI and APIs in my own programs.

## Features

- **Personalized Book Recommendations:** Users answer 13 questions about their reading preferences, including their favorite genres, authors, reading level, and the types of stories they enjoy.
- **AI Recommendations:** BookMatch uses Ollama to generate five book recommendations based on the user's answers.
- **Match Percentages:** Each recommended book gets an estimated match percentage based on how well it fits the user's preferences.
- **Book Covers:** The bot uses Open Library to find and display book covers when they're available.
- **Book Information:** Each recommendation includes the book's title, author, a short explanation, and a link to learn more about it.
- **Discord Commands:** Users can start or cancel the questionnaire directly in Discord.

## Technologies Used

- **Python:** Used to build the bot and handle the recommendation process.
- **discord.py:** Allows the bot to interact with users through Discord.
- **Ollama:** Runs the AI model locally on my computer.
- **Qwen2.5 (1.5B):** The AI model that generates book recommendations.
- **Open Library API:** Used to retrieve book covers and information.
- **Git and GitHub:** Used to manage and share the project.

## How It Works

When someone types `!bm start` in Discord, BookMatch begins asking questions about their reading preferences.

After the user finishes all 13 questions, their answers are sent to the AI model. The model uses those preferences to recommend five books.

Each recommendation includes a match percentage, a short explanation of why the book was chosen, and a book cover if one is available.

The goal is to make finding a new book easier and more personalized.

## Getting Started

To run BookMatch on your own computer, you'll need Python, Ollama, and a Discord bot token.

### 1. Clone the Repository

```bash
git clone https://github.com/dj0621/BookMatch.git
cd BookMatch
```

### 2. Install Dependencies

```bash
pip install discord.py python-dotenv ollama requests
```

### 3. Set Up Ollama

Download the AI model used by BookMatch:

```bash
ollama pull qwen2.5:1.5b
```

Make sure Ollama is running before starting the bot.

### 4. Set Up Your Discord Token

Create a `.env` file in the project folder and add your Discord bot token:

```env
DISCORD_TOKEN=your_token_here
```

Keep your actual token private.

You'll also need to invite your bot to a Discord server and enable the Message Content Intent in the Discord Developer Portal.

### 5. Run BookMatch

```bash
python bot.py
```

Once the bot is online, you can use its commands in Discord.

## Commands

| Command | Description |
|---|---|
| `!bm start` | Starts the book recommendation questionnaire |
| `!bm cancel` | Cancels the current questionnaire |
| `!bm help` | Shows the available commands |
| `!bm test` | Tests the recommendation system using sample preferences |

## Screenshots

I'll add screenshots of the questionnaire and book recommendations here.

## What I Learned

Working on BookMatch helped me get more comfortable with Python and understand how different parts of a program work together.

One of the biggest things I learned was how to connect a Discord bot to an AI model and use an API to retrieve information.

I also ran into some challenges with the AI model taking too long to respond. After testing different options, I switched to a smaller model that worked better on my computer.

Overall, this project gave me more experience with debugging, organizing code into separate files, and building something that people can actually use.

## Future Improvements

There are a few things I'd like to improve as I continue learning:

- Make the book recommendations more accurate.
- Improve the match percentage system.
- Give users the option to save books they're interested in.
- Add more commands and customization options.

## Project Status

BookMatch Version 1.0 is complete and working.

The bot can ask users questions, generate five personalized recommendations, and display book information directly in Discord.