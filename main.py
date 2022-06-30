import time
from pytube import YouTube
from pytube import Playlist
import concurrent.futures
from pyfiglet import figlet_format
from rich.console import Console
from rich.markdown import Markdown
import os
from datetime import datetime


def convertTime(seconds):
    hours = int(seconds/3600)
    minutes = int((seconds/60) % 60)
    seconds -= hours * 3600 + minutes * 60
    seconds = int(seconds)
    return (hours, minutes, seconds)


def takeInput():

    print(figlet_format("Youtube    Playlist Downloader"))
    console = Console()
    console.print(Markdown("# Made with ❤️  by Harsh Gupta"))
    console.print(
        Markdown("###### I recommend you to run this application on tmux"))

    choices = ["Download a youtube playlist",
               "Download only one youtube video"]
    for index, choice in enumerate(choices):
        console.print(Markdown(f"{index+1}. {choice}"))

    try:
        choice = int(input("\nYour choice - "))
        console.print(
            Markdown(f"## You have chosen to {choices[choice-1].lower()}"))
        print()
    except:
        console.print(Markdown("##### Choice should be a valid number"))
        print()
        quit()

    if choice == 1:
        link = input("Link to the youtube playlist - ")
    elif choice == 2:
        link = input("Link to the youtube video - ")

    return choice, link


def downloadYoutubeVideo(video, dir_name, index):

    console = Console()
    video.title = f"{index+1} - {video.title}"

    if os.path.exists(os.path.join(os.getcwd(), f"{dir_name}/downloaded_videos.txt")):
        with open(f"{dir_name}/downloaded_videos.txt", "r") as file:
            content = file.read()
            if video.title in content:
                console.print(
                    Markdown(f"- Downloaded : {video.title} | {datetime.now()}"))
                return

    console.print(
        Markdown(f"- Downloading : {video.title} | {datetime.now()}"))

    video.streams.filter(mime_type="video/mp4", progressive=True,
                         type="video").order_by("resolution")[-1].download(dir_name)

    console.print(Markdown(f"- Downloaded : {video.title} | {datetime.now()}"))

    with open(f"{dir_name}/downloaded_videos.txt", "a") as file:
        file.write(f"{video.title}\n")


def downloadYoutubePlaylist(link):

    start_time = time.time()
    console = Console()
    try:
        p = Playlist(link)
    except:
        print()
        console.print(Markdown(
            "##### Could not connect to the link that you have input. Check your connection or the link that you have input. Thank you."))
        print()
        quit()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(downloadYoutubeVideo, video, p.title, index)
                   for index, video in enumerate(p.videos)]
        done, not_done = concurrent.futures.wait(
            fs=futures, return_when=concurrent.futures.ALL_COMPLETED)
        if not_done:
            print()
            console.print(
                Markdown(f"##### Could not download all videos from the playlist - {p.title}"))
            console.print(Markdown(f"###### Check downloaded_videos.txt"))
            print()
            quit()
        if done:
            time_taken = time.time() - start_time
            hours, minutes, seconds = convertTime(time_taken)
            print()
            console.print(Markdown(
                f"##### Successfully downloaded all videos from the playlist - {p.title}"))
            print()
            console.print(Markdown(
                f"###### Time taken - {str(hours) + ' hours ' if hours else ''}{str(minutes) + ' minutes ' if minutes else ''}{seconds} seconds"))
            print()


def downloadSingleYouTubeVideo(link):
    console = Console()
    start_time = time.time()
    try:
        video = YouTube(link)
        console.print(
            Markdown(f"- Downloading : {video.title} | {datetime.now()}"))
        video.streams.filter(mime_type="video/mp4", progressive=True,
                             type="video").order_by("resolution")[-1].download("Single YouTube Videos")
        time_taken = time.time() - start_time
        hours, minutes, seconds = convertTime(time_taken)
        print()
        console.print(Markdown(
            f"##### Successfully downloaded the YouTube video - {link}"))
        print()
        console.print(Markdown(
            f"###### Time taken - {str(hours) + ' hours ' if hours else ''}{str(minutes) + ' minutes ' if minutes else ''}{seconds} seconds"))
        print()
    except:
        print()
        console.print(Markdown(
            "##### Could not connect to the link that you have input. Check your connection or the link that you have input. Thank you."))
        print()


def main():

    choice, link = takeInput()

    if choice == 1:
        downloadYoutubePlaylist(link=link)
    elif choice == 2:
        downloadSingleYouTubeVideo(link=link)


if __name__ == "__main__":
    main()
