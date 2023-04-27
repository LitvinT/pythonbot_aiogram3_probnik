import os
from json import loads
from urllib.parse import urlsplit

from aiohttp import ClientSession
from aiofiles import open as aiopen
from sqlalchemy.exc import IntegrityError

from models import Product, Brand, Model, ProductImage, Sex,Category
from loader import BASE_DIR


async def parse_stockx(category: str, limit: int = 100, page: int = 1):
    if category.lower() in ('sneakers', 'shoes'):
        async with aiopen(os.path.join(BASE_DIR, 'stockx_headers.json'), 'r', encoding='utf-8') as file:
            headers = loads(await file.read())
        async with ClientSession(
                headers=headers
        ) as session:
            async with session.post(
                url='https://stockx.com/api/p/e',
                json={
                    "query": "query Browse($category: String, $filters: [BrowseFilterInput], $filtersVersion: Int, $query: String, $sort: BrowseSortInput, $page: BrowsePageInput, $currency: CurrencyCode, $country: String!, $market: String, $staticRanking: BrowseExperimentStaticRankingInput, $skipFollowed: Boolean!) {\n  browse(\n    category: $category\n    filters: $filters\n    filtersVersion: $filtersVersion\n    query: $query\n    sort: $sort\n    page: $page\n    experiments: {staticRanking: $staticRanking}\n  ) {\n    results {\n      edges {\n        objectId\n        node {\n          ... on Product {\n            ...BrowseProductDetailsFragment\n            ...FollowedFragment @skip(if: $skipFollowed)\n            ...ProductTraitsFragment\n            market(currencyCode: $currency) {\n              ...MarketFragment\n            }\n          }\n          ... on Variant {\n            id\n            followed @skip(if: $skipFollowed)\n            product {\n              ...BrowseProductDetailsFragment\n              traits(filterTypes: [RELEASE_DATE, RETAIL_PRICE]) {\n                name\n                value\n              }\n            }\n            market(currencyCode: $currency) {\n              ...MarketFragment\n            }\n            traits {\n              size\n            }\n          }\n        }\n      }\n      pageInfo {\n        limit\n        page\n        pageCount\n        queryId\n        queryIndex\n        total\n      }\n    }\n    query\n  }\n}\n\nfragment FollowedFragment on Product {\n  followed\n}\n\nfragment ProductTraitsFragment on Product {\n  productTraits: traits(filterTypes: [RELEASE_DATE, RETAIL_PRICE]) {\n    name\n    value\n  }\n}\n\nfragment MarketFragment on Market {\n  currencyCode\n  bidAskData(market: $market, country: $country) {\n    lowestAsk\n    highestBid\n    lastHighestBidTime\n    lastLowestAskTime\n  }\n  state(country: $country) {\n    numberOfCustodialAsks\n  }\n  salesInformation {\n    lastSale\n    lastSaleDate\n    salesThisPeriod\n    salesLastPeriod\n    changeValue\n    changePercentage\n    volatility\n    pricePremium\n  }\n  deadStock {\n    sold\n    averagePrice\n  }\n}\n\nfragment BrowseProductDetailsFragment on Product {\n  id\n  name\n  urlKey\n  title\n  brand\n  description\n  model\n  condition\n  productCategory\n  listingType\n  media {\n    thumbUrl\n    smallImageUrl\n  }\n}\n",
                    "variables": {
                        "category": category.lower(),
                        "filters": [
                            {
                                "id": "browseVerticals",
                                "selectedValues": [category.lower()]}
                        ],
                        "filtersVersion": 4,
                        "sort": {
                            "id": "most-active",
                            "order": "DESC"
                        },
                        "page": {
                            "index": page,
                            "limit": limit
                        },
                        "currency": "USD",
                        "country": "US",

                        "market": "US",
                        "query": "",
                        "staticRanking": {
                            "enabled": False
                        },
                        "skipFollowed": True
                    },
                    "operationName": "Browse"
                }
            ) as response:
                if response.status == 200:
                    sex_list = await Sex.all()
                    edges = (await response.json())['data']['browse']['results']['edges']
                    for rating, line in enumerate(edges):
                        print(line)
                        brand = await Brand.all(name=line['node']['brand'])
                        if not brand:
                            brand = Brand(name=line['node']['brand'])
                            await brand.save()
                        else:
                            brand = brand[0]

                        model = await Model.all(name=line['node']['model'])
                        if not model:
                            model = Model(name=line['node']['model'], brand_id=brand.id)
                            await model.save()
                        else:
                            model = model[0]
                        sex_id = 1
                        if '(W)' in line['node']['title']:
                            sex_id = 2
                        elif '(GS)' in line['node']['title']:
                            sex_id = 3
                        elif '(PS)' in line['node']['title']:
                            sex_id = 4
                        elif '(TD)' in line['node']['title']:
                            sex_id = 6
                        elif '(I)' in line['node']['title'] or 'Infant' in line['node']['title']:
                            sex_id = 5
                        product = Product(
                            article=line['node']['id'],
                            brand_id=brand.id,
                            model_id=model.id,
                            name=line['node']['name'],
                            title=line['node']['title'],
                            category_id=1,
                            price=line['node']['market']['salesInformation']['lastSale'],
                            rating=rating,
                            sex_id=sex_id
                        )
                        try:
                            await product.save()
                        except IntegrityError:
                            pass
                        else:
                            base_url = line['node']['media']['thumbUrl'][:line['node']['media']['thumbUrl'].find('.jpg')+4]
                            path = urlsplit(base_url).path.removeprefix('/images/').replace('-Product', '').split('.jpg')[0]
                            response = await session.get(url=f'https://images.stockx.com/360/{path}/Images/{path}/Lv2/img01.jpg')
                            if response.status == 200:
                                for i in range(1, 22, 5):
                                    i = str(i).zfill(2)
                                    url = f'https://images.stockx.com/360/{path}/Images/{path}/Lv2/img{i}.jpg'
                                    image = ProductImage(
                                        product_id=product.id,
                                        url=url
                                    )
                                    try:
                                        await image.save()
                                    except IntegrityError:
                                        pass
                            else:
                                image = ProductImage(
                                    product_id=product.id,
                                    url=base_url
                                )
                                try:
                                    await image.save()
                                    print(product.title)
                                    print(image.url)
                                except IntegrityError:
                                    pass
    else:
        raise ValueError('incorrect argument `category`')
