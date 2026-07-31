import re


class M3UParser:

    @staticmethod
    def parse(content):

        channels = []

        current = {}

        for line in content.splitlines():

            line = line.strip()

            if line.startswith("#EXTINF"):

                current = {}

                def get(field):
                    match = re.search(fr'{field}="([^"]*)"', line)
                    return match.group(1) if match else ""

                current["name"] = line.split(",")[-1]
                current["logo"] = get("tvg-logo")
                current["country"] = get("tvg-country")
                current["language"] = get("tvg-language")
                current["category"] = get("group-title")

            elif line.startswith("http"):

                current["url"] = line

                channels.append(current.copy())

        return channels