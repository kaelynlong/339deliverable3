import csv
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
import re

# Load Jinja2 environment and templates directory
env = Environment(loader=FileSystemLoader('templates'))

# Paths to the CSV files for all athletes
adrienne_csv = "athletes/womens_team/Adrienne Stewart21142907.csv"
alex_csv = "athletes/mens_team/Alex Nemecek18820260.csv"
amir_csv = "athletes/mens_team/Amir Abston25395576.csv"
bruno_csv = "athletes/mens_team/Bruno Cifaldi21147176.csv"
caspian_csv = "athletes/mens_team/Caspian Ruiz26460414.csv"
cole_csv = "athletes/mens_team/Cole Harms26322018.csv"
dylan_csv = "athletes/mens_team/Dylan Hanley23349680.csv"
elliot_csv = "athletes/mens_team/Elliot Daley26322015.csv"
emmett_csv = "athletes/mens_team/Emmett Strait26322025.csv"
enshu_csv = "athletes/mens_team/Enshu Kuan23687884.csv"
ethan_csv = "athletes/mens_team/Ethan Miller23349703.csv"

# Function to load and clean CSV data
def load_csv_data(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = [row for row in reader if row]  # Remove empty rows
    return data


# Extract athlete info from CSV
def extract_athlete_info(data):
    athlete_name = data[0][0] if len(data[0]) > 0 else "Unknown"
    athlete_id = data[1][0] if len(data) > 1 else "Unknown"
    athlete_link = f"https://www.athletic.net/athlete/{athlete_id}/cross-country/high-school"
    athlete_grade = next((row[2] for row in data if len(row) > 2 and row[2].isdigit()), "N/A")
    return athlete_name, athlete_id, athlete_link, athlete_grade

# Load CSV data for athletes
adrienne_data = load_csv_data(adrienne_csv)
alex_data = load_csv_data(alex_csv)
amir_data = load_csv_data(amir_csv)
bruno_data = load_csv_data(bruno_csv)
caspian_data = load_csv_data(caspian_csv)
cole_data = load_csv_data(cole_csv)
dylan_data = load_csv_data(dylan_csv)
elliot_data = load_csv_data(elliot_csv)
emmett_data = load_csv_data(emmett_csv)
enshu_data = load_csv_data(enshu_csv)
ethan_data = load_csv_data(ethan_csv)

# Extract athlete info
adrienne_name, adrienne_id, adrienne_link, adrienne_grade = extract_athlete_info(adrienne_data)
alex_name, alex_id, alex_link, alex_grade = extract_athlete_info(alex_data)
amir_name, amir_id, amir_link, amir_grade = extract_athlete_info(amir_data)
bruno_name, bruno_id, bruno_link, bruno_grade = extract_athlete_info(bruno_data)
caspian_name, caspian_id, caspian_link, caspian_grade = extract_athlete_info(caspian_data)
cole_name, cole_id, cole_link, cole_grade = extract_athlete_info(cole_data)
dylan_name, dylan_id, dylan_link, dylan_grade = extract_athlete_info(dylan_data)
elliot_name, elliot_id, elliot_link, elliot_grade = extract_athlete_info(elliot_data)
emmett_name, emmett_id, emmett_link, emmett_grade = extract_athlete_info(emmett_data)
enshu_name, enshu_id, enshu_link, enshu_grade = extract_athlete_info(enshu_data)
ethan_name, ethan_id, ethan_link, ethan_grade = extract_athlete_info(ethan_data)

# Extract season records and races based on the presence of "Meet" information
def extract_season_records_and_races(data):
    records = []
    races = []
    
    for row in data:
        if len(row) >= 6 and row[5] == '':  # If the "Meet" column (index 5) is empty, it's a season record
            record_dict = {
                "Year": row[1],
                "Grade": row[2] if row[2] != '' else "N/A",
                "Time": row[3]
            }
            records.append(record_dict)
        elif len(row) >= 6 and row[5] != '':  # If the "Meet" column is filled, it's a race
            race_dict = {
                "Place": row[1],
                "Time": row[3],
                "Date": row[4],
                "Meet": row[5],
                "Comments": row[6] if len(row) > 6 else "",
                "Photo": row[7] if len(row) > 7 else ""
            }
            races.append(race_dict)
    
    return records, races

# Filter races that are not part of the season records and exclude rows with header-like values
def filter_all_races(races, records):
    record_times = {record['Time'] for record in records}  # Get a set of times from the records

    filtered_races = [
        race for race in races
        if race["Time"] not in record_times and race["Place"] != "Name"
    ]
    return filtered_races


# Extract season records and races for each athlete
adrienne_records, adrienne_races = extract_season_records_and_races(adrienne_data)
alex_records, alex_races = extract_season_records_and_races(alex_data)
amir_records, amir_races = extract_season_records_and_races(amir_data)
bruno_records, bruno_races = extract_season_records_and_races(bruno_data)
caspian_records, caspian_races = extract_season_records_and_races(caspian_data)
cole_records, cole_races = extract_season_records_and_races(cole_data)
ethan_records, ethan_races = extract_season_records_and_races(ethan_data)
dylan_records, dylan_races = extract_season_records_and_races(dylan_data)
elliot_records, elliot_races = extract_season_records_and_races(elliot_data)
emmett_records, emmett_races = extract_season_records_and_races(emmett_data)
enshu_records, enshu_races = extract_season_records_and_races(enshu_data)

# Filter all races (remove ones that are in the season records)
adrienne_all_races = filter_all_races(adrienne_races, adrienne_records)
alex_all_races = filter_all_races(alex_races, alex_records)
amir_all_races = filter_all_races(amir_races, amir_records)
bruno_all_races = filter_all_races(bruno_races, bruno_records)
caspian_all_races = filter_all_races(caspian_races, caspian_records)
cole_all_races = filter_all_races(cole_races, cole_records)
ethan_all_races = filter_all_races(ethan_races, ethan_records)
dylan_all_races = filter_all_races(dylan_races, dylan_records)
elliot_all_races = filter_all_races(elliot_races, elliot_records)
emmett_all_races = filter_all_races(emmett_races, emmett_records)
enshu_all_races = filter_all_races(enshu_races, enshu_records)

# Generate dynamic HTML table for races without the "Photos" column
def races_table_maker(races_list):
    if not races_list:
        return "<p>No races available</p>"
    
    html_table = "<table>\n"
    
    # Treat the first row as the header
    header = races_list[0]
    html_table += "<tr>\n"
    for key in header.keys():
        if key != "Photo":  # Skip the "Photos" column
            html_table += f"<th>{key}</th>\n"  # Use <th> for the first row (header)
    html_table += "</tr>\n"
    
    # Generate table rows for the remaining data (exclude the first row)
    for race in races_list[1:]:  # Skip the first row
        html_table += "<tr>\n"
        for key, value in race.items():
            if key != "Photo":  # Skip the "Photos" column
                html_table += f"<td>{value}</td>\n"  # Use <td> for normal rows
        html_table += "</tr>\n"
    
    html_table += "</table>\n"
    return html_table


# Generate dynamic HTML table for season records
def table_maker(list_dicts):
    if not list_dicts:
        return "<p>No data available</p>"
    
    html_table = "<table>\n<tr>\n"
    for key in list_dicts[0].keys():
        html_table += f"<th>{key}</th>\n"
    html_table += "</tr>\n"
    
    for entry in list_dicts:
        html_table += "<tr>\n"
        for value in entry.values():
            html_table += f"<td>{value}</td>\n"
        html_table += "</tr>\n"
    
    html_table += "</table>\n"
    return html_table

# Generate tables for season records
adrienne_table = table_maker(adrienne_records)
alex_table = table_maker(alex_records)
amir_table = table_maker(amir_records)
bruno_table = table_maker(bruno_records)
caspian_table = table_maker(caspian_records)
cole_table = table_maker(cole_records)
ethan_table = table_maker(ethan_records)
dylan_table = table_maker(dylan_records)
elliot_table = table_maker(elliot_records)
emmett_table = table_maker(emmett_records)
enshu_table = table_maker(enshu_records)

# Generate tables for all races
adrienne_all_races_table = races_table_maker(adrienne_all_races)
alex_all_races_table = races_table_maker(alex_all_races)
amir_all_races_table = races_table_maker(amir_all_races)
bruno_all_races_table = races_table_maker(bruno_all_races)
caspian_all_races_table = races_table_maker(caspian_all_races)
cole_all_races_table = races_table_maker(cole_all_races)
ethan_all_races_table = races_table_maker(ethan_all_races)
dylan_all_races_table = races_table_maker(dylan_all_races)
elliot_all_races_table = races_table_maker(elliot_all_races)
emmett_all_races_table = races_table_maker(emmett_all_races)
enshu_all_races_table = races_table_maker(enshu_all_races)


def calculate_progress(time_str):
    # Use regex to extract only numbers and valid time separators (colon and period), ignoring any invalid characters
    cleaned_time_str = re.sub(r'[^\d:.]', '', time_str)
    print(f"Original time string: {time_str}, Cleaned time string: {cleaned_time_str}")
    
    try:
        # Check if the cleaned time is in mm:ss.s format
        if ':' in cleaned_time_str:
            minutes, seconds = map(float, cleaned_time_str.split(':'))
            total_seconds = minutes * 60 + seconds
        else:
            # Assume the time is in seconds if no colon is found
            total_seconds = float(cleaned_time_str)
        print(f"Total seconds: {total_seconds}")
    except ValueError:
        print(f"Error parsing time: {time_str}")
        total_seconds = float('inf')  # Treat as invalid time, set to infinity for progress calculation
    
    max_time = 60 * 60  # 30 minutes in seconds
    progress = (1 - (total_seconds / max_time)) * 100
    progress = max(0, min(progress, 100))  # Ensure progress is between 0 and 100
    
    print(f"Calculated progress: {progress}%")
    return progress


# Example to calculate progress for each athlete's year and time
def generate_progress_data(records):
    progress_data = []
    for record in records:
        year = record["Year"]
        time = record["Time"]
        progress = calculate_progress(time)
        progress_data.append((year, time, progress))
    return progress_data

# Generate progress data for Adrienne's page
adrienne_progress_data = generate_progress_data(adrienne_records)
alex_progress_data = generate_progress_data(alex_records)
amir_progress_data = generate_progress_data(amir_records)
bruno_progress_data = generate_progress_data(bruno_records)
caspian_progress_data = generate_progress_data(caspian_records)
cole_progress_data = generate_progress_data(cole_records)
ethan_progress_data = generate_progress_data(ethan_records)
dylan_progress_data = generate_progress_data(dylan_records)
elliot_progress_data = generate_progress_data(elliot_records)
emmett_progress_data = generate_progress_data(emmett_records)
enshu_progress_data = generate_progress_data(enshu_records)


def render_index_page(mens_top10, womens_top10):
    index_template = env.get_template('index.html')
    index_html = index_template.render(
        mens_top10=mens_top10,
        womens_top10=womens_top10,
        page_heading="Top 10 Men’s and Women’s Cross Country Rankings"
    )
    with open("index.html", "w") as f:
        f.write(index_html)

mens_top10_data = [
    {"Rank": 1, "Name": "Bruno Cifaldi", "Time": "17:07.8"},
    {"Rank": 2, "Name": "Enshu Kuan", "Time": "17:44.4"},
    {"Rank": 3, "Name": "Dylan Hanley", "Time": "18:13.9 PR"},
    {"Rank": 4, "Name": "Elliot Daley", "Time": "19:05.6 PR"},
    {"Rank": 5, "Name": "Alex Nemecek", "Time": "19:21.4"},
    {"Rank": 6, "Name": "Emmett Strait", "Time": "19:41.3 PR"},
    {"Rank": 7, "Name": "Ethan Miller", "Time": "21:25.1 PR"},
    {"Rank": 8, "Name": "Cole Harms", "Time": "24:34.5 PR"},
    {"Rank": 9, "Name": "Amir Abston", "Time": "25:25.0 PR"},
    {"Rank": 10, "Name": "Caspian Ruiz", "Time": "25:52.7 PR"},
]

womens_top10_data = [
    {"Rank": 1, "Name": "Adrienne Stewart", "Time": "23:31.1"},
]

render_index_page(mens_top10_data, womens_top10_data)
print("index.html has been generated.")

# Render and save athlete pages
athlete_template = env.get_template('athlete.html')

# Adrienne Stewart's page
athlete_html_adrienne = athlete_template.render(
    athlete_name=adrienne_name,
    athlete_grade=adrienne_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=adrienne_all_races_table,  # Passing the all races table
    all_records_table=adrienne_table,
    progress_data=adrienne_progress_data,  
    season_notes="<li>2024: Best season performance</li>"
)
with open("athlete-adrienne-stewart.html", "w") as f:
    f.write(athlete_html_adrienne)

# Alex Nemecek's page
athlete_html_alex = athlete_template.render(
    athlete_name=alex_name,
    athlete_grade=alex_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=alex_all_races_table,  # Passing the all races table
    all_records_table=alex_table,
    progress_data=alex_progress_data, 
    season_notes="<li>2024: You were flying today! Keep up that momentum!</li>"
)
with open("athlete-alex-nemecek.html", "w") as f:
    f.write(athlete_html_alex)

# Amir Abston's page
athlete_html_amir = athlete_template.render(
    athlete_name=amir_name,
    athlete_grade=amir_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=amir_all_races_table,  # Passing the all races table
    all_records_table=amir_table,
    progress_data=amir_progress_data, 
    season_notes="<li>2024: Way to stay focused during the race! Keep that mindset for the next one.</li>"
)
with open("athlete-amir-abston.html", "w") as f:
    f.write(athlete_html_amir)

# Bruno Cifaldi's page
athlete_html_bruno = athlete_template.render(
    athlete_name=bruno_name,
    athlete_grade=bruno_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=bruno_all_races_table,  # Passing the all races table
    all_records_table=bruno_table,
    progress_data=bruno_progress_data, 
    season_notes="<li>2024: Your pacing was solid today. Let's focus on maintaining it throughout the race.</li>"
)
with open("athlete-bruno-cifaldi.html", "w") as f:
    f.write(athlete_html_bruno)

# Caspian Ruiz's page
athlete_html_caspian = athlete_template.render(
    athlete_name=caspian_name,
    athlete_grade=caspian_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=caspian_all_races_table,  # Passing the all races table
    all_records_table=caspian_table,
    progress_data=caspian_progress_data, 
    season_notes="<li>2024: You really pushed hard in that final mile, awesome finish!</li>"
)
with open("athlete-caspian-ruiz.html", "w") as f:
    f.write(athlete_html_caspian)

# Cole Harms's page
athlete_html_cole = athlete_template.render(
    athlete_name=cole_name,
    athlete_grade=cole_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=cole_all_races_table,  # Passing the all races table
    all_records_table=cole_table,
    progress_data=cole_progress_data, 
    season_notes="<li>2024: Awesome race! Let's look at where we can shave off a few more seconds.</li>"
)
with open("athlete-cole-harms.html", "w") as f:
    f.write(athlete_html_cole)

# Ethan Miller's page
athlete_html_ethan = athlete_template.render(
    athlete_name=ethan_name,
    athlete_grade=ethan_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=ethan_all_races_table,  # Passing the all races table
    all_records_table=ethan_table,
    progress_data=ethan_progress_data, 
    season_notes="<li>2024: I blinked and missed the first half of your race! That was quick!</li>"
)
with open("athlete-ethan-miller.html", "w") as f:
    f.write(athlete_html_ethan)

# Dylan Hanley's page
athlete_html_dylan = athlete_template.render(
    athlete_name=dylan_name,
    athlete_grade=dylan_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=dylan_all_races_table,  # Passing the all races table
    all_records_table=dylan_table,
    progress_data=dylan_progress_data, 
    season_notes="<li>2024: Super strong start! We'll work on keeping that energy the whole race.</li>"
)
with open("athlete-dylan-hanley.html", "w") as f:
    f.write(athlete_html_dylan)

# Elliot Daley's page
athlete_html_elliot = athlete_template.render(
    athlete_name=elliot_name,
    athlete_grade=elliot_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=elliot_all_races_table,  # Passing the all races table
    all_records_table=elliot_table,
    progress_data=elliot_progress_data, 
    season_notes="<li>2024: Awesome race! Let's look at where we can shave off a few more seconds.</li>"
)
with open("athlete-elliot-daley.html", "w") as f:
    f.write(athlete_html_elliot)

# Emmett Strait's page
athlete_html_emmett = athlete_template.render(
    athlete_name=emmett_name,
    athlete_grade=emmett_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table= emmett_all_races_table,  # Passing the all races table
    all_records_table=emmett_table,
    progress_data=emmett_progress_data, 
    season_notes="<li>2024: I blinked and missed the first half of your race! That was quick!</li>"
)
with open("athlete-emmett-strait.html", "w") as f:
    f.write(athlete_html_emmett)

# Enshu Kuan's page
athlete_html_enshu = athlete_template.render(
    athlete_name=enshu_name,
    athlete_grade=enshu_grade,
    athlete_school="Ann Arbor Skyline",
    season_year="2024",
    all_races_table=enshu_all_races_table,  # Passing the all races table
    all_records_table=enshu_table,
    progress_data=enshu_progress_data, 
    season_notes="<li>2024: Nice work! By the way, you know this is a race, not a scenic tour, right?</li>"
)
with open("athlete-enshu-kuan.html", "w") as f:
    f.write(athlete_html_enshu)

# Confirm completion
print('HTML pages generated for all athletes')
