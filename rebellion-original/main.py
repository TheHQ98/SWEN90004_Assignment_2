
def main():

    tick = 0

    with open('output.csv', 'w+') as fp:
        fp.write('tick,quiet,jailed,active\n')
        for i in range(1000):
            fp.write("1, 1, 1, 1" + '\n') #TODO
            tick += 1


if __name__ == '__main__':
    main()