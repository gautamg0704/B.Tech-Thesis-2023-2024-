shuffle = lambda x: x

from random import shuffle  # <---- UNCOMMENT THIS LINE FOR SHUFFLING

def add_to_list(path, lst):  # <------ CHANGE THIS VALUE FOR THE LIMIT       limit=15
    with open(path, 'r') as file:
        #i = 0
        for line in file:
            lst.append(line.split(',')[0].strip())
            #i += 1
            #if i == limit:
                #break

test_data = []
test_labels = []on
test_snr = []

add_to_list('test_data.csv', test_data)
add_to_list('test_labels.csv', test_labels)
add_to_list('test_snr.csv', test_snr)


def write_csv(path, data):
    with open(path, 'w') as file:
        for line in data:
            line = ','.join(line)
            file.write(line + '\n')


def process_data(data):
    data = list(data)
    shuffle(data)
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
    return data
        


def get_magnitude(iq):
    iq = iq.strip('-')
    if 'i' in iq:
        if '+' in iq:
            real, imaginary = iq.split('+')
        if '-' in iq:
            real, imaginary = iq.split('-')
            
        real = float(real)
        imaginary = float(imaginary[:-1])
        
    else:
        real = float(iq)
        imaginary = 0

    magnitude = (real**2 + imaginary**2) ** 0.5

    return magnitude

data = zip(test_data, test_labels, test_snr)
data = process_data(data)
write_csv('test_samples.csv', data)

