# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #

# Version 0.07

import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
import re

def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host,
        settings.mysql_user,
        settings.mysql_passwd,
        settings.mysql_schema)

    return con

def extract_ngrams(text, num):

    # Break the text to words ignoring punctuation
    words = re.findall('\w+', text)

    # Initialize the list of strings
    result = []

    # Calculate the number of the num-word strings in the list of strings
    end = len(words)-num+1

    # Create the list of num-word strings
    for i in range(0, end):
        result = result + [(' '.join(words[i:i+num])),]
    return result

def classify_review(reviewid):

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    
    # Prepare the SQL statement to retrieve review text and business name
    sql = """
        select b.name, r.text
        from business b, reviews r
        where b.business_id = r.business_id and r.review_id = '%s'"""\
        % (reviewid)

    # print(sql)

    try:
         # Execute SQL query
        cur.execute(sql)
    except:
        # Return only the headers in case of error
        print("Exception while executing query:",sql)
        con.close()
        return [("business_name","text","result"),]

    if cur.rowcount <= 0: # The given review id wasn't found
        con.close()
        return [("business_name","text","result"),]

    # Retrieve business name and review text from the tuple
    it = iter(cur.fetchone())
    business_name = next(it)
    text = next(it)


    # Extract n-grams from the text of the review
    ngrams = [(extract_ngrams(text,1)),(extract_ngrams(text,2)),
            (extract_ngrams(text,3))]

    # Allocate a 2d truth map of the terms that has been used
    usedtermsmap = [[False]*len(ngrams[0]), [False]*len(ngrams[1]),
                    [False]*len(ngrams[2])]

    postermcnt = 0; # positive terms counter
    negtermcnt = 0; # negative terms counter

    for i in range(2,-1,-1): # For every 3, 2 1-gram
        for j in range(0,len(ngrams[i])): # For every term in the n-gram
            
            # If the term has been used already
            if usedtermsmap[i][j] == True:
                continue # continue to the next one (if exists)
            
            # Prepare the SQL statement to check if the term is positive
            sql = "select * from posterms where word = '%s'" % (ngrams[i][j])
            try:
                # Execute SQL query
                cur.execute(sql)
            except:
                # Return only the headers in case of error
                print("Exception while executing query:",sql)
                con.close()
                return [("business_name","text","result"),]
            
            if cur.rowcount > 0: #If the term is positive
                print ("Positive term:", ngrams[i][j]) # debug print
                # Mark the term and its substrings as used in the term map
                for k in range(i,-1,-1): 
                    for l in range(j,j+i-k+1):
                        usedtermsmap[k][l] = True
                postermcnt += i+1   # Increase the positive terms counter
                continue  # continue checking the next term (if exists)  
            
            # Prepare the SQL statement to check if the term is negative
            sql = "select * from negterms where word = '%s'" % (ngrams[i][j])
            try:
                # Execute SQL query
                cur.execute(sql)
            except:
                # Return only the headers in case of error
                print("Exception while executing query:",sql)
                con.close()
                return [("business_name","text","result"),]
            
            if cur.rowcount > 0: #If the term is negative
                print ("Negative term:", ngrams[i][j]) # debug print
                # Mark the term and its substrings as used in the term map
                for k in range(i,-1,-1): 
                    for l in range(j,j+i-k+1):
                        usedtermsmap[k][l] = True
                negtermcnt += i+1 # Increase the negative terms counter
      
    print("Positive term count:", postermcnt) # debug print
    print("Negative term count:", negtermcnt) # debug print

    # Disconnect from server
    con.close()

    # If the positive terms are more than the negative then the review is 
    # considered positive
    if postermcnt > negtermcnt:
        result = [(business_name,text,"positive")]
    elif postermcnt == negtermcnt:
        result = [(business_name,text,"neutral")]
    else:
        result = [(business_name,text,"negative")]
    return [("business_name","text","result"),]+result


def updatezipcode(business_id,zipcode):

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    # Prepare the update statement
    sql = "UPDATE business SET zip_code = '%s' WHERE business_id = '%s'" \
        % (zipcode, business_id)

    # debug print to console
    # print(sql)

    try:
        # Execute the update command
        cur.execute(sql)
    except:
        # Rollback in case there is any error
        print("Exception while executing query:",sql)
        con.rollback()
        con.close()
        return [("result",),("error",)]
    try:
        # Commit the changes to the database
        con.commit()
    except:
        # Rollback in case there is any error
        print("Exception while commit:",sql)
        con.rollback()
        con.close()
        return [("result",),("error",)]

    # Disconnect from server
    con.close()

    # Extract "matched row(s) count" from query result
    msg = cur._result.message
    msg = msg.decode('ASCII')
    msg = msg.split(' ')

    # If any row was matched, then the update command was successful
    if msg[2] != '0':
        return [("result",),("ok",)]
    else:
        return [("result",),("error",)]

def selectTopNbusinesses(category_id,n):

    try:
        n = int(n) # Covert n to integer
    except:
        raise TypeError('Only integer as N')

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    # Prepare SQL query (businesses in a category in descending rating order)
    sql = """
       select r.business_id, count(r.review_id) as numberOfreviews
       from reviews r, reviews_pos_neg rpn, business_category bc
       where  r.review_id = rpn.review_id and r.business_id =  bc.business_id
                and rpn.positive = true and bc.category_id = '%s'
       group by r.business_id
       order by numberOfreviews desc
       """ % (category_id)

    # debug print to console
    # print(sql)

    try:
        # Execute SQL query
        cur.execute(sql)
    except:
        # Return only the headers in case of error
        print ("Exception while executing query:",sql)
        con.close()
        return [("business_id", "numberOfreviews"),]


    # Get n first tuples of select query result
    if n <= 0 or cur.rowcount <= 0:
        # If n is less than or zero no tuples are returned
        data = []
    else:
        # Fetch the fist n tuples and convert them to a list
        data = list(cur.fetchmany(n))

    # Disconnect from server
    con.close()

    # Add headers to the the data list
    return [("business_id", "numberOfreviews"),] + data

def traceUserInfuence(userId,depth):

    # Convert depth to integer
    try:
        d = int(depth)
    except:
        raise TypeError('Only integer as depth')

    # If depth is negative no data returned
    if d <= 0:
        print ("Non positive depth was given")
        return [("user_id",),]

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    # Prepare SQL query (user_id of friends that were influenced by userID user
    # to chose business_id)
    sql = """
        select distinct r2.user_id, r2.business_id
        from reviews r1, reviews r2, friends f
        where r1.business_id = r2.business_id
        and r1.date < r2.date and r1.user_id = '%s'
        and r2.user_id = f.friend_id and f.user_id = r1.user_id """ % (userId)

    try:
        # Execute SQL query
        cur.execute(sql)
    except:
        # Return only the headers in case of error
        print ("Exception while executing query:",sql)
        con.close()
        return [("user_id",),]

    # Store influenced (user_id, business_id) tuples in a 2d list
    influserbuslist2d = [cur.fetchall()]

    
    # Using the (user_id,business_id) tuples of the previous step that were 
    # stored into the 2d list, the influenced (user_id, business_id)
    # tuples of them are found until either the requested depth is reached, 
    # or no more influenced users are found
    i = 1
    while i < d and influserbuslist2d[i-1] != []:
        influserbuslist2d.append([]) # Append an empty list to the 2d tuple list
        for ubtuple in influserbuslist2d[i-1]: # For every (user_id,business_id)
            # tuple of the previous step,
            # find the (user_id, business_id) tuples that are influenced by them
            sql = """
                select distinct r2.user_id, r2.business_id
                from reviews r1, reviews r2, friends f
                where r1.business_id = r2.business_id
                and r1.date < r2.date and r1.user_id = '%s'
                and r1.business_id = '%s'
                and r2.user_id = f.friend_id and f.user_id = r1.user_id
                """ % (ubtuple[0], ubtuple[1])
            try:
                # Execute SQL query
                cur.execute(sql)
            except:
                # Return only the headers in case of error
                print("Exception while executing query:",sql)
                con.close()
                return [("user_id",),]
            # If new influenced (user_id,business_id) tuples were found
            if cur.rowcount > 0:
                # For every influenced tuple that were found
                for influbtuple in cur.fetchall():
                    # If this tuple has not occurred previously, then add it to
                    # the list of tuples of the current step in the 2d list
                    if influbtuple not in influserbuslist2d[i]:
                        influserbuslist2d[i] += [influbtuple]
        i+=1
    
    # Disconnect from server
    con.close()
    
    # Display a message in case the user doesn't affect any user at the given
    # depth
    if influserbuslist2d[i-1] == []:
        print("User",userId,"doesn't affect any friends at depth",d,
            "try using a lower depth value")
        return [("user_id",),]
            
    
    # Flatten the 2d influenced (user_id,business_id) list, retaining only the 
    # user_id
    influserlist = []
    for l in influserbuslist2d:
        for t in l:
            influserlist += [(t[0],)]

    return [("user_id",),] + influserlist

def test_classify_review():
    con=connection()
    cur=con.cursor()
    sql = "select review_id, positive from reviews_pos_neg";
    cur.execute(sql)
    matched = 0
    for i in range(0,cur.rowcount):
        tuple = cur.fetchone()
        result = classify_review(tuple[0])
        if result[1][2] == 'positive' and tuple[1] == '1':
            matched+=1
            print("matched",matched,"from",i)
        elif result[1][2] == 'negative' and tuple[1] == '0':
            matched+=1
            print("matched",matched,"from",i)
        else:
            print("not matched:",tuple[0])
        
    print("Total matched",matched,"from",cur.rowcount)
    con.close()

# Takes a lot of time to complete
# test_classify_review()

