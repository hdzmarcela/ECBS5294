# Google Sheet Booking Template for Interview Simulations

**Instructions for Setting Up Student Booking Sheet**

---

## Overview

This document provides the structure and instructions for creating a Google Sheet where students can book their whiteboard interview simulation timeslots.

---

## Sheet Setup Instructions

### 1. Create a New Google Sheet

1. Go to https://sheets.google.com
2. Create a new blank spreadsheet
3. Name it: **"ECBS5294 - SQL Interview Simulations - Booking Sheet"**

### 2. Configure Sharing Settings

**Important:** Set permissions correctly!

1. Click **Share** (top right)
2. Change access to: **"Anyone with the link can EDIT"**
   - This allows students to sign up without requesting access
   - Alternative: Share with your institution domain (e.g., @ceu.edu can edit)
3. Copy the shareable link → This goes in your student announcement

### 3. Create the Header

**Row 1 (Header):**

| A: Date | B: Time | C: Scenario | D: Student Name | E: Student Email | F: Status | G: Notes |
|---------|---------|-------------|------------------|------------------|-----------|----------|

**Format the header:**
- Bold text
- Background color: Light blue or gray
- Freeze Row 1 (View → Freeze → 1 row)

### 4. Add Scenario Options (Column C)

Use **Data Validation** to create a dropdown:

1. Select Column C (starting at C2, not the header)
2. Go to Data → Data Validation
3. Criteria: List of items
4. Items:
   ```
   Scenario 1: E-Commerce Analytics
   Scenario 2: SaaS Product Analytics
   Scenario 3: Retail Store Operations
   ```
5. Check "Show dropdown list in cell"
6. Save

### 5. Add Status Options (Column F)

Use **Data Validation** again:

1. Select Column F (starting at F2)
2. Data → Data Validation
3. Criteria: List of items
4. Items:
   ```
   Available
   Booked
   Completed
   Canceled
   ```
5. Optional: Set up **conditional formatting**:
   - Available = Green background
   - Booked = Yellow background
   - Completed = Blue background
   - Canceled = Red background

### 6. Pre-Fill Timeslots

**Example:**

| Date | Time | Scenario | Student Name | Student Email | Status | Notes |
|------|------|----------|--------------|---------------|--------|-------|
| May 6, 2024 | 9:00-9:25 AM | [Dropdown] | | | Available | |
| May 6, 2024 | 9:30-9:55 AM | [Dropdown] | | | Available | |
| May 6, 2024 | 10:00-10:25 AM | [Dropdown] | | | Available | |
| May 6, 2024 | 10:30-10:55 AM | [Dropdown] | | | Available | |
| ... | ... | ... | ... | ... | ... | ... |

**Tips:**
- Schedule 25-minute slots with 5-minute buffer between (e.g., 9:00-9:25, 9:30-9:55)
- Leave breaks for yourself (e.g., lunch, bathroom)
- Consider your energy level (don't schedule 20 interviews in one day!)
- Typical: 4-6 interviews per day is reasonable

---

## Student Instructions (Add to Top of Sheet)

**Add this text in a merged cell above the table (Rows 1-3, spanning all columns):**

```
🎓 SQL WHITEBOARD INTERVIEW SIMULATIONS - BOOKING SHEET

HOW TO BOOK YOUR SLOT:
1. Find an "Available" timeslot that works for you
2. Select your preferred Scenario from the dropdown (Column C)
3. Enter your full name in Column D
4. Enter your CEU email in Column E
5. Change Status (Column F) to "Booked"
6. One booking per student, please!

CANCELLATION POLICY:
If you can't make your slot, please update at least 24 hours in advance:
- Delete your name and email
- Change Status back to "Available"
- This lets someone else book the slot!

LOCATION: [INSTRUCTOR: Fill in room number and building]
QUESTIONS: Email RubiaE@ceu.edu

⚠️ IMPORTANT: Do NOT delete or edit other students' bookings!
```

---

## Sheet Protection (Optional but Recommended)

To prevent accidental deletions:

1. Select Columns A, B (Date and Time)
2. Right-click → Protect range
3. Set permissions: "Only you can edit"
4. This prevents students from changing dates/times, but they can still edit their info

---

## Sample Filled Sheet

Here's what a booked slot looks like:

| Date | Time | Scenario | Student Name | Student Email | Status | Notes |
|------|------|----------|--------------|---------------|--------|-------|
| May 6, 2024 | 9:00-9:25 AM | Scenario 1: E-Commerce Analytics | John Smith | smithj@student.ceu.edu | Booked | |
| May 6, 2024 | 9:30-9:55 AM | Scenario 2: SaaS Product Analytics | Maria Garcia | garciam@student.ceu.edu | Booked | |
| May 6, 2024 | 10:00-10:25 AM | [Dropdown] | | | Available | |
| May 6, 2024 | 10:30-10:55 AM | Scenario 3: Retail Store Operations | Alex Chen | chena@student.ceu.edu | Booked | |

---

## Monitoring and Management

### Before Each Day

1. Review the next day's bookings
2. Prepare materials for each scenario
3. Load sample data on your laptop
4. Print/open interviewer guides

### After Each Interview

1. Update Status from "Booked" to "Completed"
2. Add brief notes if needed (e.g., "Great job!" or "Needs JOIN review")
3. This helps you track progress

### Handling No-Shows

If a student doesn't show up:
1. Wait 5 minutes
2. Mark Status as "Canceled"
3. Add note: "No-show [date]"
4. Email student to check in

---

## Example Schedule Template

**Copy-paste this into your sheet and modify dates/times:**

```
May 6, 2024	9:00-9:25 AM	[Dropdown]			Available
May 6, 2024	9:30-9:55 AM	[Dropdown]			Available
May 6, 2024	10:00-10:25 AM	[Dropdown]			Available
May 6, 2024	10:30-10:55 AM	[Dropdown]			Available
May 6, 2024	11:00-11:25 AM	[Dropdown]			Available
May 6, 2024	11:30-11:55 AM	[Dropdown]			Available
May 6, 2024	1:00-1:25 PM	[Dropdown]			Available
May 6, 2024	1:30-1:55 PM	[Dropdown]			Available
May 6, 2024	2:00-2:25 PM	[Dropdown]			Available
May 6, 2024	2:30-2:55 PM	[Dropdown]			Available
May 6, 2024	3:00-3:25 PM	[Dropdown]			Available
May 6, 2024	3:30-3:55 PM	[Dropdown]			Available

May 7, 2024	9:00-9:25 AM	[Dropdown]			Available
May 7, 2024	9:30-9:55 AM	[Dropdown]			Available
...
```

**Scheduling Tips:**
- **Morning slots** (9-12): Students are fresh, perform better
- **Lunch break** (12-1): Essential for you!
- **Afternoon slots** (1-4): Good, but students may be tired
- **Late afternoon** (4+): Avoid if possible (low energy)

---

## Troubleshooting

### Problem: Students are overbooking

**Solution:** Add data validation to Column D (Student Name):
- Custom formula: `=COUNTIF(D:D, D2) <= 1`
- This prevents duplicate names

### Problem: Students are editing others' bookings

**Solution:**
1. Make a copy of the sheet at the end of each day as backup
2. Use Version History (File → Version History) to restore if needed
3. Send a reminder email about not editing others' slots

### Problem: All slots are booked, more students want to participate

**Solution:**
1. Add more dates if your schedule allows
2. Or: Create a "Waitlist" tab in the same sheet
3. Or: Offer a second round after all initial bookings are complete

---

## Analytics (Optional)

You can track some interesting metrics:

1. **Scenario popularity:**
   ```
   =COUNTIF(C:C, "Scenario 1: E-Commerce Analytics")
   ```

2. **Completion rate:**
   ```
   =COUNTIF(F:F, "Completed") / COUNTIF(F:F, "Booked")
   ```

3. **No-show rate:**
   ```
   =COUNTIF(F:F, "Canceled") / (COUNTIF(F:F, "Booked") + COUNTIF(F:F, "Canceled"))
   ```

---

## Final Checklist

Before sharing the sheet with students:

- [ ] Header row is formatted and frozen
- [ ] Dropdowns work for Scenario and Status columns
- [ ] All timeslots are listed with "Available" status
- [ ] Instructions are clear at the top of the sheet
- [ ] Sharing is set to "Anyone with link can edit" (or domain-restricted edit)
- [ ] Date and Time columns are protected (optional)
- [ ] Link is tested (open in incognito to verify students can access)
- [ ] Link is added to student announcement

---

## Share the Link!

Once your sheet is ready:

1. Copy the shareable link
2. Add it to `STUDENT_ANNOUNCEMENT.md` where it says **[INSTRUCTOR: Insert link]**
3. Post the link in Moodle, Slack, or your course communication platform
4. Monitor bookings and adjust as needed!

---

**Good luck with the simulations!** 🎯
