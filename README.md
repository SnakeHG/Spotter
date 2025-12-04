!!Make sure you have python!!


First make sure you have all the proper libraries installed

python3 -m pip install discord huggingface_hub dotenv requests

Then get the .env file and the corresponding tokens (Obtain from us or get a separate discord_api_token, google_safe_browsing_token, and huggingface token)
- Make sure .env file is in same folder as code (Make sure file is named .env)

Then you can run the bot locally:

cd into the correct folder to where the test_bot.py file is located.

Use '''python3 test_bot.py''' to run the file


General Steps:
---------------
1. get code from github
2. get tokens in .env
3. run test_bot

Contribution Breakdown
----------------------
Jenny conceptualized the URL threat detection approach as a core solution to Discord's malware delivery problem, conducted research on Discord security vulnerabilities and malware delivery mechanisms, authored the Problem/Significance statement and co-wrote the project proposal, then implemented the URL-checking functionality by developing safe_browsing.py and integrating it into test_bot.py using Google Safe Browsing API. Additionally, Jenny facilitated team communication and coordinated meeting schedules to ensure smooth project execution.

Shu combined the backend integration, merging individual contributions from Jenny and Ye into a unified operational framework. He optimized the bot's interaction with external libraries by resolving data retrieval issues from huggingface and validated the bot's functionality through testing and debugging within Discord server.

Henry developed base features of the Discord bot, including message parsing and reaction handling. He coordinated team meetings, assigned roles, and organized development tasks to ensure smooth collaboration. He also set up the Discord bot, server, and GitHub repository, establishing the project infrastructure for version control, deployment, and team coordination
