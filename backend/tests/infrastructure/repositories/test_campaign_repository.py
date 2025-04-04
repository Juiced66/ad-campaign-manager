from datetime import date

import pytest
from sqlalchemy.orm import Session

from app.domain.entities.campaign import Campaign as DomainCampaign
from app.infrastructure.database.sql_alchemy.models.campaign import (
    Campaign as ModelCampaign,
)
from app.infrastructure.repositories.sql_alchemy.campaign import (
    CampaignSqlAlchemyRepository,
)


@pytest.fixture
def campaign_repo(db_session: Session):
    return CampaignSqlAlchemyRepository(db=db_session)


def test_create_and_get_campaign(
    campaign_repo: CampaignSqlAlchemyRepository, db_session: Session
):
    # Arrange
    campaign_entity_to_create = DomainCampaign(
        name="Integration Test",
        description="Testing Repo",
        start_date=date(2024, 2, 1),
        end_date=date(2024, 2, 28),
        budget=500.0,
        is_active=False,
    )

    # Act
    created_entity = campaign_repo.create(entity=campaign_entity_to_create)

    # Assert (Repo return value)
    assert hasattr(created_entity, "id")
    assert created_entity.id is not None
    assert created_entity.name == "Integration Test"

    # Assert (Direct DB check)
    db_campaign = (
        db_session.query(ModelCampaign)
        .filter(ModelCampaign.id == created_entity.id)
        .first()
    )
    assert db_campaign is not None
    assert db_campaign.name == "Integration Test"
    assert db_campaign.budget == 500.0
    assert db_campaign.is_active is False

    # Act (Get)
    retrieved_entity = campaign_repo.get(id=created_entity.id)

    # Assert (Get)
    assert retrieved_entity is not None
    assert retrieved_entity.id == created_entity.id
    assert retrieved_entity.name == created_entity.name


def test_get_multi_filtered(
    campaign_repo: CampaignSqlAlchemyRepository, db_session: Session
):
    c1 = campaign_repo.create(
        entity=DomainCampaign(
            name="Active Campaign 1",
            description="Desc 1",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
            budget=100,
            is_active=True,
        )
    )
    c2 = campaign_repo.create(
        entity=DomainCampaign(
            name="Inactive Campaign",
            description="Desc 2",
            start_date=date(2024, 1, 5),
            end_date=date(2024, 1, 15),
            budget=200,
            is_active=False,
        )
    )
    c3 = campaign_repo.create(
        entity=DomainCampaign(
            name="Active Campaign 2",
            description="Desc 3",
            start_date=date(2024, 1, 12),
            end_date=date(2024, 1, 20),
            budget=300,
            is_active=True,
        )
    )

    active_campaigns = campaign_repo.get_multi_filtered(is_active=True)
    assert len(active_campaigns) == 2
    assert {c.id for c in active_campaigns} == {c1.id, c3.id}

    inactive_campaigns = campaign_repo.get_multi_filtered(is_active=False)

    assert len(inactive_campaigns) == 1

    if len(inactive_campaigns) == 1:
        assert inactive_campaigns[0].id == c2.id

    active_campaigns = campaign_repo.get_multi_filtered(is_active=True)
    assert len(active_campaigns) == 2
    assert {c.id for c in active_campaigns} == {c1.id, c3.id}

    inactive_campaigns = campaign_repo.get_multi_filtered(is_active=False)
    assert len(inactive_campaigns) == 1
    assert inactive_campaigns[0].id == c2.id

    campaigns_after_jan_10 = campaign_repo.get_multi_filtered(
        start_date=date(2024, 1, 11)
    )
    assert len(campaigns_after_jan_10) == 2
