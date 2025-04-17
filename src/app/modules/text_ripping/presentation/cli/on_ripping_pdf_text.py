from dependency_injector.wiring import inject, Provide
from app.container import Container
from aiofiles import open as aioopen
from app.modules.text_ripping.application.rip_text import RippingPDFText, RipPDFText


@inject
async def on_ripping_pdf_text(
    input_path: str,
    output_path: str,
    /,
    handler: RipPDFText = Provide[Container.rip_pdf_text],
):
    async with aioopen(input_path, "rb") as input:
        pdf = await input.read()
        query = RippingPDFText(pdf=pdf)
        text = await handler(query)
        async with aioopen(output_path, "w", encoding="utf-8") as output:
            await output.write(text)
