import sys
from pathlib import Path
from docx import Document
from pptx import Presentation

BASE = Path(__file__).resolve().parent.parent
docx_path = BASE / "artifacts" / "project_report.docx"
pptx_path = BASE / "artifacts" / "project_presentation.pptx"
md_path = BASE / "docs" / "project_report.md"
readme_path = BASE / "README.md"

print("========================================")
print("ACADEMIC DOCUMENTS AUDIT INSPECTION")
print("========================================")

has_failure = False

# 1. WORD REPORT AUDIT
print("\n[1] WORD REPORT (.docx) AUDIT:")
if not docx_path.exists():
    print("[FAIL] ERROR: Word report does not exist!")
    has_failure = True
else:
    doc = Document(str(docx_path))
    print(f"[PASS] File: {docx_path.name}")
    print(f"[PASS] Total Paragraphs: {len(doc.paragraphs)}")
    print(f"[PASS] Total Tables: {len(doc.tables)}")

    doc_text = " ".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])

    # Check Team Number 22
    if "Team Number 22" in doc_text:
        print("[PASS] Verified Team Identification: 'Team Number 22' is present.")
    else:
        print("[FAIL] ERROR: 'Team Number 22' is missing from Word report.")
        has_failure = True

    # Check that roll numbers / roll placeholders are ABSENT
    roll_markers = ["[ROLL_NO_", "Roll No", "Roll Number", "[ROLL_NO_1]"]
    found_roll_markers = [rm for rm in roll_markers if rm.lower() in doc_text.lower()]
    if not found_roll_markers:
        print("[PASS] Verified: All roll numbers, roll markers, and [ROLL_NO_X] placeholders are ABSENT.")
    else:
        print(f"[FAIL] Found roll number references in Word report: {found_roll_markers}")
        has_failure = True

    # Check that institutional placeholders are ABSENT
    undesired_placeholders = [
        "[INSTITUTION_NAME]", "[COURSE_OR_DEPARTMENT]", "[MENTOR_NAME]",
        "[MENTOR_DESIGNATION]", "[SUBMISSION_DATE]", "[SEAL]"
    ]
    found_undesired = [up for up in undesired_placeholders if up in doc_text]
    if not found_undesired:
        print("[PASS] Verified: Institution, department, mentor, and date placeholders are ABSENT.")
    else:
        print(f"[FAIL] Found unremoved placeholders: {found_undesired}")
        has_failure = True

# 2. POWERPOINT AUDIT
print("\n[2] POWERPOINT PRESENTATION (.pptx) AUDIT:")
if not pptx_path.exists():
    print("[FAIL] ERROR: PowerPoint presentation does not exist!")
    has_failure = True
else:
    prs = Presentation(str(pptx_path))
    print(f"[PASS] File: {pptx_path.name}")
    print(f"[PASS] Total Slides: {len(prs.slides)}")

    ppt_text = " ".join([sh.text_frame.text for s in prs.slides for sh in s.shapes if sh.has_text_frame])

    if "Team Number 22" in ppt_text:
        print("[PASS] Verified Team Identification: 'Team Number 22' is present on Slide 1.")
    else:
        print("[FAIL] ERROR: 'Team Number 22' is missing from PowerPoint presentation.")
        has_failure = True

    found_ppt_rolls = [rm for rm in roll_markers if rm.lower() in ppt_text.lower()]
    if not found_ppt_rolls:
        print("[PASS] Verified: All roll numbers, roll markers, and [ROLL_NO_X] placeholders are ABSENT in PowerPoint.")
    else:
        print(f"[FAIL] Found roll number references in PowerPoint: {found_ppt_rolls}")
        has_failure = True

    found_undesired_ppt = [up for up in undesired_placeholders if up in ppt_text]
    if not found_undesired_ppt:
        print("[PASS] Verified: Institution, department, mentor, and date placeholders are ABSENT in PowerPoint.")
    else:
        print(f"[FAIL] Found unremoved placeholders in PowerPoint: {found_undesired_ppt}")
        has_failure = True

# 3. MARKDOWN REPORT & README AUDIT
print("\n[3] MARKDOWN REPORT & README AUDIT:")
for p, name in [(md_path, "Markdown Report"), (readme_path, "README.md")]:
    if not p.exists():
        print(f"[FAIL] ERROR: {name} does not exist!")
        has_failure = True
    else:
        text = p.read_text(encoding="utf-8")
        if "Team Number 22" in text:
            print(f"[PASS] {name}: Verified 'Team Number 22' present.")
        else:
            print(f"[FAIL] {name}: 'Team Number 22' missing.")
            has_failure = True
        
        found_rolls = [rm for rm in roll_markers if rm.lower() in text.lower()]
        if not found_rolls:
            print(f"[PASS] {name}: No roll numbers or [ROLL_NO_X] placeholders found.")
        else:
            print(f"[FAIL] {name}: Found roll number references: {found_rolls}")
            has_failure = True

print("\n========================================")
if has_failure:
    print("[FAIL] Pre-submission document audit FAILED.")
    sys.exit(1)
else:
    print("[SUCCESS] All pre-submission document checks PASSED cleanly.")
    print("========================================")
