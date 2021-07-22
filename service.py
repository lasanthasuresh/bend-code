import json
import csv
import os

from date_utils import to_epoch_date

root_path = "D:\MSC-Project\company-data\P0717"

decistions = {}


# region decisions
def get_desition(company, date):
    if company not in decistions:
        decistions[company] = load_company_decisions(company)

    if date not in decistions[company]:
        return '-'
    return decistions[company][date]


def load_company_decisions(company):
    data = {}
    with(open(get_decision_file(company))) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            data[row[0]] = row[1]

    return data


def get_decision_file(company):
    path = os.path.join(root_path, 'CompanyData-' + company)
    if os.path.exists(os.path.join(path, 'gru-records.csv')):
        return os.path.join(path, 'gru-records.csv')
    if os.path.exists(os.path.join(path, 'lstm-records.csv')):
        return os.path.join(path, 'lstm-records.csv')


# endregion


def load_all_data(date):
    with(open('data/companies.json')) as json_file:
        data = json.load(json_file)
        for company in data:
            company['decision'] = get_desition(company['id'], date if date is None else '2015-06-03')

        return data


def load_data_of_company(company, date):
    with(open('data/' + company + '.json')) as json_file:
        data = json.load(json_file)
    for company in data:
        company['decision'] = get_desition(company['id'], date if date is None else '2015-06-03')

    return data


def get_price_data(company):
    path = os.path.join(root_path, 'CompanyData-' + company, company + '.csv')
    price_points = []
    price_point_dict = {}
    with (open(path)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if row[0] != 'Date':
                price_points.append([to_epoch_date(row[0]), float(row[2])])
                price_point_dict[row[0]] = float(row[2])

    decitions = load_company_decisions(company)

    decision_points = []

    for k, v in decitions.items():
        if v == 'buy' or v == 'sell':
            decision_points.append([to_epoch_date(k), v, price_point_dict[k] ])

    return price_points, decision_points


if __name__ == '__main__':
    # print(get_desition('AEL','2013-08-05'))
    # profile(
    data = get_price_data('AEL')
    print(data)
