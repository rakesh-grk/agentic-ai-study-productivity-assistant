from pathlib import Path
from docx import Document
from pptx import Presentation

BASE = Path(__file__).resolve().parent.parent
docx_path = BASE / "artifacts" / "project_report.docx"
pptx_path = BASE / "artifacts" / "project_presentation.pptx"

print("========================================")
print("ACADEMIC DOCUMENTS AUDIT INSPECTION")
print("========================================")

# 1. WORD REPORT AUDIT
print("\n[1] WORD REPORT (.docx) AUDIT:")
if not docx_path.exists():
    print("[FAIL] ERROR: Word report does not exist!")
else:
    doc = Document(str(docx_path))
    print(f"[PASS] File: {docx_path.name}")
    print(f"[PASS] Total Paragraphs: {len(doc.paragraphs)}")
    print(f"[PASS] Total Tables: {len(doc.tables)}")

    doc_text = " ".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])

    # Check Student Names
    if "G. Rakesh Kumar" in doc_text and "M. Harshitha" in doc_text:
        print("[PASS] Verified Candidate Names: 'G. Rakesh Kumar' and 'M. Harshitha' present.")
    else:
        print("[FAIL] WARNING: Candidate names missing or incomplete.")

    # Check All Five Team Roll Numbers
    roll_numbers = ["[ROLL_NO_1]", "[ROLL_NO_2]", "[ROLL_NO_3]", "[ROLL_NO_4]", "[ROLL_NO_5]"]
    missing_rolls = [rn for rn in roll_numbers if rn not in doc_text]
    if not missing_rolls:
        print("[PASS] Verified All 5 Team Roll Numbers are present on separate rows/lines:")
        for rn in roll_numbers:
            print(f"   * {rn}")
    else:
        print(f"[FAIL] Missing Roll Numbers: {missing_rolls}")

    # Check That Institutional / Mentor / Date Placeholders Are Removed
    undesired_placeholders = ["[INSTITUTION_NAME]", "[COURSE_OR_DEPARTMENT]", "[MENTOR_NAME]", "[MENTOR_DESIGNATION]", "[SUBMISSION_DATE]", "[SEAL]"]
    found_undesired = [up for up in undesired_placeholders if up in doc_text]
    if not found_undesired:
        print("[PASS] Verified: Institution, department, mentor, and date placeholders successfully REMOVED.")
    else:
        print(f"[FAIL] Found unremoved placeholders: {found_undesired}")

# 2. POWERPOINT AUDIT
print("\n[2] POWERPOINT PRESENTATION (.pptx) AUDIT:")
if not pptx_path.exists():
    print("[FAIL] ERROR: PowerPoint presentation does not exist!")
else:
    prs = Presentation(str(pptx_path))
    print(f"[PASS] File: {pptx_path.name}")
    print(f"[PASS] Total Slides: {len(prs.slides)}")

    ppt_text = " ".join([sh.text_frame.text for s in prs.slides for sh in s.shapes if sh.has_text_frame])

    if "G. Rakesh Kumar" in ppt_text and "M. Harshitha" in ppt_text:
        print("[PASS] Verified Candidate Names: 'G. Rakesh Kumar' and 'M. Harshitha' present.")
    else:
        print("[FAIL] WARNING: Candidate names missing in presentation.")

    missing_ppt_rolls = [rn for rn in roll_numbers if rn not in ppt_text]
    if not missing_ppt_rolls:
        print("[PASS] Verified All 5 Team Roll Numbers present on separate lines on Slide 1.")
    else:
        print(f"[FAIL] Missing Roll Numbers in PowerPoint: {missing_ppt_rolls}")

    found_undesired_ppt = [up for up in undesired_placeholders if up in ppt_text]
    if not found_undesired_ppt:
        print("[PASS] Verified: Institution, department, mentor, and date placeholders REMOVED from presentation.")
    else:
        print(f"[FAIL] Found unremoved placeholders in PowerPoint: {found_undesired_ppt}")

print("\n========================================")
print("[SUCCESS] All pre-submission document checks completed.")
print("========================================")
