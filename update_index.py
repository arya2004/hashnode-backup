import os


index_file = "index.md"


base_url = "https://github.com/arya2004/hashnode-backup/blob/main/"


def read_existing_entries(index_file):
    if not os.path.exists(index_file):
        return set()
    with open(index_file, "r") as f:
        return set(line.strip() for line in f if line.startswith("- ["))


def append_to_index(file_name, link):
    with open(index_file, "a") as f:
        f.write(f"- [{file_name}]({link})\n")


md_files = [
    f for f in os.listdir(".") if f.endswith(".md") and f != index_file
]

existing_entries = read_existing_entries(index_file)


for file_name in md_files:
    file_link = base_url + file_name
    entry = f"- [{file_name}]({file_link})"
    if entry not in existing_entries:
        append_to_index(file_name, file_link)
