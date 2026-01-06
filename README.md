🔍 Arc Raider Scanner (v0.1 BETA)
An Open-Source Inventory Intelligence Tool for Arc Raiders

💡 The Problem
In the ruins of the old world, looting is life. However, with hundreds of different items, it becomes nearly impossible to remember which ones are vital for your next Workshop upgrade, which are needed for Quests, and which are simply Recycle fodder to be sold for Marks.

I found myself constantly tab-out to check wikis or second-guessing my loot before extraction. To solve this, I developed Arc Raider Scanner.

🚀 How It Works
This tool uses the SIFT (Scale-Invariant Feature Transform) algorithm to "look" at your game screen and match items against a local database of icons.

Overlay Mode: A transparent grid aligns with your in-game inventory.

Instant Recognition: With one click, the scanner identifies every item in your backpack.

Visual Categorization:

🔴 QUEST: Keep these! They are required for active missions.

🟠 PROJECT: Needed for base upgrades and research.

🟢 WORKSHOP: Essential crafting components.

⚪ RECYCLE: Safe to sell for profit.

🛠️ Technical Features
Interactive Filtering: The analysis window allows you to toggle categories. Want to see only what you can safely sell? Click "RECYCLE" and everything else dims out.

High Accuracy: Unlike simple pixel matching, the SIFT method recognizes items even with slight UI scaling or transparency changes.

Open Source: Built entirely in Python with OpenCV and Tkinter.

📋 Prerequisites
Python 3.11+

OpenCV, NumPy, and Pillow libraries.

👤 Author
Developed by Santazer. This project is in BETA. Feedback and icon contributions are welcome!

<img width="548" height="852" alt="image" src="https://github.com/user-attachments/assets/95931391-cc2e-4a6f-9170-fd0aa58d1241" />

