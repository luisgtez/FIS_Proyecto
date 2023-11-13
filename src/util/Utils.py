class utils:
    
    def printTable(res):
        # Get maximum length of each column
        max_len = {}
        for key in res[0].keys():
            max_len[key] = len(key)

        for dict in res:
            for key, value in dict.items():
                if len(str(value)) > max_len[key]:
                    max_len[key] = len(str(value))
        # Print top row of table
        print("+" + "-" * (sum(max_len.values()) + 2 * len(max_len)) + "+")
        # Print header
        print("|", end=" ")
        for key in res[0].keys():
            print(key.ljust(max_len[key]), end=" |")
        print()
        print("|" + "-" * (sum(max_len.values()) + 2 * len(max_len) ) + "|")


        # Print content
        for i, dict in enumerate(res):
            print("|", end=" ")
            for key, value in dict.items():
                print(str(value).ljust(max_len[key]), end=" |")
            print()

            # Print line of -- and | between rows
            if i < len(res) - 1:
                print("|" + "-" * (sum(max_len.values()) + 2 * len(max_len)) + "|")


        print("+" + "-" * (sum(max_len.values()) + 2 * len(max_len)) + "+")

