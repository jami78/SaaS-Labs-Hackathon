from fastapi import APIRouter, File, Depends, UploadFile
from typing import Optional
from app.schemas.content_schema import InputProcess, ContentResponse
from app.graphs.pricing_workflow import workflow
from pathlib import Path
import uuid

router = APIRouter()

@router.post("/pricing/", response_model=ContentResponse)
def process_content(
    input_data: InputProcess = Depends(),
    pdf_file: Optional[UploadFile] = File(None),
    excel_file: Optional[UploadFile] = File(None)
):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    pdf_path = upload_dir / "context.pdf"
    if pdf_file:
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.file.read())
        print(f"PDF saved to: {pdf_path}")

    excel_path = upload_dir / "finance_data.xlsx"
    if excel_file:
        with open(excel_path, "wb") as f:
            f.write(excel_file.file.read())
        print(f" Excel file saved to: {excel_path}")

    state = {"user_input": input_data.input}
    config = {"configurable": {"thread_id": uuid.uuid4()}}
    result = workflow.invoke(state, config)

    return ContentResponse(
        response=result.get("messages", "")
    )
