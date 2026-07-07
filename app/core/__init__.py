from .builders import GreenPagesBuilder
from .builders import BasePagesBuilder
from .creators import CREATORS_LISTS
import os
from dotenv import load_dotenv

load_dotenv()

builders = [GreenPagesBuilder]


def builders_factory(design_id: str):
    for b in builders:
        if b.DESIGN_ID == design_id:
            return b(CREATORS_LISTS[design_id])

    return BasePagesBuilder([])


page_builder = builders_factory(os.getenv("DESIGN_ID"))
