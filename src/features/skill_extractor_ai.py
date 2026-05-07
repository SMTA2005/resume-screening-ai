from transformers import pipeline

class AISkillExtractor:
    def __init__(self):
        # Hugging Face ka zero-shot classification model jo bina training ke skills recognize karega
        self.classifier = pipeline("zero-shot-classification", 
                                   model="facebook/bart-large-mnli")
        self.skill_taxonomy = [
            "Python", "Java", "JavaScript", "React", "Django", "SQL", "Machine Learning",
            "Project Management", "Agile", "Scrum", "Data Analysis", "Communication",
            "Leadership", "Sales", "Marketing", "Accounting", "Recruitment"
        ]
    
    def extract(self, text):
        result = self.classifier(text, self.skill_taxonomy)
        # Sirf high confidence wali skills lo
        extracted = [skill for skill, score in zip(result['labels'], result['scores']) if score > 0.5]
        return extracted