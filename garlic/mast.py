"""Python script to download data from MAST staging areas"""
import argparse
from ftplib import FTP_TLS
import getpass


def download_from_mast(user, stage, suffix):
    print("Connecting to MAST as user: " + user)
    password = getpass.getpass()
    ftps = FTP_TLS("archive.stsci.edu")
    ftps.login(user=user, passwd=password)
    ftps.prot_p()
    ftps.cwd("stage/" + stage)

    filenames = ftps.nlst()
    if suffix is None:
        suffix = ""
    for fn in filenames:
        if fn.endswith(suffix):
            print("getting " + fn)
            with open(fn, "wb") as fp:
                ftps.retrbinary("RETR {}".format(fn), fp.write)


# -----------------------------------------------------------------------------
# Script I/O
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
        fromfile_prefix_chars="@",
    )
    parser.add_argument("user")
    parser.add_argument("stage")
    parser.add_argument("--suffix", default=None)
    args = parser.parse_args()
    download_from_mast(args.user, args.stage, args.suffix)
