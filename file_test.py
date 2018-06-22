

def main():
    #file location and name
    current_dir= r"C:\Users\Public\Documents\Python Scripts"
    file_name = "\Test_CSV"
    #select file type
    extension = ".csv"
    #assigns a datae and time to file
    date_time = "here and now"
    #opens requested file
    requested_file = open(current_dir + file_name + extension, "r+")
    #read requested file content to file_content
    file_content = requested_file.read()
    #where new file will be created
    destination = r"C:\Users\Public\Documents\Python Scripts\file_destination"
    #creates new file
    new_file = open(destination + file_name + date_time + extension, "w+")
    #writes content of file_content to new_file
    new_file.write(file_content)

if __name__ == '__main__':
    main()