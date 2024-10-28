# Folder structure that has already been created
theme_folder_structure = {
    "Physical Health": {
        "Pain and discomfort": {},
        "Energy and fatigue": {},
        "Sleep and rest": {}
    },
    "Psychological Health": {
        "Positive feelings": {},
        "Thinking, learning, memory, and concentration": {
            "Speed": {},
            "Clarity": {}
        },
        "Self-esteem": {},
        "Body image and appearance": {},
        "Negative feelings": {}
    },
    "Level of Independence": {
        "Mobility": {},
        "Activities of daily living": {
            "Taking care of oneself": {},
            "Managing one's belongings appropriately": {}
        },
        "Dependence on medication and medical aids": {},
        "Work capacity - education and skills": {}
    },
    "Civic Engagement and Governance": {},
    "Subjective Well-being": {},
    "Work-Life Balance": {},
    "Environment": {
        "Comfort and security": {},
        "Domestic environment": {
            "Crowding": {},
            "Available space": {},
            "Cleanliness": {},
            "Opportunities for privacy": {},
            "Available equipment": {},
            "Building construction quality": {}
        },
        "Financial resources": {
            "Independence": {},
            "Feeling of having enough": {}
        },
        "Health care and social care": {
            "Accessibility": {},
            "Quality": {}
        },
        "Opportunities to acquire new information and skills": {},
        "Participation in recreational activities and leisure opportunities": {},
        "Physical environment": {
            "Pollution": {},
            "Noise": {},
            "Traffic": {},
            "Climate": {}
        },
        "Infrastructure": {
            "Transport": {},
            "Drinking water": {},
            "Gas": {},
            "Electricity": {},
            "Sewage networks": {}
        },
        "Urbanisation level": {}
    },
    "Social Relationships": {
        "Personal relations": {},
        "Social support": {},
        "Sexual activity": {}
    },
    "Spirituality/Religion/Personal Beliefs": {}
}


# Define hierarchies
hS_F = [
    [(0, 'COUNTRY'), (1, 'REGION'), (2, 'DEPARTEMENT'), (3, 'ARRONDISSEMENT'), (4, 'CANTON'), (5, 'COMMUNE'),
     (6, 'GEOPOINT')],
    [(0, 'COUNTRY'), (1, 'EPCI'), (5, 'COMMUNE'), (6, 'GEOPOINT')]
]

hT_F = [
    [(0, 'YEAR'), (1, 'QUARTER'), (2, 'MONTH'), (3, 'DATE')],
    [(0, 'YEAR'), (1, 'WEEK'), (3, 'DATE')]
]

