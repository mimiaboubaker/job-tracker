from flask import Flask, request, redirect
from datetime import datetime


app = Flask(__name__)

@app.route("/", methods=["GET"])
def homepage():
    f = open("homepage.html", "r")
    page = f.read()
    f.close()

    f = open("jobdb.txt", "r")
    contents = f.read()
    lines = contents.split("\n")

    for line in lines:
        if line.strip():
            print(f"Processing line: {line}")  
            sections = line.split("|")
            id = int(sections[0])
            company_name = sections[1]
            role = sections[2]
            date_applied = sections[4]
            status = sections[3]
            
            # add to page table rows and table data for each of the lines.  
            page += f"<tr><td>{id}</td><td>{company_name}</td><td>{role}</td><td>{date_applied}</td><td>{status}</td><td><a href='/editjob/{id}''>Edit</a></td></tr>"
    page += "</tbody></table></div></body></html>"
    
    f.close()
    return page

@app.route("/addjob", methods=["POST"])
def addjob():       
    form = request.form

    role = request.form["role"]
    company_name = request.form["company_name"]
    job_status = request.form["status"]  # Note: your form calls it "status"
    date_applied = request.form["date_applied"]


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

    return redirect("/")

@app.route("/editjob/<job_id>", methods=["GET", "POST"])
def editjob(job_id):
    if request.method == "GET":
        # Find the job to edit
        f = open("jobdb.txt", "r")
        contents = f.read()
        f.close()
        lines = contents.split("\n")
        
        # Find matching job
        for line in lines:
            if line.strip():
                sections = line.split("|")
                if sections[0] == job_id:
                    current_company = sections[1]
                    current_role = sections[2]
                    current_status = sections[3]
                    current_date = sections[4]
                    break
        
        # Build edit form HTML
        page = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Edit Job</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <h1>Edit Job #{job_id}</h1>
                
                <form method="POST" action="/editjob/{job_id}">
                    <div class="mb-3">
                        <label class="form-label">Company Name</label>
                        <input type="text" class="form-control" name="company_name" value="{current_company}" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Role</label>
                        <input type="text" class="form-control" name="role" value="{current_role}" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Status</label>
                        <select class="form-control" name="status" required>
                            <option value="none" {'selected' if current_status == 'none' else ''}>None</option>
                            <option value="applied" {'selected' if current_status == 'applied' else ''}>Applied</option>
                            <option value="applied-and-followed-up" {'selected' if current_status == 'applied-and-followed-up' else ''}>Applied and followed up</option>
                            <option value="phone-screen" {'selected' if current_status == 'phone-screen' else ''}>Phone Screen</option>
                            <option value="interview" {'selected' if current_status == 'interview' else ''}>Interview</option>
                            <option value="awaiting-decision" {'selected' if current_status == 'awaiting-decision' else ''}>Awaiting Decision</option>
                            <option value="offer" {'selected' if current_status == 'offer' else ''}>Offer</option>
                            <option value="rejected" {'selected' if current_status == 'rejected' else ''}>Rejected</option>
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Date Applied</label>
                        <input type="date" class="form-control" name="date_applied" value="{current_date}" required>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Update Job</button>
                    <a href="/" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </body>
        </html>
        """
        
        return page
    
    elif request.method == "POST":
        # Get updated values from form
        company_name = request.form["company_name"]
        role = request.form["role"]
        status = request.form["status"]
        date_applied = request.form["date_applied"]
        date_updated = datetime.now().strftime("%Y-%m-%d")
        
        # Read file
        f = open("jobdb.txt", "r")
        contents = f.read()
        f.close()
        lines = contents.split("\n")
        
        # Build updated line
        updated_line = f"{job_id}|{company_name}|{role}|{status}|{date_applied}|{date_updated}"
        
        # Replace the old line with updated line
        all_lines = []
        for line in lines:
            if line.strip():
                sections = line.split("|")
                if sections[0] == job_id:
                    all_lines.append(updated_line)
                else:
                    all_lines.append(line)
        
        # Write everything back
        f = open("jobdb.txt", "w")
        for line in all_lines:
            f.write(line + "\n")
        f.close()
        
        return redirect("/")
        



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

    # Get ID to edit (AFTER showing all)
    

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

#@app.route("/view_job")

app.run(port=5000, debug=True)