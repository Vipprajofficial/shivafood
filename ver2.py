#import streamlit as st
import sqlite3
import streamlit as st
global sff

conn=sqlite3.connect("database11.db")
conn.execute("PRAGMA foreign_keys = 1")
cur=conn.cursor()

def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS company_info 
            (c_name NVARCHAR(50) NOT NULL PRIMARY KEY ,
             c_add NVARCHAR(50) NOT NULL,
             c_gst NVARCHAR(50) NOT NULL UNIQUE)''')
            
    cur.execute('''CREATE TABLE IF NOT EXISTS machinetable
            ( 
             machine NVARCHAR(50) NOT NULL PRIMARY KEY)''')
            
    cur.execute('''CREATE TABLE IF NOT EXISTS machineinfotable
            ( 
             mch_name NVARCHAR(50) NOT NULL ,
             c_name NVARCHAR(50) NOT NULL, 
             FOREIGN KEY (c_name) REFERENCES company_info(c_name),
             FOREIGN KEY (mch_name) REFERENCES machinetable(machine))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS machine_estimate
                ( 
                 po_no NVARCHAR(50) NOT NULL PRIMARY KEY,
                 cname NVARCHAR(50) NOT NULL ,
                 machine_name NVARCHAR(50) NOT NULL  ,
                 m_cost REAL NOT NULL,
                 m_quantity INTEGER NOT NULL,
                 FOREIGN KEY (cname) REFERENCES company_info(c_name),
                 FOREIGN KEY (machine_name) REFERENCES machinetable(machine)
                 )''')
                # FOREIGN KEY (cname) REFERENCES company_info(c_name),
                # FOREIGN KEY (machine_name) REFERENCES machinetable(mch_name)


    cur.execute('''CREATE TABLE IF NOT EXISTS collection
            (
             po_no NVARCHAR(50) NOT NULL,
             company_name NVARCHAR(50) NOT NULL,
             machine_name1 NVARCHAR(50) NOT NULL ,
             datetime1 TEXT NOT NULL,
             customer_name NVARCHAR(50) NOT NULL,
             mobile_number INTEGER(10) NOT NULL,
             transaction_type NVARCHAR(50) NOT NULL,
             transaction_id NVARCHAR(50) NOT NULL, 
             machine_cost NVARCHAR(50) NOT NULL,
             FOREIGN KEY (company_name) REFERENCES company_info(c_name),
             FOREIGN KEY (machine_name1) REFERENCES machinetable(machine)
             )''')
            
    cur.execute('''CREATE TABLE IF NOT EXISTS vendor_info 
            (
             v_name NVARCHAR(50) NOT NULL PRIMARY KEY ,
             v_add NVARCHAR(50) NOT NULL,
             gstno NVARCHAR(50) NOT NULL UNIQUE) ''')     
            
    cur.execute('''CREATE TABLE IF NOT EXISTS materialinfo 
            (vid INTEGER PRIMARY KEY AUTOINCREMENT,
             v_name NVARCHAR(50) NOT NULL ,
             co_name NVARCHAR(50) NOT NULL,
             mname NVARCHAR(50) NOT NULL,
             mat_name NVARCHAR(50) NOT NULL,
             cost REAL NOT NULL,
             m_quantity REAL NOT NULL,
             m_gst REAL NOT NULL,
             m_total REAL NOT NULL,
             FOREIGN KEY (v_name) REFERENCES vendor_info(v_name)) ''')
    
    conn.commit()
def add_company(name,add,gst):
    try:
        cur.execute('''INSERT INTO company_info VALUES(?,?,?)''',( name,add, gst))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Company Already Exist")
                return 0
def show_company():
    
    m=cur.execute('''SELECT *FROM company_info''')
    st.table(m.fetchall())

def add_machine(mn):
    try:
        cur.execute('''INSERT INTO machinetable VALUES(?)''',(mn))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Machine Already Exist")
                return 0
def show_machinetable():
    
    m=cur.execute('''SELECT *FROM machinetable''')
    st.table(m.fetchall())
def add_machineinfo(mname,cname):
    try:
        cur.execute('''INSERT INTO machineinfotable VALUES(?,?)''',(mname,cname))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Machine Already Exist")
                return 0
def show_machineinfo():
    
    m=cur.execute('''SELECT *FROM machineinfotable''')
    st.table(m.fetchall())
    
def add_machine_estimate(po,cname,mname,mcost,mquantity):
    try:
        
        cur.execute('''INSERT INTO machine_estimate VALUES(?,?,?,?,?)''',(po,cname,mname,mcost,mquantity))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Machine Already Exist")
                return 0
            

def show_machine():
        m1=cur.execute('''SELECT *FROM machine_estimate''')
        st.table(m1.fetchall())
        
def add_collection(po,cm_name, mc_name,cusname,mobile,trans_type,trans_id,amount):
    
        d1=cur.execute("SELECT datetime('now','localtime')")
        d2=d1.fetchall()
        date1=d2[0][0]
        cur.execute('''INSERT INTO collection(po_no,company_name,machine_name1,datetime1,customer_name,mobile_number,transaction_type ,transaction_id, machine_cost) VALUES(?,?,?,?,?,?,?,?,?)''', (po,cm_name, mc_name,date1,cusname,mobile,trans_type,trans_id,amount))
        conn.commit()
    
def show_machine_collection():
    m1 = cur.execute('''SELECT *FROM collection''')
    st.table(m1.fetchall())
    
def add_vendor(vname,address,gstno):
    try:
        cur.execute('''INSERT INTO vendor_info VALUES(?,?,?)''',( vname,address,gstno))
        conn.commit()
        
    except sqlite3.IntegrityError:
                st.info("Vendor Already Exist")
                return 0
def show_vendor():
    
    m=cur.execute('''SELECT *FROM vendor_info''')
    st.table(m.fetchall())
    
def add_material(vendorname,co_name,machinename,materialname,mcost,qn,mgst,mtotal) :
    try:
        
        cur.execute('''INSERT INTO materialinfo(v_name,co_name,mname,mat_name,cost,m_quantity,m_gst,m_total) VALUES(?,?,?,?,?,?,?,?)''',(vendorname,co_name,machinename,materialname,mcost,qn,mgst,mtotal))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Material Already Exist")
                return 0

def show_material():
    
    m=cur.execute('''SELECT *FROM materialinfo''')
    st.table(m.fetchall())





def company_info_entry():
    m2=cur.execute("SELECT c_name FROM  company_info")
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
# st.write(pairs)

def machine_entry():
    m2=cur.execute("SELECT machine FROM  machinetable")
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def machineinfotable_entry(name1):
    m2=cur.execute('SELECT mch_name FROM  machineinfotable WHERE c_name="{}"'.format(name1))
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def machineinfotable_entry_comp():
    m2=cur.execute('SELECT c_name FROM  machineinfotable')
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def machine_estimate_entry():
    m2=cur.execute('SELECT cname FROM  machine_estimate')
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def machine_estimate_entry2(com_name):
    m2=cur.execute('SELECT machine_name FROM  machine_estimate WHERE cname="{}"'.format(com_name))
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def vendor_info_entry():
    m2=cur.execute("SELECT v_name FROM  vendor_info")
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def collection_comp_entry():
    m2=cur.execute('SELECT company_name FROM  collection')
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def collection_entry(com_name):
    m2=cur.execute('SELECT machine_name1 FROM  collection WHERE company_name="{}"'.format(com_name))
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def select_po(cname1):
     m2=cur.execute('SELECT po_no FROM  machine_estimate WHERE cname="{}"'.format(cname1))
# data=m2.fetchall()
# st.write(data)
     pairs = [x[0] for x in m2.fetchall()]
     return pairs
def select_po_machine(po):
     m2=cur.execute('SELECT machine_name FROM  machine_estimate WHERE po_no="{}"'.format(po))
# data=m2.fetchall()
# st.write(data)
     pairs = [x[0] for x in m2.fetchall()]
     return pairs
def search_by_cname(cnm):
    try:
        cur.execute('SELECT * FROM company_info WHERE c_name="{}"'.format(cnm))
        data = cur.fetchall()
        return data
    except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
    
def search_by_mcname(mcn):
    try:
        cur.execute('SELECT * FROM machineinfotable WHERE c_name="{}"'.format(mcn))
        data = cur.fetchall()
        return data
    except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
   
def total(cost1,quantity1,gst1):
    base_cost=float(cost1)*float(quantity1)
    gst_cost= float(base_cost)*(float(gst1)/100)
    
    total1=float(base_cost) + float(gst_cost)
    return float(total1)

def Bills():
     try:
        cur.execute('SELECT * FROM materialinfo')
        data = cur.fetchall()
        cur.execute('SELECT SUM(m_total) FROM materialinfo')
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def machinebill():
     try:
        cur.execute('SELECT * FROM machine_estimate')
        data = cur.fetchall()
        cur.execute('SELECT SUM(m_cost) FROM machine_estimate')
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def machinebill_by_company():
     try:
        cur.execute('SELECT * FROM machine_estimate')
        data = cur.fetchall()
        cur.execute('SELECT SUM(m_cost) FROM machine_estimate')
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def machinebill_by_installments():
     try:
        cur.execute('SELECT * FROM collection')
        data = cur.fetchall()
        cur.execute('SELECT SUM(machine_cost) FROM collection')
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def profit_loss(cname2):
    try:
        cur.execute('SELECT SUM(m_cost) FROM machine_estimate WHERE cname="{}"'.format(cname2))
        data = cur.fetchall()
        cur.execute('SELECT SUM(m_total) FROM materialinfo WHERE co_name="{}"'.format(cname2))
        data1 = cur.fetchall()
        return data,data1
    except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def outstanding_bills(cname1):
     try:
        cur.execute('SELECT SUM(m_cost) FROM machine_estimate WHERE cname="{}"'.format(cname1))
        data = cur.fetchall()
        cur.execute('SELECT SUM(machine_cost) FROM collection WHERE company_name="{}"'.format(cname1))
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def vendor_wise_bill(vname):
    
      try:
        cur.execute('SELECT * FROM materialinfo WHERE v_name="{}"'.format(vname))
        data = cur.fetchall()
        
        cur.execute('SELECT SUM(m_total) FROM materialinfo WHERE v_name="{}"'.format(vname))
        data1 = cur.fetchall()
        return data,data1
      except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
    
    
def column_wise_bill(cname):
    
      try:
        cur.execute('SELECT * FROM materialinfo WHERE co_name="{}"'.format(cname))
        data = cur.fetchall()
        
        cur.execute('SELECT SUM(m_total) FROM materialinfo WHERE co_name="{}"'.format(cname))
        data1 = cur.fetchall()
        return data,data1
      except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def by_vendor_wise():
     try:
        m2=cur.execute('SELECT v_name FROM  vendor_info')
        pairs = [x[0] for x in m2.fetchall()]
        return pairs
        
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0

def by_company_wise():
     try:
        m2=cur.execute('SELECT c_name FROM  company_info')
        pairs = [x[0] for x in m2.fetchall()]
        return pairs
        
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
    
def drop_tables():
    try:
        cur.execute('''DROP TABLE machineinfotable''')
        conn.commit()
        cur.execute('''DROP TABLE companyinfo''')
        conn.commit()
        cur.execute('''DROP TABLE vendor_info''')
        conn.commit()
        cur.execute('''DROP TABLE materialinfo''')
        conn.commit()
        
    except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
# -----------------------------------------------------------------------------------------------
st.title("Management ")

create_table()
select1=["Home","COMPANY","VENDOR"]
select2=st.sidebar.selectbox("Choose",select1)
if select2=="HOME":
    st.write("WELCOME")
elif select2=="COMPANY":
    menu = ["Add Company","Add Machine","Machine and Company","Machine Estimation","Add Collection","Show Details","Search","Company Payments"]
    choice = st.sidebar.selectbox("Menu", menu)
    

    if choice == "Add Company":
        with st.form(key='Company Information'):
            col1,col2,col3 = st.columns([1,1,1])
            with col1:
                name1 = st.text_input("Enter Company Name" )
            with col2:
                add1=st.text_input("Enter Address")
            with col3:
                gst1=st.text_input("Enter GST No. ")
            submit1 = st.form_submit_button(label='Save')
        if submit1:
            s = add_company(name1, add1, gst1)
            print(s)
            if s == 0:
                st.error("Not Added")
            else:
                st.success("Successfully added")
            # name1 = st.text_input("Enter Company Name" )
    
            # print(name1)
            # add1=st.text_input("Enter Address")
            # gst1=st.text_input("Enter GST No. ")
            # b=st.button("Save")
            # if b:
            #     s = add_company(name1, add1, gst1)
            #     print(s)
            #     if s == 0:
            #         st.error("Not Added")
            #     else:
            #         st.success("Successfully added")
         
    elif choice == "Add Machine":
        mc_name = st.text_input("Enter machine Name" )
            
        submit1 = st.button(label='Submit')
        if submit1:
            s =add_machine(mc_name)
            print(s)
            if s == 0:
                st.error("Not Added")
            else:
                st.success("MACHINE Successfully added")
            
       
    elif choice == "Machine and Company":  
        with st.form(key='Machine_form'):
       
            data=company_info_entry()
            cname=st.selectbox('Select company', data)
            machine_data=machine_entry()
            mname=st.selectbox('Select machine', machine_data)
            submit2 = st.form_submit_button(label='Save')
            if submit2:
                s2=add_machineinfo(mname, cname)
                if s2==0:
                    st.error("Not Added")      
                else :
                   st.success("Successfully added")
    
    elif choice == "Machine Estimation":
    
            data1=company_info_entry()
            cname1=st.selectbox('Select company', data1)
            po = st.text_input("Purchase Order No.")
            machine_data2=machineinfotable_entry(cname1)
            mname1=st.selectbox('machine', machine_data2)
            mcost1 = st.text_input("Machine cost")
            mquan = st.text_input("Machine quantity")
            submit2 = st.button(label='Add')
            if submit2:
                s2=add_machine_estimate(po,cname1,mname1,mcost1,mquan)
                if s2==0:
                    st.error("Not Added")      
                else :
                   st.success("Successfully added")
    elif choice == "Add Collection":
    
            data = company_info_entry()
            cname3 = st.selectbox('Select company', data)
            po1=select_po(cname3)
            po2=st.selectbox("Select po",po1)
            data1 = select_po_machine(po2)
            mname3 = st.selectbox('Select machine', data1)
    
            staffname = st.text_input("Staff name")
            mobno = st.text_input("Mobile Number")
            t_type = st.text_input("Transaction Type")
            t_id= st.text_input("Transaction_id")
            t_cost = st.text_input("Total cost")
            submit2 = st.button('Save')
            if submit2:
                s2 = add_collection(po2,cname3, mname3,staffname,mobno,t_type,t_id,t_cost)
                if s2 == 0:
                    st.error("Not Added")
                else:
                    st.success("Successfully added")
    
    elif choice== "Show Details":
           show_company()
           show_machinetable()
           show_machine()
           show_machineinfo()
          
           show_machine_collection()
           show_vendor()
           show_material()
    

    elif choice=="Company Payments":
            bill1,total1=machinebill()
            st.table(bill1)
            st.write("TOTAL MACHINE COST")
            st.write(total1[0][0])
            bill2,total2=machinebill_by_installments()
            st.table(bill2)
            st.write("TOTAL PAID MACHINE COST")
            st.write(total2[0][0])
            list2=by_company_wise()
            op2=st.selectbox("Company", list2)
            if op2:
                bill3,total3=outstanding_bills(op2)
                st.write("TOTAL COST")
                st.write(bill3[0][0])
                st.write("TOTAL PAID COST")
                st.write(total3[0][0])
                st.write("OUTSTANDING")
                amount=bill3[0][0]-total3[0][0]
                st.write(amount)
                res1,res2=profit_loss(op2)
                profit=res1[0][0]-res2[0][0]
                st.write("profit")
                st.write(profit)
elif select2=="VENDOR":
    menu = ["Add Vendor","Add Material","Search","Vendor Bills"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add Vendor":
             with st.form(key='Machine_form'):
                # vdata=vendor_info_entry()
                 name3 = st.text_input('enter vendor')
                 print(name3)
                 add2=st.text_input("Enter Address")
                 gst2=st.text_input("Enter GST No. ")
        
                 submit3 = st.form_submit_button(label='Save')
                 if submit3:
                    s3 = add_vendor(name3, add2,gst2)
                    print(s3)
                    if s3 == 0:
                        st.error("Not Added")
                    else:
                        st.success("Successfully added")           
                        
    elif choice == "Add Material":
            data2=vendor_info_entry()
            vendorn=st.selectbox('Select Vendor', data2)
            data3=company_info_entry()
            coname=st.selectbox('Select company', data3)
            data4=collection_entry(coname)
            machine=st.selectbox('Select machine', data4)
            with st.form(key='Material Information1'):
                col1,col2,col3,col4 = st.columns([1,1,1,1])
                with col1:
                    
                    mname2 = st.text_input("Enter material" )
                with col2:
                    
                    cost2=st.text_input("Enter cost")
                with col3:
                    
                    quantity=st.text_input("Enter quantity")
                with col4:
                    gst2=st.text_input("Enter GST")
                    
                submit5 = st.form_submit_button(label='Add')
                amount1=total(cost2,quantity,gst2)
                amount=float(amount1)
                if submit5:
                    s4=add_material(vendorn,coname,machine,mname2,cost2,quantity,gst2,amount) 
                    if s4==0:
                        st.error("Not Added")      
                    else :
                       st.success("Successfully added")
                      

    elif choice=="Search":
                name2 = st.text_input("Enter Company Name to search" )
                searched_data1=search_by_cname(name2)
                searched_data2=search_by_mcname(name2)
                st.table(searched_data1)
                st.table(searched_data2)
        
    elif choice=="Vendor Bills":
            bill,total=Bills()
            st.table(bill)
            st.write(total[0][0])
            
            option=st.radio("SELECT OPTION",["BY VENDOR WISE","BY COMPANY WISE"])
            if option=="BY VENDOR WISE":
                list1=by_vendor_wise()
                op1=st.selectbox("VENDOR", list1)
                if op1:
                    result,amount1=vendor_wise_bill(op1)
                    st.table(result)
                    st.write("TOTAL AMOUNT ",amount1[0][0])
            elif option=="BY COMPANY WISE": 
                list2=by_company_wise()
                op2=st.selectbox("Company", list2)
                if op2:
                    result1,amount2=column_wise_bill(op2)
                    st.table(result1)
                    st.write("TOTAL AMOUNT ",amount2[0][0])
        
        
