import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from beanie import PydanticObjectId

os.environ.setdefault("DESIGN_ID", "green")

from app.core.creators.static_creator import StaticCreator
from app.core.repository import ui_repo
from app.features.track.route import TrackRequest, recalculate_buyer_type, track
from app.shared.dbmodels import UserAction, get_beanie_models


class StaticCreatorTests(unittest.IsolatedAsyncioTestCase):
    async def test_get_item_loads_static_template_with_impulsive_flag(self):
        doc = SimpleNamespace(json_dict=json.dumps({"id": "hero", "type": "container"}))

        with patch(
            "app.core.creators.static_creator.ui_repo.get_element_by_type",
            new=AsyncMock(return_value=doc),
        ) as get_element:
            result, variables = await StaticCreator("hero_banner").get_item(
                context={"type": "hero_banner", "is_impulsive": True},
            )

        self.assertEqual(result, {"id": "hero", "type": "container"})
        self.assertEqual(variables, [])
        get_element.assert_awaited_once_with("hero_banner", True)

    async def test_get_item_returns_placeholder_when_template_missing(self):
        placeholder = {"type": "footer"}

        with patch(
            "app.core.creators.static_creator.ui_repo.get_element_by_type",
            new=AsyncMock(return_value=None),
        ):
            result, variables = await StaticCreator("footer").get_item(placeholder)

        self.assertIs(result, placeholder)
        self.assertEqual(variables, [])


class UIElementsRepositoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_get_element_by_type_falls_back_when_variant_missing(self):
        fallback = SimpleNamespace(type="product_card")

        with patch(
            "app.core.repository.UIElement.find_one",
            new=AsyncMock(side_effect=[None, fallback]),
        ) as find_one:
            result = await ui_repo.get_element_by_type("product_card", True)

        self.assertIs(result, fallback)
        self.assertEqual(find_one.await_count, 2)


class UserActionModelTests(unittest.TestCase):
    def test_user_action_is_registered_for_beanie(self):
        self.assertIn(UserAction, get_beanie_models())


class TrackRouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_track_saves_action_and_recalculates_for_authenticated_user(self):
        user_id = PydanticObjectId()
        saved_action = SimpleNamespace(save=AsyncMock())

        class FakeUserAction:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

            async def save(self):
                await saved_action.save()

        fake_user = Mock()
        fake_user.link_from_id.return_value = "user-link"

        with (
            patch("app.features.track.route.UserAction", FakeUserAction),
            patch("app.features.track.route.User", fake_user),
            patch(
                "app.features.track.route.recalculate_buyer_type",
                new=AsyncMock(),
            ) as recalculate,
        ):
            response = await track(
                TrackRequest(action_type="add_to_cart", item_id="item-1"),
                user_id=user_id,
            )

        saved_action.save.assert_awaited_once()
        fake_user.link_from_id.assert_called_once_with(user_id)
        recalculate.assert_awaited_once_with(user_id)
        self.assertEqual(response.data, "OK")

    async def test_track_ignores_anonymous_user(self):
        with (
            patch("app.features.track.route.UserAction") as user_action,
            patch(
                "app.features.track.route.recalculate_buyer_type",
                new=AsyncMock(),
            ) as recalculate,
        ):
            response = await track(TrackRequest(action_type="view_product"), user_id=None)

        user_action.assert_not_called()
        recalculate.assert_not_awaited()
        self.assertEqual(response.data, "OK")

    async def test_recalculate_buyer_type_sets_impulsive_when_views_per_purchase_low(self):
        user_id = PydanticObjectId()
        user = SimpleNamespace(is_impulsive=False, save=AsyncMock())

        class FakeField:
            def __eq__(self, other):
                return ("eq", other)

        class FakeLink:
            id = FakeField()

        class FakeQuery:
            async def to_list(self):
                return [
                    SimpleNamespace(action_type="view_product"),
                    SimpleNamespace(action_type="add_to_cart"),
                    SimpleNamespace(action_type="buy"),
                ]

        class FakeUserAction:
            user = FakeLink()

            @classmethod
            def find(cls, *args):
                return FakeQuery()

        fake_user = SimpleNamespace(get=AsyncMock(return_value=user))

        with (
            patch("app.features.track.route.UserAction", FakeUserAction),
            patch("app.features.track.route.User", fake_user),
        ):
            await recalculate_buyer_type(user_id)

        self.assertTrue(user.is_impulsive)
        user.save.assert_awaited_once()

    async def test_recalculate_buyer_type_does_not_save_without_purchases(self):
        user_id = PydanticObjectId()

        class FakeField:
            def __eq__(self, other):
                return ("eq", other)

        class FakeLink:
            id = FakeField()

        class FakeQuery:
            async def to_list(self):
                return [SimpleNamespace(action_type="view_product")]

        class FakeUserAction:
            user = FakeLink()

            @classmethod
            def find(cls, *args):
                return FakeQuery()

        fake_user = SimpleNamespace(get=AsyncMock())

        with (
            patch("app.features.track.route.UserAction", FakeUserAction),
            patch("app.features.track.route.User", fake_user),
        ):
            await recalculate_buyer_type(user_id)

        fake_user.get.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
