from sys import stdout
from random import shuffle


class Counter:
    def __init__(self):
        self.counter = 0
        self.previous_length = 0

    def update(self):
        stdout.write('\b' * self.previous_length)
        self.counter += 1
        message = f'{self.counter} done'
        self.previous_length = len(message)
        stdout.write(message)

    def finish(self):
        stdout.write('\n')
        self.__init__()


def write_to_csv(path, data, limit):
    print('Writing to', path)
    counter = Counter()

    with open(path, 'w') as file:
        i = 0
        for line in data:
            if i == limit:
                break
            line = ','.join(line)
            file.write(line + '\n')
            i += 1
            counter.update()

    counter.finish()


def get_items(path):
    items = []

    print('Reading', path)
    counter = Counter()

    with open(path, 'r') as file:
        for line in file:
            items.append(line.split(',')[0].strip())
            counter.update()

    counter.finish()
    return items


def process_data(data):
    data = list(data)
    print('Shuffling data')
    shuffle(data)
    print('Processing data')
    counter = Counter()

    for i in range(len(data)):
        line = data[i]
        line = list(line)
        iq = line[0]
        iq = get_magnitude(iq)
        line.append(str(iq))
        snr = float(line[2])

        if snr < -15 and iq < 5:
            line.append('No')
        else:
            line.append('Yes')

        line = list(map(str, line))
        data[i] = line
        counter.update()

    counter.finish()
    return data


def get_magnitude(iq):
    iq = complex(iq.replace('i', 'j'))
    magnitude = (iq.real**2 + iq.imag**2) ** 0.5
    return magnitude


test_data = get_items('test_data.csv')
test_labels = get_items('test_labels.csv')
test_snr = get_items('test_snr.csv')

test_data = zip(test_data, test_labels, test_snr)
test_data = process_data(test_data)
write_to_csv('test_samples.csv', test_data, limit=100000)

train_data = get_items('train_data.csv')
train_labels = get_items('train_labels.csv')
train_snr = get_items('train_snr.csv')

train_data = zip(train_data, train_labels, train_snr)
train_data = process_data(train_data)
write_to_csv('train_samples.csv', train_data, limit=200000)
