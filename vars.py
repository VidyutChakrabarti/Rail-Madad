departments = {
    'Engineering': "Responsible for the construction and maintenance of railway tracks, bridges, and buildings.",
    'Mechanical': "Manages the maintenance and operation of locomotives, coaches, and wagons.",
    'Electrical': "Handles the electrification of railway lines and the maintenance of electrical equipment.",
    'Traffic': "Oversees the operation of trains, including scheduling and control.",
    'Commercial': "Manages passenger services, ticketing, and freight operations.",
    'Personnel': "Deals with human resources, including recruitment, training, and employee welfare.",
    'Finance': "Responsible for budgeting, accounting, and financial management.",
    'Signal and Telecommunication': "Maintains signaling systems and communication networks.",
    'Stores': "Manages the procurement and distribution of materials and supplies.",
    'Safety': "Ensures the safety of railway operations and implements safety protocols.",
    'Security': "The Railway Protection Force (RPF) is responsible for the security of railway property and passengers.",
    'Medical': "Provides healthcare services to railway employees and their families.",
    'Legal': "Handles legal matters and litigation involving Indian Railways.",
    'Public Relations': "Manages communication with the public and media."
}

scheduling_schema = {}

urgency_eval = {}

issue_department_mapping = {
    # Mechanical Department Issues
    "AC": "Mechanical",
    "air conditioning": "Mechanical",
    "AC malfunction": "Mechanical",
    "AC not working": "Mechanical",
    "broken seats": "Mechanical",
    "seat damage": "Mechanical",
    "door malfunction": "Mechanical",
    "coach maintenance": "Mechanical",
    
    # Commercial Department Issues  
    "staff behavior": "Commercial",
    "staff rude": "Commercial",
    "ticketing": "Commercial",
    "refund": "Commercial",
    "food quality": "Commercial",
    "catering": "Commercial",
    
    # Electrical Department Issues
    "lights": "Electrical",
    "lighting": "Electrical",
    "power supply": "Electrical",
    "fan": "Electrical",
    
    # Safety Department Issues
    "safety": "Safety",
    "accident": "Safety",
    "emergency": "Safety",
    
    # Security Department Issues
    "theft": "Security",
    "harassment": "Security",
    
    # Engineering Department Issues
    "track": "Engineering",
    "platform": "Engineering",
    "station": "Engineering",
    
    # Medical Department Issues
    "medical": "Medical",
    "health": "Medical",
    
    # Signal and Telecommunication Issues
    "signal": "Signal and Telecommunication",
    "announcement": "Signal and Telecommunication",
    
    # Traffic Department Issues
    "delay": "Traffic",
    "late": "Traffic",
    "cancellation": "Traffic",
}
