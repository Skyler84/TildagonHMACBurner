#!/usr/bin/python
import argparse
from tildagon_hmac_burner.client.main import main

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])