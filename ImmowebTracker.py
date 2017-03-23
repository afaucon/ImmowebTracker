debug = False
temp_dir = "c:\\Users\\adrie\\Data\\temp\\"

def print_if_debug_is_set(str):
    if debug:
        print(str)
        
        
def get_list_of_id(url):
    print_if_debug_is_set("\n--")
    print_if_debug_is_set("In get_list_of_id:")
    import urllib.request
    with urllib.request.urlopen(url) as response:
        html_doc = response.read()
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_doc, 'html.parser')

    # import time
    # filename = time.strftime("%Y%m%d-%H%M%S_orig") + ".log"
    # with open(temp_dir + filename, "wb") as myfile:
    #     myfile.write(html_doc)
    # 
    # filename = time.strftime("%Y%m%d-%H%M%S_soup2") + ".log"
    # with open(temp_dir + filename, "w", encoding='utf-8') as myfile:
    #     myfile.write(soup.prettify())
    
    result = []
    for item in soup.find_all():
        if "data-type" in item.attrs:
            if item["data-type"] == "resultgallery-resultitem":
                id = int(item["data-id"])
                result.append(id)
                print_if_debug_is_set(str(id))
                
    return result
    
    
def store_list_of_id(list_of_id, file_path):
    print_if_debug_is_set("\n--")
    print_if_debug_is_set("In store_list_of_id:")
    with open(file_path, "w") as f:
        for id in list_of_id:
            f.write(str(id) + "\n")
            print_if_debug_is_set(str(id) + " has been stored")
    
    
def load_list_of_id(file_path):
    print_if_debug_is_set("\n--")
    print_if_debug_is_set("In load_list_of_id:")
    list_of_id = []
    with open(file_path, "r") as f:
        for line in f:
            id_as_string = line
            id = int(id_as_string)
            list_of_id.append(id)
            print_if_debug_is_set(str(id) + " has been recovered")
    return list_of_id
    
    
def find_new_id_in_current_list(current_list, previous_list):
    print_if_debug_is_set("\n--")
    print_if_debug_is_set("In find_new_id_in_current_list:")
    new_list_of_id = []
    for id in current_list:
        if id not in previous_list:
            new_list_of_id.append(id)
            print_if_debug_is_set(str(id))
    return new_list_of_id


def get_new_real_estate_ad():
    print_if_debug_is_set("\n--")
    print_if_debug_is_set("In get_new_real_estate_ad:")
    
    # Step 0 : Local variable
    file_path = temp_dir + "list_of_id.txt"
    
    # Step 1 : Recovered the list of id from Immoweb
    url = 'http://www.immoweb.be/fr/recherche/maison/a-vendre/hainaut?XORDERBY1=datemodification'
    current_list_of_id = get_list_of_id(url)
    
    # Step 2 : Recovered the list of id from the stored file
    previous_list_of_id = load_list_of_id(file_path)
    
    # Step 3 : Compare to find the new house annoucements
    new_list_of_id = find_new_id_in_current_list(current_list_of_id, previous_list_of_id)
    
    # Step 4 : Store the current list of id for a future use
    store_list_of_id(current_list_of_id, file_path)
    
    # Step N : return
    return new_list_of_id
    
    
def send_to_pushbullet(new_list_of_id):
    print_if_debug_is_set("\n--")
    print_if_debug_is_set("In send_to_pushbullet:")
    from pushbullet import Pushbullet
    try:
        pb = Pushbullet('o.mjx5s4pc2ScCZFUoqcA8WH307cIdeXfB')
        print_if_debug_is_set("Adrien Faucon devices: " + str(pb.devices))
        my_smartphone = pb.get_device('LGE Nexus 5')
        
        if len(new_list_of_id) == 0:
            print_if_debug_is_set("Nothing to send")
        else:
            for id in new_list_of_id:
                url = "http://www.immoweb.be/fr/Global.Estate.cfm?IdBien=" + str(id)
                push = pb.push_note("New house!", url, device=my_smartphone)
    except Exception as e:
        print(str(e))
    
    
def full_program():
    send_to_pushbullet(get_new_real_estate_ad())
    
    
if __name__ == '__main__':
    debug = True
    
    tests = [get_list_of_id, 
             store_list_of_id,
             load_list_of_id,
             find_new_id_in_current_list,
             get_new_real_estate_ad,
             send_to_pushbullet,
             full_program]
    
    if debug == True:
        cnt = 0
        for test in tests:
            cnt = cnt + 1
            print(str(cnt) + " - " + test.__name__)
        selection = int(input("Select the test: "))-1
        
        if tests[selection] == get_list_of_id:
            url = 'http://www.immoweb.be/fr/recherche/maison/a-vendre/hainaut?XORDERBY1=datemodification'
            list_of_id = get_list_of_id(url)
        
        if tests[selection] == store_list_of_id:
            list_of_id = [6910224,6910212,6910210,6910162,6910159,6910144,6910141,6910110,6910096,6910094,6910093,6910092,6800346,6910072,6910042,6910040,6651983,6910025,6804106,6909998,6909997,6909996,6866227,6909938,6796249,6909925,6906629,6909877,6506592,6834357]
            file_path = temp_dir + "list_of_id.txt"
            store_list_of_id(list_of_id, file_path)
        
        if tests[selection] == load_list_of_id:
            file_path = temp_dir + "list_of_id.txt"
            list_of_id = load_list_of_id(file_path)
            
        if tests[selection] == find_new_id_in_current_list:
            previous_list = [6910224,6910212,6910210,6910162,6910159,6910144,6910141,6910110,6910096,6910094,6910093,6910092,6800346,6910072,6910042,6910040,6651983,6910025,6804106,6909998,6909997,6909996,6866227,6909938,6796249,6909925,6906629,6909877,6506592,6834357]
            current_list  = [6910450,6910427,6696970,6910386,6788831,6910299,6910224,6910212,6910210,6910162,6910159,6910144,6910141,6910110,6910096,6910094,6910093,6910092,6800346,6910072,6910042,6910040,6651983,6910025,6804106,6909998,6909997,6909996,6866227,6909938]
            new_list = find_new_id_in_current_list(current_list, previous_list)
            
        if tests[selection] == get_new_real_estate_ad:
            new_list_of_id = get_new_real_estate_ad()
            
        if tests[selection] == send_to_pushbullet:
            new_list_of_id = [6910450,6910427]
            send_to_pushbullet(new_list_of_id)
        
        if tests[selection] == full_program:
            full_program()
            
    else:
        full_program()