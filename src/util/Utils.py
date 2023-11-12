class utils:
    
    def printTable(res):  
        # Get maximum length of each column
        max_len = {}
        for key in res[0].keys():
            max_len[key] = len(key)
            
        for dict in res:
            for key,value in dict.items():
                if len(str(value)) > max_len[key]:
                    max_len[key] = len(str(value))
                    
        # Print header
        
        print("-"*(sum(max_len.values())+3*len(max_len)))
        for key in res[0].keys():
            print(key.ljust(max_len[key]), end=" | ")
        print()
        print("-"*(sum(max_len.values())+3*len(max_len)))
                
        # Print content
        for dict in res:
            for key,value in dict.items():
                print(str(value).ljust(max_len[key]), end=" | ")
            print()
        print("-"*(sum(max_len.values())+3*len(max_len)))