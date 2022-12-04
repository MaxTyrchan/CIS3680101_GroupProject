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
    data['FileNumber'] = line[8:19].strip()
    data['DefendName'] = line[20:41].strip()
    data['Complainant'] = line[42:55].strip()
    data['Attorney'] = line[57:81].strip()
    data['Cont'] = line[82:].strip()

    return data


def is_aka(line):
    if line[14:16] == "AKA":
        return True
    else:
        return False


def fingerprintAndBond(line, defend_data):

    if line[19:27] == "********":
        defend_data['Needs Fingerprinted'] = "Yes"
    elif line[20:24] == "BOND":
        defend_data['Bond'] = line[31:45].strip()
        defend_data['Needs Fingerprinted'] = "No"
    else:
        defend_data['Bond'] = "WPA"
        defend_data['Needs Fingerprinted'] = "No"

    return defend_data


def is_bond(prevline):
    if prevline[19:27] == "********" or prevline[14:16] == "AKA":
        return True
    else:
        return False


def process_bond(line, defend_data):
    if line[20:24] == "BOND":
        defend_data['Bond'] = line[31:45].strip()
    else:
        defend_data['Bond'] = "WPA"

    return defend_data


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


def process_secondline_report_offence(line, offense_data):
    if line[13] != "":
        offense_data['CLS'] = line[13].strip()
    else:
        offense_data['CLS'] = ""
    if line[18] != "":
        offense_data['P'] = line[18].strip()
    else:
        offense_data['P'] = ""
    if line[23] != "":
        offense_data['L'] = line[23].strip()
    else:
        offense_data['L'] = ""
    try:
        if line[50] != "":
            offense_data['Judgement'] = line[50:70].strip()
        else:
            offense_data['Judgement'] = ""
        if line[81] != "":
            offense_data['ADA'] = line[81:83].strip()
        else:
            offense_data['ADA'] = ""
    except IndexError:
        offense_data['Judgement'] = ""
        offense_data['ADA'] = ""

    return offense_data


def write_data(writer, rpt_data, defend_data, offense_data):
    rec = dict(rpt_data)
    rec.update(defend_data)
    rec.update(offense_data)
    writer.writerow(rec)


def main():
    filename = input("plaese enter the filename:")
    # filename = "data.txt"
    header = [
        'RunDate', 'CourtDate', 'CourtTime', 'CourtRoom', 'No', 'FileNumber', 'DefendName', 'Complainant', 'Attorney', 'Cont', 'Needs Fingerprinted', 'Bond', 'Charge', 'Plea', 'Ver', 'CLS', 'P', 'L', 'Judgement', 'ADA'
    ]

    newfilename = filename.replace('.txt', '')
    csvfile = open(f'{newfilename}.csv', 'w', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()

    infile = open(filename)
    prevline = ""

    rpt_data = {}
    defend_data = {}
    offense_data = {}

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
        elif is_defend(line):
            if len(defend_data) > 0:
                write_data(writer, rpt_data, defend_data, offense_data)
                defend_data = {}
                offense_data = {}
            defend_data = process_report_defend(line)
        elif is_defend(prevline):
            fingerprintAndBond(line, defend_data)
        elif is_aka(prevline):
            fingerprintAndBond(line, defend_data)
        elif is_bond(prevline):
            process_bond(line, defend_data)
        elif is_offence(line):
            if len(offense_data) > 0:
                write_data(writer, rpt_data, defend_data, offense_data)
                offense_data = {}
            offense_data = process_report_offence(line)
        elif is_secondline_offence(prevline):
            process_secondline_report_offence(line, offense_data)
        else:
            print(line, end="")

        prevline = line
    csvfile.close()


if __name__ == '__main__':
    main()
