start_number = 1111111 
end_number = 5555555

for i in range(start_number, end_number + 1):
    print(i)
    file =open('password.txt',"a")
    file.writelines(str(i))
    file.writelines('\n')
    file.close()
