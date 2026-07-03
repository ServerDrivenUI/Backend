from .repository import repo
import pydivkit as dk
import json


class Service:
    def test(self):
        slider = dk.DivData(
            log_id="sample_card",
            states=[
                dk.DivDataState(
                    state_id=0,
                    div=dk.DivSlider(
                        width=dk.DivMatchParentSize(),
                        max_value=10,
                        min_value=1,
                        thumb_style=dk.DivShapeDrawable(
                            color="#00b300",
                            stroke=dk.DivStroke(
                                color="#ffffff",
                                width=3,
                            ),
                            shape=dk.DivRoundedRectangleShape(
                                item_width=dk.DivFixedSize(value=32),
                                item_height=dk.DivFixedSize(value=32),
                                corner_radius=dk.DivFixedSize(value=100),
                            ),
                        ),
                        track_active_style=dk.DivShapeDrawable(
                            color="#00b300",
                            shape=dk.DivRoundedRectangleShape(
                                item_height=dk.DivFixedSize(value=6)
                            ),
                        ),
                        track_inactive_style=dk.DivShapeDrawable(
                            color="#20000000",
                            shape=dk.DivRoundedRectangleShape(
                                item_height=dk.DivFixedSize(value=6)
                            ),
                        ),
                    ),
                )
            ],
        )
        print(json.dumps(slider.dict(), indent=1))


test_service = Service()
