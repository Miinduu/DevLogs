# DevLogger

A Discord bot that turns a `/devlog` command into a single post on X/Twitter.
It lets you send a quick note and optional video from Discord, then handles the
upload and tweet flow from the bot itself.

> NOTE: Posting to X uses API credits. The X API is billed for media uploads and
> tweet activity, so keep that in mind before posting large or frequent videos.

## Why

This project was built to avoid manually writing the same dev update twice and
re-uploading the same clip to Twitter. The goal is to keep the workflow in one
Discord command instead of splitting it across multiple tools.

## Current status

- ✅ `/devlog` slash command with optional attachment
- ✅ X/Twitter video upload flow
- ⚠️ The project is still fairly minimal and is not yet generalized across many
  platforms.

## Requirements

- Python 3.11+
- A Discord bot application with a bot token and the following permissions:
  - View Channels
  - Send Messages
  - Embed Links
  - Attach Files
  - Read Message History
  - Use Slash Commands
- An X/Twitter developer account with:
  - App permissions set to Read and write
  - OAuth 1.0a consumer key/secret and access token/secret
  - A valid Twitter API setup for media uploads

## Setup

1. Clone or download this project.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example file and fill in your values:

   ```bash
   cp .env.example .env
   ```

4. Update the `.env` file with your Discord bot token, your Discord user ID, your
   X/Twitter credentials, and the channel ID if needed by the bot.
5. Run the bot:

   ```bash
   python bot.py
   ```

6. In Discord, run `/devlog` with a note and optional video attachment.

## How it works

1. `/devlog` accepts a note and optional video attachment.
2. The command checks whether the caller matches `my_user_id` before allowing the
   post.
3. If an attachment is provided, it is saved to `tmp/myVideo.mp4` in this repo.
4. The content is assembled into a message list and sent to the Twitter platform
   helper.
5. The Twitter client uploads media when needed and posts the tweet.

## Important notes

- The file path for the uploaded media is currently hard-coded to the local repo
  path under `tmp/`, so this is best suited for a single local setup unless you
  adjust the path logic.
- This project is currently focused on X/Twitter and still assumes a single owner
  user for access control.
- The command argument names in the code are `new_features` and `todos`, rather than
  a single generic `note` field.