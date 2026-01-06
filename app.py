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
    page += f"<tr><td>{id}</td><td>{company_name}</td><td>{role}</td><td>{date_applied}</td><td>{status}</td><td><button>Edit</button></td></tr>"
    
    print(f"Total rows added: {len([l for l in lines if l.strip()])}")
    print(f"Page length: {len(page)}")

    page += "</tbody></table></div></body></html>"
    
    f.close()
    return page

@app.route("/addjob", methods=["POST"])
def addjob():
    print("=== ADDJOB ROUTE CALLED ===")
    print(f"Form data: {request.form}")
    
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

#@app.route("/edit_job", method=["POST"])

#@app.route("/view_job")

app.run(port=5000, debug=True)