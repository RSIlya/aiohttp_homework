import json

from aiohttp import web

import models as db

from validation import validate, PostAds, PatchAds


app = web.Application()


def json_response(
    data,
    status: int = 200,
    content_type: str = "application/json",
) -> web.Response:
    text = json.dumps(data, ensure_ascii=False)
    return web.Response(
        text=text,
        status=status,
        content_type=content_type,
    )


class AdsView(web.View):

    async def get(self):
        ads_id = int(self.request.match_info['ads_id'])
        ads = await db.get_item(db.Ads, ads_id)
        return json_response(dict(
            id=ads.id,
            title=ads.title,
            description=ads.description,
            owner=ads.owner,
            published_at=ads.published_at.isoformat()
        ))

    async def post(self):
        req_json = validate(PostAds, await self.request.json())
        new_ads = await db.Ads.create(**req_json)
        return json_response(
            {
            "ads_id": new_ads.id,
            "published_at": new_ads.published_at.isoformat()
            }
        )

    async def patch(self):
        ads_id = int(self.request.match_info['ads_id'])
        req_json = validate(PatchAds, await self.request.json())
        ads = await db.get_item(db.Ads, ads_id)
        if req_json.get('title'):
                ads.title = req_json['title']
        if req_json.get('description'):
            ads.description = req_json['description']
        await ads.update(title=ads.title, description=ads.description).apply()
        return json_response({
                'status': 'success',
            })

    async def delete(self):
        ads_id = int(self.request.match_info['ads_id'])
        ads = await db.get_item(db.Ads, ads_id)
        await ads.delete()
        return json_response("", status=204)


routes =[
    web.get('/ads/{ads_id:\d+}', AdsView),
    web.post('/ads/', AdsView),
    web.patch('/ads/{ads_id:\d+}', AdsView),
    web.delete('/ads/{ads_id:\d+}', AdsView),
]

app.add_routes(routes)
app.cleanup_ctx.append(db.db_init)

if __name__ == "__main__":
    web.run_app(app)