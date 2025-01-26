import scrapy
from config import categories
import json
import mwparserfromhell


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["ne.wikipedia.org"]

    def __init__(self, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.data_list = []

    # function to generate offset for each cateogory
    def split_number(self, number, part_size=500):
        parts = []
        while number >= part_size:
            parts.append(part_size)
            number -= part_size
        if number > 0:
            parts.append(number)
        return parts

    def start_requests(self):
        for indv_category, total_result in categories.items():
            # Generate all offsets
            offsets = [offset for offset in range(0, total_result, 500)]
            # Generate srlimit values
            limits = self.split_number(total_result)

            for i, offset in enumerate(offsets):
                # Ensure that srlimit matches the number of items remaining
                srlimit = limits[i] if i < len(limits) else 500
                url = f"https://ne.wikipedia.org/w/api.php?action=query&list=search&srsearch={indv_category}&srlimit={srlimit}&sroffset={offset}&format=json"
                yield scrapy.Request(
                    url, callback=self.parse_listing, meta={"category": indv_category}
                )

    def parse_listing(self, response):
        category = response.meta["category"]
        data = json.loads(response.body)
        for result in data["query"]["search"]:
            self.logger.info("PAGE ID")
            self.logger.info(result["pageid"])
            yield scrapy.Request(
                f"https://ne.wikipedia.org/w/api.php?action=query&prop=revisions&rvslots=main&rvprop=content&pageids={result['pageid']}&format=json",
                callback=self.parse_article,
                meta={"category": category, "page_id": result["pageid"]},
            )

    def parse_article(self, response):
        category = response.meta["category"]
        page_id = response.meta["page_id"]
        page_id = str(page_id)
        data = response.json()

        try:
            title = data["query"]["pages"][page_id]["title"]
            wikitext = data["query"]["pages"][page_id]["revisions"][0]["slots"]["main"][
                "*"
            ]
        except Exception as e:
            wikitext = None
            self.logger.info(f"Couldn't parse: {response.request.url} {str(e)}")

        if wikitext and title:
            # Parse the wikitext using mwparserfromhell

            text = mwparserfromhell.parse(wikitext)
            # Extract the plain text (without any wiki syntax)
            plain_text = text.strip_code()

            scraped_data = {
                "title": title,
                "text": plain_text,
            }
            self.data_list.append(scraped_data)

            with open(f"{category}.json", "w", encoding="utf-8") as json_file:
                json.dump(self.data_list, json_file, ensure_ascii=False, indent=4)
