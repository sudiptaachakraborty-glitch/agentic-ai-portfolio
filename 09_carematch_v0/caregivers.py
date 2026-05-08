"""Seed data for the CareMatch v0 demo.

12 fictional caregivers with photos sourced from randomuser.me (free,
public domain stock portraits). All names, bios and rates are fictional
and illustrative only. The data is intentionally diverse along axes that
matter for senior-care matching: age band of the caregiver, languages,
clinical vs. companion specialty, and weekday/weekend availability.
"""

CAREGIVERS = [
    {
        "id": "c01",
        "name": "Maria Hernandez",
        "age": 58,
        "photo": "https://randomuser.me/api/portraits/women/65.jpg",
        "city": "Pleasanton, CA",
        "hourly_rate": 28,
        "specialty": "companion",
        "languages": ["English", "Spanish"],
        "background_checked": True,
        "years_experience": 6,
        "availability": "Weekdays 9am–5pm",
        "bio": (
            "Recently retired pre-K teacher. Raised three kids and helped care for "
            "my mother through her last years with Parkinson's. I love conversation, "
            "puzzles, gentle walks and cooking simple Mexican comfort food."
        ),
        "skills": ["meal prep", "medication reminders", "light housekeeping", "transportation"],
    },
    {
        "id": "c02",
        "name": "James Patel",
        "age": 42,
        "photo": "https://randomuser.me/api/portraits/men/32.jpg",
        "city": "Dublin, CA",
        "hourly_rate": 38,
        "specialty": "clinical",
        "languages": ["English", "Hindi", "Gujarati"],
        "background_checked": True,
        "years_experience": 14,
        "availability": "Evenings + weekends",
        "bio": (
            "Licensed CNA with 14 years in skilled-nursing facilities. Trained in "
            "fall prevention, wound care, and dementia behavior support. I keep "
            "calm under pressure and document everything cleanly for the family."
        ),
        "skills": ["CNA", "wound care", "dementia care", "transfers & mobility"],
    },
    {
        "id": "c03",
        "name": "Linda Cho",
        "age": 67,
        "photo": "https://randomuser.me/api/portraits/women/78.jpg",
        "city": "San Ramon, CA",
        "hourly_rate": 25,
        "specialty": "companion",
        "languages": ["English", "Korean"],
        "background_checked": True,
        "years_experience": 3,
        "availability": "Weekday afternoons",
        "bio": (
            "Retired from 30 years in HR. I picked up part-time companion work after "
            "my husband passed — being useful keeps me going. I love books, music "
            "from the 60s, and church-community events."
        ),
        "skills": ["companionship", "errands", "light cooking", "reading aloud"],
    },
    {
        "id": "c04",
        "name": "Devon Williams",
        "age": 29,
        "photo": "https://randomuser.me/api/portraits/men/22.jpg",
        "city": "Livermore, CA",
        "hourly_rate": 32,
        "specialty": "clinical",
        "languages": ["English"],
        "background_checked": True,
        "years_experience": 5,
        "availability": "Overnight shifts",
        "bio": (
            "EMT-B and nursing student. Strong on overnight respite shifts, "
            "post-surgery recovery, and helping families who need a few solid "
            "hours of sleep. Calm, observant, and fast on my feet."
        ),
        "skills": ["EMT", "post-surgical recovery", "overnight respite", "vitals monitoring"],
    },
    {
        "id": "c05",
        "name": "Priya Iyer",
        "age": 51,
        "photo": "https://randomuser.me/api/portraits/women/45.jpg",
        "city": "Pleasanton, CA",
        "hourly_rate": 30,
        "specialty": "companion",
        "languages": ["English", "Tamil", "Hindi"],
        "background_checked": True,
        "years_experience": 8,
        "availability": "Flexible",
        "bio": (
            "Former IT project manager, now caregiving part-time after my own mother's "
            "stroke. I'm patient with technology — happy to help with phones, video "
            "calls and online doctor portals. Vegetarian cook."
        ),
        "skills": ["tech help", "vegetarian cooking", "doctor visits", "stroke recovery support"],
    },
    {
        "id": "c06",
        "name": "Robert Nguyen",
        "age": 63,
        "photo": "https://randomuser.me/api/portraits/men/55.jpg",
        "city": "Fremont, CA",
        "hourly_rate": 26,
        "specialty": "companion",
        "languages": ["English", "Vietnamese"],
        "background_checked": True,
        "years_experience": 4,
        "availability": "Mornings",
        "bio": (
            "Retired software engineer. I'm the guy who'll happily watch old "
            "war movies with you, fix your printer, and walk to the library. "
            "Quiet, reliable, never on my phone during a shift."
        ),
        "skills": ["companionship", "tech help", "walks", "errands"],
    },
    {
        "id": "c07",
        "name": "Aisha Mohammed",
        "age": 35,
        "photo": "https://randomuser.me/api/portraits/women/68.jpg",
        "city": "Hayward, CA",
        "hourly_rate": 36,
        "specialty": "clinical",
        "languages": ["English", "Arabic", "Somali"],
        "background_checked": True,
        "years_experience": 9,
        "availability": "Daytime weekdays",
        "bio": (
            "Home Health Aide with a hospice-care background. Specialty in "
            "diabetes management and end-of-life comfort care. I am gentle with "
            "families during hard transitions and explicit about what I observe."
        ),
        "skills": ["HHA", "diabetes care", "hospice", "family communication"],
    },
    {
        "id": "c08",
        "name": "Susan Brennan",
        "age": 71,
        "photo": "https://randomuser.me/api/portraits/women/85.jpg",
        "city": "San Ramon, CA",
        "hourly_rate": 22,
        "specialty": "companion",
        "languages": ["English"],
        "background_checked": True,
        "years_experience": 2,
        "availability": "Weekends",
        "bio": (
            "Retired RN who missed being useful. I keep things light — cards, "
            "tea, the newspaper, a little singalong with show tunes. Not looking "
            "for heavy clinical work anymore but my nursing instincts never left."
        ),
        "skills": ["companionship", "medication reminders", "music & games"],
    },
    {
        "id": "c09",
        "name": "Carlos Mendoza",
        "age": 47,
        "photo": "https://randomuser.me/api/portraits/men/41.jpg",
        "city": "Tracy, CA",
        "hourly_rate": 30,
        "specialty": "clinical",
        "languages": ["English", "Spanish"],
        "background_checked": True,
        "years_experience": 11,
        "availability": "Flexible incl. weekends",
        "bio": (
            "Licensed CNA, former Army medic. I am strong enough for transfers, "
            "calm during medical emergencies, and fluent in keeping a household "
            "running when the primary family caregiver needs respite."
        ),
        "skills": ["CNA", "transfers", "respite care", "medical emergencies"],
    },
    {
        "id": "c10",
        "name": "Hannah Kim",
        "age": 26,
        "photo": "https://randomuser.me/api/portraits/women/12.jpg",
        "city": "Pleasanton, CA",
        "hourly_rate": 24,
        "specialty": "companion",
        "languages": ["English", "Korean"],
        "background_checked": True,
        "years_experience": 1,
        "availability": "After 4pm + weekends",
        "bio": (
            "Grad student in social work. I picked this up because I want to be "
            "in this field long term. Patient with hearing-loss conversations, "
            "great with K-drama recaps and Korean home cooking."
        ),
        "skills": ["companionship", "Korean cooking", "errands", "tech help"],
    },
    {
        "id": "c11",
        "name": "Michael Foster",
        "age": 55,
        "photo": "https://randomuser.me/api/portraits/men/77.jpg",
        "city": "Livermore, CA",
        "hourly_rate": 34,
        "specialty": "clinical",
        "languages": ["English"],
        "background_checked": True,
        "years_experience": 13,
        "availability": "Weekdays",
        "bio": (
            "HHA + physical-therapy assistant. Best fit for clients recovering "
            "from joint replacement or stroke. I run gentle rehab exercises and "
            "log progress so the PT and the family stay aligned."
        ),
        "skills": ["HHA", "PT exercises", "post-surgical recovery", "progress notes"],
    },
    {
        "id": "c12",
        "name": "Rosa Esposito",
        "age": 60,
        "photo": "https://randomuser.me/api/portraits/women/33.jpg",
        "city": "Dublin, CA",
        "hourly_rate": 27,
        "specialty": "companion",
        "languages": ["English", "Italian"],
        "background_checked": True,
        "years_experience": 7,
        "availability": "Mid-day weekdays",
        "bio": (
            "I cooked in restaurant kitchens for 25 years. Now I cook one excellent "
            "meal, eat it with my client, do the dishes, and take a slow walk. "
            "That's the shift. Specialty: clients with poor appetite or dysphagia-friendly meals."
        ),
        "skills": ["nutrition", "Italian cooking", "companionship", "dysphagia-aware meals"],
    },
]
