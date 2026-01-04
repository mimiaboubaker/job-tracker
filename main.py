from datetime import datetime



print("Job Tracker")
print("---")

action = input("1. Add Job \n2. View Jobs \n3. Edit Job")

def addjob():
    role = input("Job Title: ")
    company_name = input("Company Name: ")
    job_status = input("""Job Status. Enter a number:
                    1. none,
                    \n2. applied
                    \n3. applied and followed up
                    \n4. phone screen
                    \n5. interview, 
                    \n6. awaiting decision
                    \n7. offer
                    \n8. rejection""")
    date_applied = input("Date Applied (DD-MM-YYYY): ")


    if job_status == "1":
        job_status = "none"
    elif job_status == "2":
        job_status = "applied"
    elif job_status == "3":
        job_status = "applied and followed up"
    elif job_status == "4":
        job_status = "phone screen"
    elif job_status == "5":
        job_status = "interview"        
    elif job_status == "6":
        job_status = "awaiting decision"        
    elif job_status == "7":
        job_status = "offer"
    elif job_status == "8":
        job_status = "rejection"

    f = open("jobdb.txt", "r")
    contents = f.read()
    lines = contents.split("\n")

# for line in file, split on delimiter, 
# take first part and make it an integer and save it as ID
# then add to list, take max of list, add one to get new job ID 
# if ids exists, then max + 1; else 1

    ids = []
    for line in lines:
        if line.strip():

            sections = line.split("|")
            id = int(sections[0])
            ids.append(id)

        if ids:
            max_id = max(ids)
            new_job_id = max_id+1
        else:
            new_job_id = 1
            
        date_updated = datetime.now().strftime("%Y-%m-%d")
        f.close()
        
        f = open("jobdb.txt", "a")
        f.write(f"{new_job_id}|{company_name}|{role}|{job_status}|{date_applied}|{date_updated}\n")
        f.close()


def viewjob():
    f = open("jobdb.txt", "r")
    contents = f.read()
    lines = contents.split("\n")

    for line in lines:
        if line.strip():

            sections = line.split("|")
            id = int(sections[0])
            company_name = sections[1]
            role = sections[2]
            date_applied = sections[4]
            print(f"{id} | {company_name} | {role} | {date_applied}")
    f.close()


def editjob():
f = open("jobdb.txt", "r")
contents = f.read()
lines = contents.split("\n")
f.close()

# Loop 1: Show all jobs
for line in lines:
    if line.strip():
        sections = line.split("|")
        id = sections[0]
        company_name = sections[1]
        role = sections[2]
        date_applied = sections[4]
        print(f"{id} | {company_name} | {role} | {date_applied}")

# Get ID to edit (AFTER showing all)
changing_id = input("Which id do you want to change? ")

# Loop 2: Find the matching job
for line in lines:
    if line.strip():
        sections = line.split("|")
        if sections[0] == changing_id:
            break

# Show and edit (OUTSIDE loops)
print(f"Editing job: {sections[1]} | {sections[2]} | {sections[4]}")

changed_field = input("What field do you want to edit? 1. Company Name, 2. Role, 3. Date Applied: ")

if changed_field == "1":
    new_value = input("Enter new company name: ")
    sections[1] = new_value
elif changed_field == "2":
    new_value = input("Enter new role: ")
    sections[2] = new_value
elif changed_field == "3":
    new_value = input("Enter new date applied: ")
    sections[4] = new_value

sections[5] = datetime.now().strftime("%Y-%m-%d")
updated_line = "|".join(sections)

# Save changes
all_lines = []
for line in lines:
    if line.strip():
        parts = line.split("|")
        if parts[0] == changing_id:
            all_lines.append(updated_line)
        else:
            all_lines.append(line)

f = open("jobdb.txt", "w")
for line in all_lines:
    f.write(line + "\n")
f.close()

print("Job updated successfully!")  

while True: 
    if action == "1":
        addjob()
            
    elif action == "2":
        viewjob()


    elif action == "3":
        editjob()

    else:
        print("ERROR: Invalid Entry. Please choose from one of the options.")



