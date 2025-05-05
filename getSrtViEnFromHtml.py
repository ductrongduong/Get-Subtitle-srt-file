import re
from bs4 import BeautifulSoup

# List of filenames
# filenames = [f'h{i}' for i in range(1, 8)]
filenames = ['br_s2_e9', 'the_social_network']

# Function to convert time format
def convert_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds)
    h = s // 3600
    s = s % 3600
    m = s // 60
    s = s % 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

for filename in filenames:
    # Read the HTML file
    with open('../sub/' + filename + '.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all subtitle spans
    subtitles = soup.find_all('span', id=re.compile('^cue'))

    # Create SRT content for English and Vietnamese
    srt_content_en = ""
    srt_content_vi = ""
    for index, subtitle in enumerate(subtitles):
        start = float(subtitle['data-start'])
        stop = float(subtitle['data-stop'])
        text_en = subtitle.find('span', class_='js-textEn').text.strip()
        text_vi = subtitle.find('small', class_='js-textVi').text.strip()

        srt_content_en += f"{index + 1}\n"
        srt_content_en += f"{convert_time(start)} --> {convert_time(stop)}\n"
        srt_content_en += f"{text_en}\n\n"

        srt_content_vi += f"{index + 1}\n"
        srt_content_vi += f"{convert_time(start)} --> {convert_time(stop)}\n"
        srt_content_vi += f"{text_vi}\n\n"

    # Write to English SRT file
    with open('../sub/' + filename + '_en.srt', 'w', encoding='utf-8') as file:
        file.write(srt_content_en)

    # Write to Vietnamese SRT file
    with open('../sub/' + filename + '_vi.srt', 'w', encoding='utf-8') as file:
        file.write(srt_content_vi)

    print(f"English and Vietnamese SRT files created successfully for {filename}.")