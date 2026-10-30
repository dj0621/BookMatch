import os
import re
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from ai import get_book_recommendations
from books import search_book
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!bm ",
    intents=intents,
    help_command=None
)

active_users = set()


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📚 BookMatch Help",
        description="Find books based on your reading preferences.",
        color=0x244855
    )

    embed.add_field(
        name="!bm start",
        value="Start the 13-question book quiz.",
        inline=False
    )

    embed.add_field(
        name="!bm test",
        value="Test recommendations without taking the quiz.",
        inline=False
    )

    embed.add_field(
        name="!bm cancel",
        value="Cancel your current quiz.",
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command()
async def cancel(ctx):
    key = (ctx.channel.id, ctx.author.id)

    if key in active_users:
        await ctx.send("Type **cancel** to stop your quiz.")
    else:
        await ctx.send("You don't have an active quiz.")


def parse_recommendations(recommendations):
    text = recommendations.replace("\\\n", "\n")
    text = text.replace("\\n", "\n")
    text = re.sub(r"\s+(Match:)", r"\n\1", text, flags=re.I)
    text = re.sub(r"\s+(Why:)", r"\n\1", text, flags=re.I)

    pattern = (
        r"(?:^|\n)\s*(?:\d+[\.\)]\s*)?"
        r"(?:\*\*)?(.+?)\s+-\s+(.+?)(?:\*\*)?\s*\n"
        r"\s*Match:\s*(\d{1,3}\s*%)\s*\n"
        r"\s*Why:\s*(.*?)"
        r"(?=\n\s*(?:\d+[\.\)]\s*)?(?:\*\*)?"
        r"[^\n]+?\s+-\s+[^\n]+?\n\s*Match:|\Z)"
    )

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    books = []
    seen_titles = set()

    for title, author, match, reason in matches:
        title = title.strip().strip("*")
        author = author.strip().strip("*")
        reason = reason.strip()

        if not title or not author:
            continue

        if title.lower() in seen_titles:
            continue

        books.append({
            "title": title,
            "author": author,
            "match": match.strip(),
            "reason": reason
        })

        seen_titles.add(title.lower())

        if len(books) == 5:
            break

    return books


async def show_recommendations(ctx, preferences):
    async with ctx.typing():
        recommendations = await asyncio.to_thread(
            get_book_recommendations,
            preferences
        )

    if not recommendations:
        await ctx.send(
            "❌ I couldn't generate recommendations right now. "
            "Please try again."
        )
        return

    print("OLLAMA RESPONSE:")
    print(recommendations)

    books = parse_recommendations(recommendations)

    if not books:
        await ctx.send(
            "⚠️ I couldn't process the recommendations. "
            "Check the terminal for Ollama's response."
        )
        return

    for book in books:
        book_info = await asyncio.to_thread(
            search_book,
            book["title"],
            book["author"]
        )

        embed = discord.Embed(
            title=f"📚 {book['title']}",
            description="Recommended based on your reading preferences.",
            color=0x244855
        )

        embed.add_field(
            name="✍️ Author",
            value=book["author"][:1024],
            inline=False
        )

        embed.add_field(
            name="🎯 Match",
            value=book["match"],
            inline=True
        )

        embed.add_field(
            name="💡 Why This Matches",
            value=book["reason"][:1024] or "Based on your preferences.",
            inline=False
        )

        if book_info:
            if book_info.get("image"):
                embed.set_thumbnail(url=book_info["image"])

            if book_info.get("link"):
                embed.add_field(
                    name="🔗 Book Information",
                    value=f"[View on Open Library]({book_info['link']})",
                    inline=False
                )

        await ctx.send(embed=embed)
        await asyncio.sleep(1.1)

    await ctx.send(
        f"📚 **Found {len(books)} book recommendations!**"
    )


@bot.command()
async def start(ctx):
    key = (ctx.channel.id, ctx.author.id)

    if key in active_users:
        await ctx.send("You already have a quiz running.")
        return

    active_users.add(key)

    questions = [
        (
            "genre",
            "📚 What genre are you interested in?",
            ["Fantasy", "Mystery", "Romance", "Science Fiction",
             "Thriller", "Horror", "Historical Fiction",
             "Non-Fiction", "Biography", "Self-Help"],
            True
        ),
        (
            "favorite_book",
            "📖 What's your favorite book? Type its name, or type Skip.",
            None,
            False
        ),
        (
            "favorite_author",
            "✍️ Do you have a favorite author? Type their name, or type Skip.",
            None,
            False
        ),
        (
            "book_mood",
            "😊 What mood are you looking for?",
            ["Happy", "Dark", "Funny", "Emotional",
             "Action-packed", "Suspenseful", "Romantic",
             "Inspirational", "Surprise me"],
            True
        ),
        (
            "book_length",
            "📏 How long should the book be?",
            ["Short", "Medium", "Long", "No preference"],
            False
        ),
        (
            "avoid",
            "🚫 Is there anything you want to avoid in a book? Type your answer, or None.",
            None,
            False
        ),
        (
            "series",
            "📚 Do you prefer standalone books or series?",
            ["Standalone", "Series", "No preference"],
            False
        ),
        (
            "reading_level",
            "📖 What's your reading level?",
            ["Beginner", "Intermediate", "Advanced", "No preference"],
            False
        ),
        (
            "setting",
            "🌍 What kind of setting interests you?",
            ["Modern world", "Historical", "Fantasy world",
             "Futuristic", "Small town", "Big city",
             "No preference"],
            True
        ),
        (
            "age_group",
            "👤 What age group should the book target?",
            ["Middle Grade", "Young Adult", "Adult", "Any age"],
            False
        ),
        (
            "pace",
            "⚡ What pace do you prefer?",
            ["Slow", "Medium", "Fast", "No preference"],
            False
        ),
        (
            "focus",
            "🧠 What matters most to you in a book?",
            ["Characters", "Plot", "World-building",
             "A mix of everything"],
            True
        ),
        (
            "description",
            "✨ Describe your ideal book in a sentence or two. You can be as specific as you want.",
            None,
            False
        )
    ]

    def check(message):
        return (
            message.author == ctx.author
            and message.channel == ctx.channel
            and not message.author.bot
        )

    async def get_answer(number, question, options, allow_custom):
        message_text = f"**Question {number}/13**\n\n{question}"

        if options:
            choices = "\n".join(
                f"{i}. {option}"
                for i, option in enumerate(options, 1)
            )

            message_text += f"\n\n{choices}"

            if allow_custom:
                message_text += (
                    f"\n{len(options) + 1}. Other (type your own answer)"
                )

            message_text += "\n\nReply with a number."
        else:
            message_text += "\n\nType your answer."

        await ctx.send(message_text)

        while True:
            response = await bot.wait_for(
                "message",
                check=check,
                timeout=300
            )

            answer = response.content.strip()

            if answer.lower() in ("cancel", "!bm cancel"):
                raise asyncio.CancelledError

            if not answer:
                await ctx.send("Please enter an answer.")
                continue

            if options is None:
                return answer

            if answer.isdigit():
                choice = int(answer)

                if 1 <= choice <= len(options):
                    return options[choice - 1]

                if allow_custom and choice == len(options) + 1:
                    await ctx.send("Type your own answer.")

                    while True:
                        response = await bot.wait_for(
                            "message",
                            check=check,
                            timeout=300
                        )

                        custom_answer = response.content.strip()

                        if custom_answer.lower() in ("cancel", "!bm cancel"):
                            raise asyncio.CancelledError

                        if custom_answer:
                            return custom_answer

                        await ctx.send("Please enter an answer.")

            if allow_custom:
                await ctx.send(
                    f"Enter a number from 1 to {len(options) + 1}."
                )
            else:
                await ctx.send(
                    f"Enter a number from 1 to {len(options)}."
                )

    try:
        user_preferences = {}

        await ctx.send(
            "📚 **Welcome to BookMatch!**\n\n"
            "Answer 13 questions to get personalized book recommendations.\n\n"
            "Some questions let you type your own answers.\n\n"
            "Type **ready** to begin or **cancel** to stop."
        )

        message = await bot.wait_for(
            "message",
            check=check,
            timeout=300
        )

        if message.content.strip().lower() == "cancel":
            await ctx.send("🛑 Your quiz has been cancelled.")
            return

        if message.content.strip().lower() != "ready":
            await ctx.send(
                "Quiz not started. Type **!bm start** to try again."
            )
            return

        for number, (key_name, question, options, allow_custom) in enumerate(
            questions, 1
        ):
            answer = await get_answer(
                number,
                question,
                options,
                allow_custom
            )

            user_preferences[key_name] = answer

        await ctx.send(
            "🎉 **Quiz complete!**\n\n"
            "🔎 Finding books that match your preferences..."
        )

        await show_recommendations(ctx, user_preferences)

    except asyncio.CancelledError:
        await ctx.send("🛑 Your quiz has been cancelled.")

    except asyncio.TimeoutError:
        await ctx.send(
            "⏰ Your quiz timed out. Type **!bm start** to try again."
        )

    except Exception as e:
        print(f"Error: {e}")
        await ctx.send(
            "❌ Something went wrong. Please try again."
        )

    finally:
        active_users.discard(key)


@bot.command()
async def test(ctx):
    preferences = {
        "genre": "Fantasy",
        "favorite_book": "Harry Potter",
        "favorite_author": "No preference",
        "book_mood": "Adventurous",
        "book_length": "Medium",
        "avoid": "None",
        "series": "No preference",
        "reading_level": "Beginner",
        "setting": "Fantasy world",
        "age_group": "Young Adult",
        "pace": "Fast",
        "focus": "Plot",
        "description": "I want an exciting adventure with magic."
    }

    await ctx.send("🔎 Testing book recommendations...")

    try:
        await show_recommendations(ctx, preferences)
    except Exception as e:
        print(f"Test error: {e}")
        await ctx.send("❌ Something went wrong during the test.")


if not TOKEN:
    raise ValueError("DISCORD_TOKEN is missing.")

bot.run(TOKEN)
