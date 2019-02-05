# -*- coding: utf-8 -*-
"""
python -i homework1.py CSfaculty.txt output.txt
"""
import sys, re

def main():
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    


    print('Input File: ',input_file_name)
    print('Output File: ',output_file_name)


    html=''
    for line in open(input_file_name):
        line = line.rstrip('\n')
        html = html+line


    """ Get the data for each cell in the table up-down, left-right order
    """
    #The following are the regular expresions an the procedure to find where in the document the tags <td> and </td> are
    starting_tag  = re.compile(r'<td>')
    ending_tag = re.compile(r'</td>')

    starting_tag_found = starting_tag.finditer(html)
    ending_tag_found = ending_tag.finditer(html)

    starting_index=[]
    ending_index=[]

    for i in starting_tag_found:
        starting_index.append(i.end())

    for i in ending_tag_found:
        ending_index.append(i.start())
        
    n_celdas = len(starting_index)
    celdas = []

    for i in range(n_celdas):
        if(starting_index[i]>=ending_index[i]):
            print('error')
            print(starting_index[i],ending_index[i])
        celdas.append(html[starting_index[i]:ending_index[i]])

    """Regular Expressions to look up
    """

    prof_name_re=re.compile(r'>[A-Z].*,.*</a')
    prof_position_re=re.compile(r'/>.*<br')
    prof_mail_re=re.compile(r'>.*@.*\.edu\s?<')
    prof_phone_re=re.compile(r'-\d\d\d\d')
    erasable_re = re.compile(r'<br />')


    #Final strings to print
    prof_name_list=[]
    prof_position_list=[]
    prof_mail_list=[]
    prof_phone_list=[]

    n_prof = int( n_celdas/2)

    def get_first_or_fill(list_of_strings):
        if len(list_of_strings)>0:
            return list_of_strings[0]
        else:
            return "   "

    for i in range(n_prof):
        #print('______________\nProf',i+1,'     |')
        #print(celdas[2*i])
        prof_name = prof_name_re.findall(celdas[2*i])
        #print(prof_name, end='|')
        prof_name_list.append(get_first_or_fill(prof_name)[1:-3])
        
        prof_position = prof_position_re.findall(celdas[2*i])
        #print(prof_position, end='|')
        
       
        lalala = get_first_or_fill(prof_position)[2:-3]
        if (erasable_re.search(lalala)!= None):
            e = erasable_re.search(lalala)
            e_start_index = e.span()[0]
            e_final_index = e.span()[1]
            lalala = lalala[0:e_start_index] + ' ' + lalala[e_final_index:]
        
        
        prof_position_list.append(lalala)
        #----------------------------------------------
        #print(celdas[2*i+1])
        prof_mail = prof_mail_re.findall(celdas[2*i+1])
        #print(prof_mail, end='|')
        prof_mail_list.append(get_first_or_fill(prof_mail)[1:-1])
        
        prof_phone = prof_phone_re.findall(celdas[2*i+1])
        #print(prof_phone)    
        prof_phone_list.append(get_first_or_fill(prof_phone)[1:])


    #Writing in a file
    output_file = open(output_file_name,'w')
    for i in range(n_prof):
        output_file.write('{0:<5}{1:<25}{2:<50}{3:<36}{4:<5}\n'.format(
                            i+1, 
                            prof_name_list[i],
                            prof_position_list[i],
                            prof_mail_list[i],
                            prof_phone_list[i])
                         )

    output_file.close()
    
    print('Writing to file .............. [done]')
main()