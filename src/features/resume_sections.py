import re

def split_sections(text):

    sections = {
        "skills":"",
        "experience":"",
        "education":"",
        "projects":""
    }

    current = None

    lines = text.lower().split("\n")

    for line in lines:

        if re.search(r"skills",line):

            current="skills"

        elif re.search(r"experience",line):

            current="experience"

        elif re.search(r"education",line):

            current="education"

        elif re.search(r"projects",line):

            current="projects"

        if current:

            sections[current]+=line+"\n"

    return sections