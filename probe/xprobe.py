import getopt
import sys


def usage():
    print("Usage: xprobe [-c <collector_address> | -t <target_file>]")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:t:", ["collector=", "target="])

        (collector, target) = (None, None)

        for o, a in opts:
            if o in ("-c", "--collector"):
                collector = a
            elif o in ("-t", "--target"):
                target = a
            else:
                assert False, "unhandled option"

        if not asn:
            print("Error: insufficient arguments", file=sys.stderr)
            usage()
            sys.exit(2)

    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

if __name__ == '__main__':
    main()