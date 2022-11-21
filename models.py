
from gino import Gino

from errors import NotFound


DSN = "postgresql+asyncpg://rest-api-application:1234@localhost:8000/advertisements"

db = Gino()


class Ads(db.Model):
    __tablename__ = "advertisements"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    published_at = db.Column(db.DateTime(), server_default=db.func.now())
    owner = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"Advertisement: id={self.id!r}, \
                published at={self.published_at.isoformat()}, \
                owner={self.owner}"


async def get_item(db_table, ads_id: int):
    ads = await db_table.get(ads_id)
    if ads is None:
        raise NotFound("Resource not found")
    return ads


async def db_init(app):
    await db.set_bind(DSN)
    print('Database connect on localhost:8000')
    await db.gino.create_all()
    yield
    await db.pop_bind().close()