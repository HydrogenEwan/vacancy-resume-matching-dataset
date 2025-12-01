import re
import csv
import os

def parse_rankings(text, variable_name):
    # Find the list of lists using regex
    # Pattern: variable_name = [[...]]
    # We need to handle multi-line content
    pattern = f"{variable_name}\s*=\s*(\[\[.*?\]\])"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1)
        # Clean up newlines and comments
        content = re.sub(r'#.*', '', content) # Remove comments
        content = content.replace('\n', '').replace(' ', '')
        # Parse as python object
        print(f"content: {content}")
        try:
            return eval(content)
        except:
            print(f"Error parsing {variable_name}")
            return []
    return []

def main():
    input_file = '/Users/ewan/Documents/learn/NYU/yr2F/ResponsibleAI/proj/vacancy-resume-matching-dataset/annotations-for-the-first-30-vacancies.txt'
    output_file = '/Users/ewan/Documents/learn/NYU/yr2F/ResponsibleAI/proj/vacancy-resume-matching-dataset/ranking_dataset.csv'
    
    # Vacancy IDs from 5_vacancies.csv
    # Order: 1, 2, 3, 4, 5
    vacancy_ids = ['8', '37', '90', '207', '499']
    
    with open(input_file, 'r') as f:
        text = f.read()
        
    annotator_1_rankings = parse_rankings(text, 'ANNOTATOR_1_RANKINGS')
    annotator_2_rankings = parse_rankings(text, 'ANNOTATOR_2_RANKINGS')
    
    print(f"Found {len(annotator_1_rankings)} rankings for Annotator 1")
    print(f"Found {len(annotator_2_rankings)} rankings for Annotator 2")
    
    print(f"annotator_1_rankings: {annotator_1_rankings}, type {type(annotator_1_rankings)}")
    print(f"annotator_2_rankings: {annotator_2_rankings}, type {type(annotator_2_rankings)}")
    # Prepare rows
    rows = []
    header = ['ResumeID', 'VacancyID', 'Annotator1_Label', 'Annotator2_Label']
    
    # We assume Resume IDs are 1 to 30
    # Annotator 1 has 30 rankings
    # Annotator 2 has 20 rankings (Resumes 1-20)
    
    for i in range(30):
        resume_id = str(i + 1)
        # print(resume_id)
        
        # Get rankings for this resume
        r1 = annotator_1_rankings[i] if i < len(annotator_1_rankings) else None
        r2 = annotator_2_rankings[i] if i < len(annotator_2_rankings) else None
        
        for v_idx, vacancy_id in enumerate(vacancy_ids):
            # Annotator 1
            label1 = ''
            if r1:
                rank = r1[v_idx]
                label1 = '1' if rank <= 2 else '0'
            
            # Annotator 2
            label2 = ''
            if r2:
                rank = r2[v_idx]
                label2 = '1' if rank <= 2 else '0'
            
            rows.append([resume_id, vacancy_id, label1, label2])
            
    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
        
    print(f"Successfully wrote {len(rows)} rows to {output_file}")

if __name__ == "__main__":
    main()
