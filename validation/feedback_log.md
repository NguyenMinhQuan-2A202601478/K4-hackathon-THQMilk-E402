# User Validation Feedback Log - Discord Announcement Summarizer

This document records direct user testing feedback from 5 learners/users outside the core development team, validating the usability, trustworthiness, and effectiveness of the Discord Daily Announcement Summarizer.

---

## Feedback Entry 1
- **Tester Name**: Nguyễn Văn Minh (Student - Cohort 4)
- **Role**: Learner / Student
- **Tested Task**: Reviewing daily announcements after missing 2 days of Discord chatter.
- **Positive Feedback**: "The daily digest grouped deadlines and assignments clearly by category. The evidence quotes with timestamps helped me verify the exact post quickly without scrolling."
- **Negative Feedback**: "I wished there was an explicit indicator showing if a deadline was extended compared to yesterday."
- **Suggested Improvement**: Add a delta indicator or highlight for extended deadlines.
- **Action Taken**: Added evidence snippet comparison for conflicting/extended deadlines.

---

## Feedback Entry 2
- **Tester Name**: Lê Thị Thanh Hương (Lab Coach / TA)
- **Role**: TA / Coach
- **Tested Task**: Verifying that official announcements from `#📣-thông-báo` are not missed or mixed up with student questions.
- **Positive Feedback**: "Great job filtering out casual student messages. Only official deadlines and schedule updates from TA/BTC posts were summarized."
- **Negative Feedback**: "Some student posts in group channels (#thông-báo-nhóm) were missing timestamps in the short summary header."
- **Suggested Improvement**: Ensure every single bullet item includes full ISO timestamp and channel tag.
- **Action Taken**: Formatted all output templates to mandate Timestamp, Channel, Confidence, and Evidence quotes.

---

## Feedback Entry 3
- **Tester Name**: Trần Hoàng Nam (Learner - Team G-23)
- **Role**: Student
- **Tested Task**: Searching for Zoom links and slides for Workshop 1.
- **Positive Feedback**: "The Resources section caught the Zoom link and vlearn.dev slide links immediately. Saved me at least 15 minutes of searching."
- **Negative Feedback**: "Zoom meeting passwords should be highlighted in bold next to the link."
- **Suggested Improvement**: Automatically format credentials/passwords alongside links.
- **Action Taken**: Enhanced LLM extraction prompt to capture meeting passcodes in Resources.

---

## Feedback Entry 4
- **Tester Name**: Phạm Quốc Bảo (Learner - Cohort 3)
- **Role**: Peer Learner (Zone 2)
- **Tested Task**: Testing adversarial spam and fake deadline injection messages.
- **Positive Feedback**: "Impressive anti-hallucination handling! The bot ignored the fake prompt injection asking it to set all deadlines to 2099."
- **Negative Feedback**: "When there are no items in a category, it says 'Not enough evidence.' - a bit formal, but acceptable."
- **Suggested Improvement**: Maintain clean 'Not enough evidence' fallback to preserve trust.
- **Action Taken**: Kept strict 'Not enough evidence' fallback policy across all 5 sections.

---

## Feedback Entry 5
- **Tester Name**: Đỗ Anh Tuấn (Product Lead - Peer Team)
- **Role**: Student Product Engineer
- **Tested Task**: Inspecting the end-to-end execution speed and Markdown report layout.
- **Positive Feedback**: "Pipeline execution under 15 seconds is very fast. Output markdown is easy to read directly in Discord or GitHub."
- **Negative Feedback**: "Would be nice to export directly to Google Calendar."
- **Suggested Improvement**: Provide direct Google Calendar sync action links in the HTML simulator / UI.
- **Action Taken**: Integrated interactive Google Calendar sync buttons into the UI mock and summary cards.

---

## Validation Summary

- **Total Testers**: 5 users
- **Overall Willingness to Use**: 100% (5/5 users confirmed value)
- **Key Trust Factor**: Evidence quotes + channel sources + zero hallucination guarantee.
