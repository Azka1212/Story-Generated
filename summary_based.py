import re
import json
import requests
import io
import logging
import openai


logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

openai.api_key = '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'

genres_kids = ["Comic", "Animated", "Motivation", "Disney Land", "Adventure", "Fantasy", "Science Fiction",
               "Animal Tales", "Mystery", "Fairytale", "Superhero", "Friendship"]
genres_adults = ["Mystery", "Romance", "Science Fiction", "Fantasy", "Thriller", "Horror", "Historical Fiction",
                 "Adventure", "Crime", "Non-Fiction", "Biography", "Autobiography", "Comedy", "Drama", "Poetry",
                 "Fairy Tale", "Mythology", "Satire", "Dystopian"]

MAX_CHAPTERS = 10  # Define the maximum number of chapters for the subscription model
chapter_counter = 0  # Initialize chapter counter

Chapter_list = []  # List to store generated chapters


def generate_chapter(prompt, max_tokens):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"


def generate_short_story(age: int, genre: str, idea: str):
    global chapter_counter  # Declare chapter_counter as global
    additional_info = ""

    prompt_structure = (
        f"Create a {'children' if age < 18 else 'adult'}'s story in the genre of {genre}. Story idea: {idea}\n"
        "Chapter 1:\n"
        "[Chapter Content]\n"
        "Chapter 2:\n"
        "[Chapter Content]\n"
        "Chapter 3:\n"
        "[Chapter Content]\n"
        "Chapter 4:\n"
        "[Chapter Content]\n"
        "Chapter 5:\n"
        "[Chapter Content]\n"
        "- Moral of the Story\n"
        f"The story is in the genre of {genre}. Story idea: {idea}\n"
        f"{additional_info}"
    )

    try:
        if chapter_counter >= MAX_CHAPTERS:
            print("Chapter limit reached. Cannot generate more chapters.")
            return "Chapter limit reached."

        chapter_content = generate_chapter(prompt_structure, max_tokens=1500)
        chapter_counter += 5  # Increment chapter counter by 5 for short story

        # Generate a moral for the story
        moral_prompt = f"Generate the moral of the short story:\n{chapter_content}\nMoral:"
        moral = generate_chapter(moral_prompt, max_tokens=150)

        Chapter_list.append((chapter_content, moral))
        return chapter_content

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"



def generate_long_story(age: int, genre: str, idea: str):
    global chapter_counter
    summaries = []  # List to store summaries
    generated_chapters = []  # List to store generated chapters

    try:
        if chapter_counter >= MAX_CHAPTERS:
            print("Chapter limit reached. Cannot generate more chapters.")
            return "Chapter limit reached."

        # Generate Chapter 1
        chapter_1_prompt = (
            f"Chapter 1: The Start of {idea}\n\n"
            f"[Chapter Content]\n\n"
            f"Moral of the Story: {idea}.\n"
        )
        chapter_content_1 = generate_chapter(chapter_1_prompt, max_tokens=1500)
        generated_chapters.append(chapter_content_1)
        chapter_counter += 1  # Increment chapter counter by 1 for Chapter 1

        # Generate Chapter 2
        chapter_2_prompt = (
            f"Chapter 2: An Unexpected Twist in {idea}\n\n"
            f"[Chapter Content]\n\n"
            f"Moral of the Story: Sometimes, unexpected surprises happen in {idea}."
        )
        chapter_content_2 = generate_chapter(chapter_2_prompt, max_tokens=1500)
        generated_chapters.append(chapter_content_2)
        chapter_counter += 1  # Increment chapter counter by 1 for Chapter 2

        # Display the first two chapters
        print("\nGenerated Chapters 1 and 2:")
        for index, chapter in enumerate(generated_chapters[:2], start=1):
            print(f"Chapter {index}:\n{chapter}")
            print("-" * 50)

        # Generate and store summaries for the first two chapters
        for i in range(2):
            summary_prompt = f"Generate the summary of Chapter {i + 1}:\n{generated_chapters[i]}\nSummary:"
            summary = generate_chapter(summary_prompt, max_tokens=300)
            summaries.append(summary)

        # Generate subsequent chapters based on stored summaries
        while True:
            user_input = input("Do you want to generate the next chapter? (yes/no): ").lower()
            if user_input == 'yes':
                new_chapter_prompt = (
                    f"Generate the next chapter based on the story so far:\n"
                    f"Previous chapters explored themes of {', '.join(summaries)}\n\n"
                    f"Chapter Content:\n\n"
                    f"[Chapter Content]\n\n"
                    f"Moral of the Story: {idea}.\n"
                )
                new_chapter_content = generate_chapter(new_chapter_prompt, max_tokens=2500)
                generated_chapters.append(new_chapter_content)
                chapter_counter += 1  # Increment chapter counter by 1 for the additional chapter

                # Generate the summary for the new chapter
                new_summary_prompt = f"Generate the summary of Chapter {chapter_counter}:\n{new_chapter_content}\nSummary:"
                new_summary = generate_chapter(new_summary_prompt, max_tokens=300)
                summaries.append(new_summary)

                # Display the new chapter content
                print(f"\nGenerated Chapter {chapter_counter}:\n{new_chapter_content}")
                print("-" * 50)
            elif user_input == 'no':
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        return generated_chapters, summaries

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"


def main():
    age = int(input("Enter age: "))
    genre = input("Enter genre: ")
    idea = input("Enter story idea: ")
    story_type = input("Enter 'short' for short story or 'long' for long story: ")

    if story_type.lower() == 'short':
        result = generate_short_story(age, genre, idea)
        print("\nGenerated Short Story Content:")
        if result != "Error" and result != "Chapter limit reached.":
            print(result)
        else:
            print("Error occurred while generating the short story.")

    elif story_type.lower() == 'long':
        generated_chapters, summaries = generate_long_story(age, genre, idea)
        print("\nGenerated Long Story Content:")
        if generated_chapters != "Error" and generated_chapters != "Chapter limit reached.":
            for index, chapter in enumerate(generated_chapters, start=1):
                print(f"Chapter {index}:\n{chapter}")
                print("-" * 50)

            if summaries:
                print("\nSummaries:")
                for index, summary in enumerate(summaries, start=1):
                    print(f"Summary of Chapter {index}:\n{summary}")
        else:
            print("Error occurred while generating the long story.")

    else:
        print("Invalid story type input. Please enter 'short' or 'long'.")

if __name__ == "__main__":
    main()