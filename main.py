from src.app.lifespan import lifespan
from asyncio import run
from pathlib import Path
from sys import argv
from src.app.modules.text_ripping.presentation.cli.on_ripping_pdf_text import (
    on_ripping_pdf_text,
)


async def main():
    if len(argv) < 2:
        print("❗請拖曳一個或多個檔案進來，至少要提供一個路徑")
        return
    input_file_paths = (
        path for arg in argv[1:] if (path := Path(arg).resolve()).is_file()
    )
    async with lifespan() as injector:
        for input_file_path in input_file_paths:
            output_file_name = input_file_path.with_suffix(".txt").name
            output_file_path = Path.cwd() / output_file_name
            await injector.call_with_injection(
                on_ripping_pdf_text,
                args=(str(input_file_path), str(output_file_path)),
            )


if __name__ == "__main__":
    run(main())
