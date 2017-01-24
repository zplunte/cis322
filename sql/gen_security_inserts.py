import csv

# ---- LEVELS TABLE DATA ----

# read in levels table data
with open('./osnap_legacy/security_levels.csv', 'r') as levels_file:

    # create iterable csv reader
    reader = csv.reader(levels_file)

    # start with primary key 0
    pk = 0

    # iterate over the rows in the .csv, exclude first row since titles
    next(reader)
    for row in reader:

        # need to grab both abbrv and desc
        abbrv = row[0]
        desc = row[1]

        # if not in *REDACTED* desc zone
        if pk < 3:
        
            # create insert for this row with desc
            current_insert = "INSERT INTO levels (level_pk, abbrv, comment) VALUES ("+str(pk)+","+abbrv+","+desc+");" 
         
            # print current insert
            print(current_insert)

        # if in *REDACTED* desc zone        
        else:
 
            # create insert for this row without desc
            current_insert = "INSERT INTO levels (level_pk, abbrv, comment) VALUES ("+str(pk)+","+abbrv+");"

        # print current insert
        print(current_insert)

        # increment primary key for next row/insert
        pk = pk + 1

# ---- COMPARTMENTS TABLE DATA ----

# read in compartments table data
with open('./osnap_legacy/security_compartments.csv', 'r') as compartments_file:

    # create iterable csv reader
    reader = csv.reader(compartments_file)

    # start with primary key 0
    pk = 0

    # iterate over the rows in the .csv, exclude first row since titles
    next(reader)
    for row in reader:

        # only need abbrv since desc is *REDACTED*
        abbrv = row[0]

        # create insert for this row
        current_insert = "INSERT INTO levels (compartment_pk, abbrv, comment) VALUES ("+str(pk)+","+abbrv+");"

        # print current insert
        print(current_insert)

        # increment primary key for next row/insert
        pk = pk + 1
