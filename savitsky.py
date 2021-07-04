import math
import os
import webbrowser
import wolframalpha  # For solving equations. 'SymPy' is too slower
import time

os.system('cls' if os.name == 'nt' else 'clear')  # Clear Terminal for accurately displaying ANSI color.

wolframalpha_client = wolframalpha.Client('L9E8EU-2YK54J6V64')  # My free wolframalpha API

data_list = open('input data.txt', 'r').read().split()  # Read input parameter
input_data_line = open('input data.txt', 'r').read().splitlines()  # Split lines for final report

# Remove extra lines from input data.txt file
input_data_line.pop()
input_data_line.pop()
input_data_line.pop()

# Assign Input values
displacement = float(data_list[1])
mean_chine_beam = float(data_list[4])
dead_rise = float(data_list[7])
LCG = float(data_list[9])
speed = float(data_list[12]) * 0.514444
c_v = speed / (math.sqrt(9.8 * mean_chine_beam))
density = float(data_list[15])
displacement_force = displacement * density * 9.8
c_l_beta = displacement_force / (0.5 * density * mean_chine_beam ** 2 * (speed ** 2))

print('\n\033[1;31;40mIt will take few minutes. Be patient!\n\033[0;37;40m')

query = 'Solve ' + str(c_l_beta) + '=x-0.0065*' + str(dead_rise) + 'x^0.6'  # making wolframalpha query
result = wolframalpha_client.query(query)  # getting Solution from wolframalpha
answer = next(result.results).text  # Get only text from wolframalpha result. Because it have graphs and other data.
only_value = answer.split()  # Remove 'x =' from 'x = value' and get only 'value'
c_l0 = float(only_value[2])  # Assign solution as c_l0


# Function for solving lambda
def find_lambda(tau):
    # 'Real' is for only getting real solution.
    query2 = 'Solve ' + str(c_l0) + '=' + str(tau) + '^1.1(0.012*x^0.5+0.0055*x^2.5/' + str(c_v ** 2) + ') real'
    result2 = wolframalpha_client.query(query2)
    answer2 = next(result2.results).text
    only_value2 = answer2.split()
    return float(only_value2[2])


# Function for finding value of l_m
def l_m(tau):
    return mean_chine_beam * find_lambda(tau)


# Function for finding value of l_p
def l_p(tau):
    value_2 = l_m(tau) * (0.75 - (1 / (5.21 * (c_v / find_lambda(tau)) ** 2 + 2.39)))
    return value_2


# Function for finding value of N
def n(tau):
    return displacement_force * math.cos(math.radians(tau))


# Function for finding value of δm
def dell_n(tau):
    return displacement_force * LCG - n(tau) * l_p(tau)


# Results list assign for report
report_tau = []
report_dell_n = []
tau_list = []
dell_n_list = []


# Function for calculating δm from 'mini' to 'maxi' value of tau in 'precision' value interval.
def cal(mini, maxi, precision):
    print('Iterating between \033[1;34;40m', round(mini, 5), '\033[0;37;40m and \033[1;34;40m', round(maxi, 5),
          '\033[0;37;40m degree with \033[1;34;40m', precision, '\033[0;37;40mdegree interval.\n')
    time.sleep(2)

    while mini <= maxi + 0.00001:
        print('Calculating for \033[1;34;40m', round(mini, 5), ' degree...\t')
        dell_n_list.append(abs(dell_n(mini)))  # Adding δm value in the list
        print('\033[1;33;40mCalculated!\033[0;37;40m')
        time.sleep(0.5)
        tau_list.append(round(mini, 5))  # Adding tau value in the list
        mini += precision
    time.sleep(2)
    print('\033[1;31;40mIteration Completed!\033[0;37;40m')
    time.sleep(1)
    print('Analyzing Results.')


# Calculation of minimum value of δm in iteration.
def result():
    global x_1
    x = tau_list[dell_n_list.index(min(dell_n_list))]  # Get the value of tau for minimum δm
    report_tau.append(x)
    dell = dell_n(x)
    report_dell_n.append(dell)  # Add the value of minimum δm
    print('\033[1;31;40mThe value of delta_m(δm) which is nearest zero is \033[1;33;40m', round(dell / 1000, 3),
          'kN \033[0;37;40mfor angle \033[1;33;40m', x, ' degree')
    time.sleep(2)
    x_1 = x


# First iteration for tau range 2 to 15. Savitsky applicable for this range.
cal(2, 15, 1)
result()


# User can stop iteration if he don't want more decimal value precision
def choices():
    choice = input('\033[0;30;47mDo you want more precision? (y/n): \033[0;37;40m')
    return choice


# Calculation of the range of next iteration
def fun(precision_1, precision_2):
    del tau_list[:]
    del dell_n_list[:]
    mini, maxi = x_1 - precision_1, x_1 + precision_1
    cal(mini, maxi, precision_2)
    result()


# Repeating iteration process with the inout of choices() function. Maximum 5 decimal precision possible.
num = 1
choic = choices()
while num <= 5 and choic == 'y':
    os.system('cls' if os.name == 'nt' else 'clear')
    if num == 1:
        fun(0.9, 0.1)
    if num == 2:
        fun(0.09, 0.01)
    if num == 3:
        fun(0.009, 0.001)
    if num == 4:
        fun(0.0009, 0.0001)
    if num == 5:
        fun(0.00009, 0.00001)
    choic = choices()
    num += 1
print('\n\033[1;31;40mIteration with ', num, ' decimal precision Completed.\n\n')

time.sleep(1)

print('\033[1;35;40mCreating report for \033[1;33;40mtau(τ) = ', report_tau)
print("Please wait! Don't click any key.")

lambda_list = []
l_m_list = []
l_p_list = []
n_list = []

# Creating final value for report
for taus in tau_list:
    lamda = find_lambda(taus)
    lambda_list.append(lamda)
    l_m = mean_chine_beam * lamda
    l_m_list.append(l_m)
    l_p = l_m * (0.75 - (1 / (5.21 * (c_v / lamda) ** 2 + 2.39)))
    l_p_list.append(l_p)
    n_list.append(displacement_force * math.cos(math.radians(taus)))

final_tau = report_tau[len(report_tau) - 1]
final_l_m = l_m_list[len(l_m_list) - 1]

# Calculating Power
viscosity = 0.00000119
re_number = speed * final_l_m / viscosity
cf = 0.075 / ((math.log10(re_number) - 2) ** 2)
s = final_l_m * mean_chine_beam * (1 / math.cos(math.radians(dead_rise)))
df = 0.5 * density * s * speed ** 2 * cf
t = displacement_force * math.sin(math.radians(final_tau)) + df
rt = t * math.cos(math.radians(final_tau))
pe = rt * speed / 1000


# Report creation
def report_txt():
    report = open('report.txt', 'w', encoding='utf8')  # Creation of report file with UTF-8 encoding. Because report
    # contain some unicode character.

    # Adding input value to the report
    report.write('Input Parameter:\n\n')
    for line in input_data_line:
        if input_data_line.index(line) < 6:
            report.write(line)
            report.write('\n')

    # Adding extra input value which are not in input data.txt file
    report.write('C_v\t\t\t')
    report.write(str(round(c_v, 3)))
    report.write('\nDisplacement Force\t')
    report.write(str(displacement_force))
    report.write(' N\n\n\n')

    # Adding iteration data in report
    report.write('Iteration Table:\n\n')
    report.write('τ\t\tC_Lβ\t\tC_l0\t\tλ\t\tlm\t\tlp\t\tN\t\tδm(kN)\t\n\n')
    for i in range(len(report_tau)):
        report.write(str(report_tau[i]))
        report.write('\t\t')
        report.write(str(round(c_l_beta, 3)))
        report.write('\t\t')
        report.write(str(round(c_l0, 3)))
        report.write('\t\t')
        report.write(str(round(lambda_list[i], 3)))
        report.write('\t\t')
        report.write(str(round(l_m_list[i], 3)))
        report.write('\t\t')
        report.write(str(round(l_p_list[i], 3)))
        report.write('\t\t')
        report.write(str(round(n_list[i], 3)))
        report.write('\t')
        report.write(str(round(report_dell_n[i] / 1000, 3)))
        report.write('\n')

    # Adding power calculation data in report
    report.write('\n\nFinal results:\n\ntau(τ)\t\t')
    report.write(str(final_tau))
    report.write('\nl_m\t\t')
    report.write(str(round(final_l_m, 3)))
    report.write('\n\n\n')

    # Adding power calculation data in report
    report.write('Power Calculation:\n\nϑ\t\t0.00000119\tm^2/s\nRe\t\t')
    report.write(str(round(re_number, 3)))
    report.write('\nC_f\t\t')
    report.write(str(round(cf, 5)))
    report.write('\nS\t\t')
    report.write(str(round(s, 3)))
    report.write('\t\tm^2\nD_f\t\t')
    report.write(str(round(df, 3)))
    report.write('\tN\nT\t\t')
    report.write(str(round(t, 3)))
    report.write('\tN\nR_T\t\t')
    report.write(str(round(rt, 3)))
    report.write('\tN\nP_E\t\t')
    report.write(str(round(pe, 4)))
    report.write("\tkW\n\nYou will find all the formula in 226th page of Molland's Book. \nLink: "
                 "https://drive.google.com/file/d/1k6IiN0rNBDXruri-8Q2eOFC2lx1TYwJH/view?usp=sharing")
    report.close()


print('\n\033[1;31;40mReport Created!')
time.sleep(2)

print('\033[0;30;47mHow do you want your report?\n\033[1;33;40m[1]  Create a report.txt file.\n[2]  Write in a excel '
      'file.\nChose 1 or 2:',
      end='')
choi = input()
if choi == '1':
    report_txt()  # Report saved

    # get file location
    print('\n\033[1;31;40mreport.txt \033[0;37;40mfile saved at the location:\n\t\033[1;31;40m', os.getcwd())

if choi == '2':
    report_txt()

    # Writing in excel possible. I'll add this later
    print('\n\033[0;37;40mSorry! This option is not available right now.')
    print('But a\033[1;31;40m report.txt\033[0;37;40m file saved at the location:\n\t\033[1;31;40m', os.getcwd())

time.sleep(2)
print("\n\033[0;37;40mYou can see the details about \033[1;31;40mResistance prediction by savitsky method\033[1;31;40m "
      "in \033[0;37;40mMolland's book.\n")

time.sleep(3)
inp = input("\033[0;37;470\nWant to download Moland's book? Press \033[1;31;40mEnter\033[0;37;40m to download "
            "or\033[1;31;40m press any key and enter\033[0;37;40m to exit.\033[0;37;40m")

if inp == '':  # Checking 'enter' key.

    # Browsing Moland's book in Google drive
    webbrowser.open("https://drive.google.com/file/d/1k6IiN0rNBDXruri-8Q2eOFC2lx1TYwJH/view?usp=sharing", new='2')

time.sleep(2)
print("\n\033[95mOpening report in default text editor", flush=True, end='')


# Loading Animation
for i in range(7):
    time.sleep(0.5)
    print('.', flush=True, end='')

webbrowser.open('report.txt', new='2')  # Opening report in a default text editor.
