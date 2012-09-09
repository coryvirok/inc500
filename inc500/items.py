# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Inc500Item(Item):
    rank = Field()
    company_name = Field()
    blurb = Field()
    three_year_pct_growth = Field()
    revenue_2010 = Field()
    revenue_2007 = Field()
    num_employees = Field()
    employee_growth = Field()
    founded = Field()
    industry = Field()
    industry_rank = Field()
    city = Field()
    state = Field()
    link = Field()
