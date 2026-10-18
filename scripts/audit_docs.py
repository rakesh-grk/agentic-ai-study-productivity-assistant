from pathlib import Path
from docx import Document
from pptx import Presentation

BASE = Path(__file__).resolve().parent.parent
docx_path = BASE / "artifacts" / "project_report.docx"
pptx_path = BASE / "artifacts" / "project_presentation.pptx"

print("--- WORD REPORT AUDIT ---")
if not docx_path.exists():
    print("ERROR: Word report does not exist!")
else:
    doc = Document(str(docx_path))
    print(f"File exists: {docx_path}")
    print(f"Total Paragraphs: {len(doc.paragraphs)}")
    print(f"Total Tables: {len(doc.tables)}")
    
    # Check for student name
    doc_text = " ".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])
    if "G. Rakesh Kumar" in doc_text:
        print("[SUCCESS] Candidate Name 'G. Rakesh Kumar' found in Word report.")
    else:
        print("[WARNING] Candidate Name 'G. Rakesh Kumar' missing from Word report.")
        
    placeholders_found = set()
    for word in ["[STUDENT_ID]", "[COURSE_OR_DEPARTMENT]", "[INSTITUTION_NAME]", "[SUBMISSION_DATE]", "[MENTOR_NAME]"]:
        if word in doc_text:
            placeholders_found.add(word)
    print(f"Institutional Placeholders remaining for submission: {sorted(list(placeholders_found))}")

print("\n--- POWERPOINT AUDIT ---")
if not pptx_path.exists():
    print("ERROR: PowerPoint does not exist!")
else:
    prs = Presentation(str(pptx_path))
    print(f"File exists: {pptx_path}")
    print(f"Total Slides: {len(prs.slides)}")
    ppt_text = " ".join([shape.text_frame.text for s in prs.slides for shape in s.shapes if shape.has_text_frame])
    if "G. Rakesh Kumar" in ppt_text:
        print("[SUCCESS] Candidate Name 'G. Rakesh Kumar' found in PowerPoint presentation.")
    else:
        print("[WARNING] Candidate Name 'G. Rakesh Kumar' missing from PowerPoint presentation.")

print("\n[SUCCESS] Inspection script complete.")
