from aiofiles import open as aioopen
from app.modules.text_ripping.application.queries.rip_text import (
    RippingPDFText,
    RipPDFText,
)
from injector import inject


@inject
async def on_ripping_pdf_text(
    input_path: str, output_path: str, /, handler: RipPDFText
):
    async with aioopen(input_path, "rb") as input:
        pdf = await input.read()
        mutation = RippingPDFText(pdf=pdf)
        text = await handler(mutation)
        async with aioopen(output_path, "w", encoding="utf-8") as output:
            await output.write(text)
