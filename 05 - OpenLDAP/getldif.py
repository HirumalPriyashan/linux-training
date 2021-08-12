import pandas as pd

data = pd.read_excel('EmployeeInformation.xlsx',header=1,dtype={'Mobile Number': str, 'Home Phome': str})
# print(data)
with open('user.txt','w') as file:
    for i in range(len(data['Fist Nane'])):
        employeetype = data['EmployeeType'][i]
        if (employeetype == 'contractor'): employeetype+='s'

        # dn
        st = 'dn: uid=' + data['Fist Nane'][i].lower() + data['Last Name'][i].lower() + ',ou=' + data['Residential Addresss'][i].lower() + ',ou='+ employeetype + ',ou=employees,dc=ltacademy,dc=com' + '\n'
        # objectClass
        st += 'objectClass: inetOrgPerson'+'\n'
        st += 'objectClass: top'+'\n'
        # First Name  
        st += 'cn: ' + data['Fist Nane'][i]+'\n'
        # Last Name
        st += 'sn: ' + data['Last Name'][i]+'\n'
        # Email
        st += 'mail: ' + data['Email'][i]+'\n'
        # Mobile Number
        st += 'mobile: ' + data['Mobile Number'][i].split('.')[0] + '\n'
        # Home Phone
        st += 'homePhone: ' + data['Home Phome'][i].split('.')[0] + '\n'
        # EmployeeType
        st += 'employeeType: ' + data['EmployeeType'][i] + '\n'
        # Residential Addresss
        st += 'registeredAddress: ' + data['Residential Addresss'][i] + '\n'
        #uid
        st += 'uid: ' + data['Fist Nane'][i].lower() + data['Last Name'][i].lower() +'\n'

        file.write(st)
        file.write('\n')
