import pytest

from src.application.exceptions import AdNotFoundError
from src.application.usecases.create_ad import CreateAd
from src.application.usecases.delete_ad import DeleteAd
from src.application.usecases.increment_views import IncrementViews
from tests.conftest import FakeUnitOfWork


@pytest.mark.asyncio
async def test_increment_views_increases_counter(fake_uow: FakeUnitOfWork) -> None:
    create = CreateAd(fake_uow)
    ad = await create.execute(
        user_id=1, title="T", description="d", price=100, category="c", city="x"
    )
    assert ad.views == 0

    uc = IncrementViews(fake_uow)
    await uc.execute(ad.id)
    await uc.execute(ad.id)

    saved = await fake_uow.ads.get_by_id(ad.id)
    assert saved is not None
    assert saved.views == 2


@pytest.mark.asyncio
async def test_increment_views_not_found(fake_uow: FakeUnitOfWork) -> None:
    uc = IncrementViews(fake_uow)

    with pytest.raises(AdNotFoundError):
        await uc.execute(999)


@pytest.mark.asyncio
async def test_increment_views_archived_raises(fake_uow: FakeUnitOfWork) -> None:
    create = CreateAd(fake_uow)
    ad = await create.execute(
        user_id=1, title="T", description="d", price=100, category="c", city="x"
    )
    await DeleteAd(fake_uow).execute(ad_id=ad.id, user_id=1)

    uc = IncrementViews(fake_uow)
    with pytest.raises(AdNotFoundError):
        await uc.execute(ad.id)
