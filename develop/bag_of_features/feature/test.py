# -*- coding: utf-8 -*-

import feature

def main():
    for i, line in enumerate(feature.create('./t_shirts.jpg', 'BRISK').split('\n')):
        line = line.replace(' ', '')
        line = line.replace(',', '\t')
        print '%s\t%s' % (i, line)


if __name__ == '__main__':
    main()

