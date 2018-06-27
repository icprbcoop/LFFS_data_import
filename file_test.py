from urllib.request import urlopen
import datetime

def main():
    # requested_dir is only needed for pulling a file froma directory
    # file location and name
    # requested_dir= r"C:\Users\Public\Documents\Python Scripts"
    # file_name = "\Test_CSV"
    file_name ="/coop_pot_withdrawals"
    # select file type
    extension = ".csv"
    # #assigns a datae and time to file
    date_time = str((datetime.datetime.now().strftime("%Y%m%d"))) #"here and now"
    # #opens requested file
    # requested_file = open(requested_dir + file_name + extension, "r+")
    
    


    requested_file = urlopen('https://icprbcoop.org/drupal4/products/coop_pot_withdrawals.csv')

    #read requested file content to file_content
    file_content = requested_file.read()
    #where new file will be created
    destination = r"C:\Users\Public\Documents\Python Scripts\file_destination"
    #creates new file
    new_file = open(destination + file_name + date_time + extension, "wb")
    #writes content of file_content to new_file
    new_file.write(file_content)
    new_file.close()
    requested_file.close()
    

if __name__ == '__main__':
    main()