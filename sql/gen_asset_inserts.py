import csv, re

# keep track of seen products and associated pk's
seen_products = []
seen_products_keys = []

# function for creating inserts for assets data, adds unseen products to products
def gen_assets_inserts(file_path, prod_pk, ass_pk):

    # read in assets data from file_path
    with open(file_path, 'r') as f:

        # create iterable csv reader
        reader = csv.reader(f)

        # iterate over the rows in the .csv, exclude first row since titles
        next(reader)
        for row in reader:

            # need to grab asset_tag, product/product_fk
            tag = row[0]
            product = row[1]

            # if product has not been seen before
            notInSeens = True
            for seen in seen_products:
                if product == seen:
                    notInSeens = False
            if notInSeens:

                # move to next product primary key
                prod_pk = prod_pk + 1

                # insert new products into products
                print("INSERT INTO products (product_pk, description) VALUES ("+str(prod_pk)+","+product+");")

                # add product to seen_products
                seen_products.append(product)
                seen_products_keys.append(prod_pk)
            else:
                # set product key to whatever seen product key is
                prod_pk = seen_products_keys[seen_products.index(product)]

            # create insert for this row with asset_pk, product_fk, asset_tag
            current_insert = "INSERT INTO assets (asset_pk, product_fk, asset_tag) VALUES ("+str(ass_pk)+","+str(prod_pk)+","+tag+");"

            # print current insert
            print(current_insert)

            # determine facility of asset and facility_pk
            fac_search = re.search('osnap_legacy/(.+?)_inventory.csv', file_path)
            if fac_search:
                fac = fac_search.group(1)
            fac_pk = ['DC', 'HQ', 'MB005', 'NC', 'SPNV'].index(fac)

            # print asset_at insert
            print("INSERT INTO asset_at (asset_fk, facility_fk) VALUES ("+str(ass_pk)+","+str(fac_pk)+");")

            # increment product and assets primary key for next row/insert
            ass_pk = ass_pk + 1

    # return new asset primary key, product primary key
    return (ass_pk, prod_pk)

# initialize incremental primary keys
product_pk = -1
asset_pk = 0

# ---- PRODUCTS TABLE DATA ----

# read in products table data
with open('./osnap_legacy/product_list.csv', 'r') as products_file:

    # create iterable csv reader
    reader = csv.reader(products_file)

    # iterate over the rows in the .csv, exclude first row since titles
    next(reader)
    for row in reader:

        # need to grab name, vendor, and desc
        name = row[0]
        vendor = row[4]
        desc = row[2]

        # if product has not been seen before
        notInSeens = True
        for seen in seen_products:
            if name == seen:
                notInSeens = False
        if notInSeens:

            # create next product primary key
            product_pk = product_pk + 1

            # if not "unobtainium", create inserts with columns vendor, description
            if name != "unobtainium":

                # create insert for this row with desc
                current_insert = "INSERT INTO products (product_pk, vendor, description) VALUES ("+str(product_pk)+","+vendor+","+desc+");"

            # else create insert with only column vendor
            else:

                # create insert for this row without desc
                current_insert = "INSERT INTO products (product_pk, vendor) VALUES ("+str(product_pk)+","+vendor+");"

            # add product to seen_products
            seen_products.append(name)
            seen_products_keys.append(product_pk)

            # print current insert
            print(current_insert)
            

# ---- ASSETS TABLE DATA ----
# gen assets table from *_inventory.csv files 
# add any new products to products

(asset_pk, product_pk) = gen_assets_inserts('./osnap_legacy/DC_inventory.csv', product_pk, asset_pk)
(asset_pk, product_pk) = gen_assets_inserts('./osnap_legacy/HQ_inventory.csv', product_pk, asset_pk)
(asset_pk, product_pk) = gen_assets_inserts('./osnap_legacy/MB005_inventory.csv', product_pk, asset_pk)
(asset_pk, product_pk) = gen_assets_inserts('./osnap_legacy/NC_inventory.csv', product_pk, asset_pk)
(asset_pk, product_pk) = gen_assets_inserts('./osnap_legacy/SPNV_inventory.csv', product_pk, asset_pk)

# ---- FACILITIES TABLE DATA ----
# gen facilities table inserts
print("INSERT INTO facilities (facility_pk, fcode) VALUES (0, DC);")
print("INSERT INTO facilities (facility_pk, fcode) VALUES (1, HQ);")
print("INSERT INTO facilities (facility_pk, fcode) VALUES (2, MB005);")
print("INSERT INTO facilities (facility_pk, fcode) VALUES (3, NC);")
print("INSERT INTO facilities (facility_pk, fcode) VALUES (4, SPNV);")
