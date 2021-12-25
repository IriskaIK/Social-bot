from neo4j import GraphDatabase, basic_auth
import re
class Database:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    #get request

    ###user###
    def get_user_status(self, user_id):
        #cehck if user in db
        user_id = str(user_id)
        with self.driver.session(database="neo4j") as session:
            s = session.run('''MATCH (n) where n.user_id = '%s' return n'''%(user_id))
            if bool(s.data()) == False:
                return False
            else:
                return True

    def get_user_group_id(self, user_id):
        #check group_id by user_id
        user_id = str(user_id)
        with self.driver.session(database="neo4j") as session:
            s = session.run('''MATCH (n) where n.user_id = '%s' return n'''%(user_id))
            user = s.data()
            for k, v in user[0].items():
                return v['group_id']

    def get_all_users(self, group_id):
        #return all pair users
        group_id = str(group_id)
        with self.driver.session(database="neo4j") as session:
            s = session.run('''MATCH (n:User) where n.group_id = '%s' return n'''%(group_id))
            data = s.data()
            arr = []
            for k in data:
                for i, o in k.items():
                    arr.append(o['user_id'])
                        
            return arr

    def update_value_of_relatioships(self, group_id):
            #return all pair users
            group_id = str(group_id)
            arr_of_users = self.get_all_users(group_id)
            matrix_of_users = []
            for i in range(len(arr_of_users)):
                matrix_of_users.append([])
                for k in range(len(arr_of_users)):
                    if i != k:
                        sum_value = 0
                        count_of_relate = 0
                        with self.driver.session(database="neo4j") as session:
                            s = session.run('''MATCH (u1:User {user_id: '%s'}), (u2:User{user_id: '%s'}) MATCH p1 = (u1)-[c*2..4]-(u2) return c'''%(arr_of_users[i], arr_of_users[k]))
                            for l in s:
                                for p in l:
                                    for b in p:
                                        for o,n in b.items():
                                            count_of_relate = count_of_relate + 1
                                            sum_value = sum_value + n
                        matrix_of_users[-1].append(round(sum_value/count_of_relate, 2))
                    else:
                        matrix_of_users[-1].append(0)
            
            arr_of_sum = []
            for i in matrix_of_users:
                arr_of_sum.append(sum(i))
            done = True
            dict_of_pair = {}
            while done:
                if max(arr_of_sum) == 0:
                    done = False
                else:
                    u1_index = arr_of_sum.index(max(arr_of_sum))  
                    u2_index = matrix_of_users[u1_index].index(max(matrix_of_users[u1_index]))
                    arr_of_sum[u1_index] = 0
                    arr_of_sum[u2_index] = 0
                    for i in range(len(matrix_of_users)):
                        matrix_of_users[i][u1_index] = 0
                        matrix_of_users[i][u2_index] = 0

                    dict_of_pair[arr_of_users[u1_index]] = arr_of_users[u2_index]
            arr_of_interest = []
            for k, v in dict_of_pair.items():
                arr_of_interest.append([])
                with self.driver.session(database="neo4j") as session:
                    s = session.run('''MATCH (u1:User {user_id: '%s'}), (u2:User{user_id: '%s'}) MATCH p1 = (u1)-[c*2..4]-(u2) return p1'''%(k, v))
                    data = s.data()
                    for i in data:
                        for z, d in i.items():
                            for user in d:
                                if isinstance(user, dict):
                                    if user['type'] != 'User':
                                        if user['name'] in arr_of_interest[-1]:
                                            pass
                                        else:
                                            arr_of_interest[-1].append(user['name'])
            print(arr_of_interest)


  
    
    ###group###

    def get_group_status(self, group_id):
        #check if group in db
        group_id = str(group_id)
        with self.driver.session(database="neo4j") as session:
            s = session.run('''MATCH (n) where n.group_id = '%s' return n'''%(group_id))
            if bool(s.data()) == False:
                return False
            else:
                return True

    def get_types(self, group_id):
        #get all types with whis group_id
        group_id = str(group_id)
        with self.driver.session(database="neo4j") as session:
            s = session.run('''MATCH (n:Type) where n.group_id = '%s' return n.name'''%(group_id)) 
            arr = []
            for i in s.data():
                for k, j in i.items():
                    arr.append(j)
            print(arr)
            return arr
    
    def get_category_by_type(self, group_id, type_name):
        group_id = str(group_id)
        #get category with parent eqal type_name, and where have this group_id
        with self.driver.session(database="neo4j") as session:
            s = session.run('''MATCH (n:Type {group_id : '%s', name : '%s'})--(c:Category) return c.name'''%(group_id, type_name)) 
            arr = []
            for i in s.data():
                for k, j in i.items():
                    arr.append(j)
            print(arr)
            return arr
            


    #post request

    ###group###
    def create_group(self, group_id, categories):
        group_id = str(group_id)
        #create standart nodes with this group_id
        with self.driver.session(database="neo4j") as session:
            for types, categor in categories.items():
                session.run('''MERGE(t:Type{name:"%s", group_id: '%s', type:'Type'})'''%(types, group_id))
                for i in categor:
                    session.run('''MATCH(t:Type) where t.name = "%s" and t.group_id = '%s'  MERGE(c:Category{name:"%s", group_id: '%s', type:'Category'}) MERGE(t)-[r:Own{value:5}]-(c) '''%(types, group_id, i, group_id))
    
    def delete_group(self, group_id):
        group_id = str(group_id)
        #delete all nodes with whis group_id(users, types, category)
        with self.driver.session(database="neo4j") as session:
            session.run('''MATCH (n) where n.group_id = '%s' detach delete n'''%(group_id))


    ###user###
    def add_user(self, user_id , group_id, user_name):
        #just add user
        group_id = str(group_id)
        user_id = str(user_id)
        with self.driver.session(database="neo4j") as session:
            session.run('''MERGE (n:User{name:"%s", user_id: '%s', group_id: '%s', type:'User'})'''%(user_name, user_id, group_id))

    def delete_user(self, user_id, group_id):
        #just delete user
        group_id = str(group_id)
        user_id = str(user_id)
        with self.driver.session(database="neo4j") as session:
            session.run('''MATCH (n) where n.user_id = '%s' and n.group_id = '%s' detach delete n'''%(user_id ,group_id))
    
    def add_type(self, user_id, group_id, type_name):
        #just add new type
        group_id = str(group_id)
        user_id = str(user_id)
        with self.driver.session(database="neo4j") as session:
            s = session.run('''MATCH (n:Type) where n.group_id = '%s' and n.name = '%s' return n'''%(group_id , type_name))
            if bool(s.data()) == False:
                session.run('''MATCH(u:User) where u.user_id = '%s' MERGE (n:Type{name:'%s', group_id: '%s', type:'Type'}) MERGE(u)-[r:Own{value:20}]-(n)'''%(user_id, type_name, group_id))
            else:
                session.run('''MATCH(u:User) where u.user_id = '%s' MATCH (n:Type) where n.name = '%s' and n.group_id = '%s' MERGE(u)-[r:Own{value:20}]-(n)'''%(user_id, type_name, group_id))

    def add_category(self, user_id, group_id, category_name, type_name):
        #just add new category
        group_id = str(group_id)
        user_id = str(user_id)
        with self.driver.session(database="neo4j") as session:
            s = session.run('''MATCH (c:Category) where c.group_id = '%s' and c.name = '%s' return c'''%(group_id , category_name))
            if bool(s.data()) == False:
                session.run('''MATCH(u:User) where u.user_id = '%s' MATCH(t:Type) where t.name = '%s' and t.group_id = '%s'  MERGE (c:Category{name:'%s', group_id: '%s', type:'Category'}) MERGE(u)-[r:Own{value:20}]-(c) MERGE(t)-[s:Own{value:5}]-(c)'''%(user_id, type_name, group_id, category_name, group_id))
            else:
                session.run('''MATCH(u:User) where u.user_id = '%s' MATCH (c:Category) where c.name = '%s' and c.group_id = '%s' MERGE(u)-[r:Own{value:20}]-(c)'''%(user_id, category_name, group_id)) 
    
    def remove_relationship(self, user_id, group_id, target_node_name):
        group_id = str(group_id)
        user_id = str(user_id)
        #remove relatinship between two nodes(user, interests), using group_id and target_node_name
        with self.driver.session(database="neo4j") as session:
            session.run('''MATCH (n:User{user_id:'%s', group_id:'%s'})-[r]-(t{group_id:'%s', name:'%s'}) DELETE r'''%(user_id, group_id, group_id, target_node_name))

    def create_user_relationsip(self, user_id1, user_id2, group_id):
        user_id2 = str(user_id2)
        user_id1 = str(user_id1)
        group_id = str(group_id)
        with self.driver.session(database="neo4j") as session:
            session.run('''MERGE(u1:Mate{user_id:'%s', group_id:'%s'}) MERGE(u2:Mate{user_id:'%s', group_id:'%s'}) MERGE (u1)-[r:Mates]-(u2)'''%(user_id1, group_id, user_id2, group_id))
    

    
    

                    
                                

db = Database("bolt://100.26.187.199:7687", "neo4j", "wax-leader-drops")