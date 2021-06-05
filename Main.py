from Jarvis import wishMe, takeCommand, useQuery

if __name__ == "__main__":
    
    wishMe()
    flag = True
    while flag == True:
            
        query = takeCommand().lower() 
        print(query)
        # Use query to find out what to do
        flag = useQuery(query)
        