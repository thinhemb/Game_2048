
def read_high_score():
    file = open('high_score', 'r')
    init_high = int(file.readline())
    file.close()
    return init_high