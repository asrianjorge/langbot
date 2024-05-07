import os

import aiofiles
import pandas as pd


async def get_xlsx(filename: str) -> list:
    path = f"data/{filename}"
    if os.path.exists(path):
        async with aiofiles.open(path, 'r') as f:
            return await pd.read_excel(path)
    return []
