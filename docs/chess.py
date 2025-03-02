import requests
from bs4 import BeautifulSoup

url = "https://www.thechesswebsite.com/chess-openings/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
#
# table = soup.find('div', id='cb-container')
# rows = table.find_all('tr')

# table = soup.find('/html/body/div[2]/section/div/div/div/div[3]/div')
#
# print(table)


table = soup.select_one("body > div:nth-of-type(2) > section > div > div > div > div:nth-of-type(3) > div")
# print(table)

# /html/body/div[2]/section/div/div/div/div[3]/div

# print("\n\n\n ok \n\n\n")


all_As = table.find_all("a")

imgs = []
names = []
for a in all_As:
    # Extract the link (href attribute)
    link = a["href"]

    # Extract the image URL (src attribute of <img>)
    image_src = a.find("img")["src"]

    # Extract the title text inside <h5>
    title = a.find("h5").text

    imgs.append(image_src)
    names.append(title)

    # print("=========================================")
    #
    #
    # print(link)
    # print(image_src)
    # imgs.append(image_src)
    # print(title)
    # names.append(title)
    #
    # # Check if <span> exists inside the <a> tag
    # if a.find("span"):
    #     print("This link has a MEMBERS ONLY tag.")
    # else:
    #     print("This link is public.")
    #
    # print("========================================= \n")

# def write_row(src, start, f):
#     for i in range(4):
#         if start + i < len(src):
#             if src == imgs:
#                 f.write(f'| ![failed to load image]({src[start + i]})')
#             else:
#                 f.write('|' + src[start + i])
#         else:
#             f.write('|')
#     f.write('|\n')


from duckduckgo_search import DDGS

ddgs = DDGS()

def opening(op_name):
    with open(f"{op_name.replace(' ', '-')}.md", "w", encoding="utf-8") as file:
        results = list(ddgs.text(op_name.lower(), max_results=3))

        file.write("# " + op_name + "\n")

        for result in results:
            page_title = result.get("title", "No title")
            href = result.get("href", "No link")
            snippet = result.get("body", "No description")

            file.write(f"- ## **{page_title}** \n")
            file.write("\n---\n")
            file.write(f"### Desc: \n {snippet} \n")
            file.write(f"### Read more : [here]({href}) \n")


        file.write("\n\n")
        file.write("[← Back to the list](chess-openings.md)")



def write_op(src_img, src_nam, start, f):
    if start < len(src_nam):
        opening(src_nam[start])

        f.write("## [")
        f.write(src_nam[start])
        f.write("](")
        f.write(src_nam[start].replace(" ", "-"))
        f.write(".md) \n")

        f.write("\n\n --- \n\n")

        f.write("[![failed to load photo](")
        f.write(src_img[start])
        f.write(")](")
        f.write(src_nam[start].replace(" ", "-"))
        f.write(".md) \n")
        f.write('\n')

        print("done ", start)


from pathlib import Path




def to_md():
    with open("chess-openings.md", "w", encoding="utf-8") as file:
        file.write("# Chess Openings List\n\n")
        file.write("[←  Back to Home](README.md) \n")
        file.write("\n---\n")

        j = 0
        while j < len(imgs) and j < 16:
            write_op(imgs, names, j, file)
            j += 1


def make_README():
    with open("README.md", "w", encoding="utf-8") as file:
        file.write("# Chess Openings\n")
        file.write("\n---\n")

        result = DDGS().chat("Explain what a chess opening is and its importance in chess")

        file.write(f"\n{result} <br>\n\n")

        file.write("[→ Go to Chess Openings List](chess-openings.md)")


if __name__ == '__main__':
    make_README()
    to_md()