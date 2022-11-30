"""
CIS 3680 Team Project Fall 2022
"""
import csv

END_OF_HEADER = "*" * 30


def is_summary_header(line):
    return line[0] == '1' and "RUN DATE:" in line


def is_page_header(line):
    return line[0] == '1' and "RUN DATE:" not in line


def process_page_header(infile):
    while True:
        line = infile.readline()

        if END_OF_HEADER in line:
            break


def is_report_header(line):
    return line[0] != '1' and "RUN DATE:" in line


def process_report_header(infile, line):
    data = {}

    data['RunDate'] = line[12:22].strip()

    while True:
        line = infile.readline()

        if END_OF_HEADER in line:
            break
        elif "COURT DATE:" in line:
            data["CourtDate"] = line[22:32].strip()
            data["CourtTime"] = line[44:52].strip()
            data["CourtRoom"] = line[78:].strip()

    return data


def is_defend(line):
    try:
        int(line[0:6])
        return True
    except ValueError:
        return False


def process_report_defend(line):
    data = {}

    data['No'] = line[0:6].strip()
    data['File Number'] = line[8:19].strip()
    data['Defend Name'] = line[20:41].strip()
    data['Complainant'] = line[42:55].strip()
    data['Attorney'] = line[57:81].strip()
    data['Cont'] = line[82:].strip()

    return data


def fingerprintAndBond(line):
    data = {}

    if line[19:27] == "********":
        data['Needs Fingerprinted'] = "Yes"
    elif line[20:24] == "BOND":
        data['Bond'] = line[31:45].strip()
        data['Needs Fingerprinted'] = "No"
    else:
        data['Bond'] = "WPA"
        data['Needs Fingerprinted'] = "No"

    return data


def is_bond(prevline):
    if prevline[19:27] == "********":
        return True
    else:
        return False


def process_bond(line):
    data = {}
    if line[20:24] == "BOND":
        data['Bond'] = line[31:45].strip()
    else:
        data['Bond'] = "WPA"

    return data


def is_offence(line):
    if line[8] == "(":
        return True
    else:
        return False


def process_report_offence(line):
    data = {}

    data['Charge'] = line[7:43].strip()
    data['Plea'] = line[50:65].strip()
    data['Ver'] = line[71:].strip()
    return data


def is_secondline_offence(prevline):
    if prevline[8] == "(":
        return True
    else:
        return False


def process_secondline_report_offence(line):
    data = {}
    if line[13] != "":
        data['CLS'] = line[13].strip()
    else:
        data['CLS'] = ""
    if line[18] != "":
        data['P'] = line[18].strip()
    else:
        data['P'] = ""
    if line[23] != "":
        data['L'] = line[23].strip()
    else:
        data['L'] = ""
    try:
        if line[50] != "":
            data['Judgement'] = line[50:70].strip()
        else:
            data['Judgement'] = ""
        if line[81] != "":
            data['ADA'] = line[81:83].strip()
        else:
            data['ADA'] = ""
    except IndexError:
        data['Judgement'] = ""
        data['ADA'] = ""

    return data


def main():
    # filename = input("plaese enter the filename:")
    filename = "data.txt"
    header = [
        'Date', 'Time', 'Courtroom', 'No', 'File', 'Number', 'Defendant Name', 'Complainant',	'Attorney', 'Cont', 'Needs Fingerprinted', 'Bond', 'Charge', 'Plea', 'Ver',	'CLS', 'P',	'L', 'Judgement', 'ADA'
    ]

    newfilename = filename.replace('.txt', '')
    csvfile = open(f'{newfilename}.csv', 'w')
    writer = csv.writer(csvfile)
    writer.writerow(header)

    infile = open(filename)
    prevline = ""

    while True:
        line = infile.readline()
        if line == "" or is_summary_header(line):
            break
        elif line == "\n":
            pass
        elif is_page_header(line):
            process_page_header(infile)
        elif is_report_header(line):
            rpt_data = process_report_header(infile, line)
            print("rpt_data =", rpt_data)
        elif is_defend(line):
            defence_data = process_report_defend(line)
            print("defence_data =", defence_data)
        elif is_defend(prevline):
            fingerprintAndBond_data = fingerprintAndBond(line)
            print("fingerprintAndBond =", fingerprintAndBond_data)
        elif is_bond(prevline):
            bond_data = process_bond(line)
            print("bonddata =", bond_data)
        elif is_offence(line):
            offence_data = process_report_offence(line)
            print("offence_data =", offence_data)
        elif is_secondline_offence(prevline):
            secondline_offence_data = process_secondline_report_offence(line)
            print("secondline_offence_data =", secondline_offence_data)
            print("\n")
        else:
            print(line, end="")

        prevline = line

        csvfile.close()


if __name__ == '__main__':
    main()
